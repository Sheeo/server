#-------------------------------------------------------------------------------
# Copyright (c) 2014 Gael Honorez.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Public License v3.0
# which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/gpl.html
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#-------------------------------------------------------------------------------


from gamesContainer import  gamesContainerClass
from trueSkill.TrueSkill.FactorGraphTrueSkillCalculator import * 
from trueSkill.Team import *
from trueSkill.Teams import *

import time
import random, sys
from ladder.ladderMaps import ladderMaps
from PySide.QtSql import QSqlQuery
from PySide import QtCore


import gameModes.ladderGame
reload(gameModes.ladderGame)
from gameModes.ladderGame import ladder1v1GameClass



class ladder1v1GamesContainerClass(gamesContainerClass):
    '''Class for 1vs1 ladder games'''
    
    def __init__(self, db, parent=None):
        super(ladder1v1GamesContainerClass, self).__init__("ladder1v1", "ladder 1 vs 1", db, parent)
        
        self.version = 21
        self.season = None
        self.players = []
        self.listable = False
        self.host = False
        self.join = False
        self.parent = parent

    def getLeague(self, season, player):
        
        query = QSqlQuery(self.db)
        query.prepare("SELECT league FROM %s WHERE idUser = ?" % season)
        query.addBindValue(player.getId())
        query.exec_()
        if query.size() > 0 :
            query.first()
            return int(query.value(0))
        
        # place the player in his league !
        else :              
            query.prepare("INSERT INTO %s (`idUser` ,`league` ,`score`) VALUES (?, 1, 0)" % season)
            query.addBindValue(player.getId())     
            query.exec_()
            return 1

    def addPlayer(self, season, player) :

        self.season = season

        if not player in self.players :
            
            league = self.getLeague(season, player)
            
            player.setLeague(league)

            self.players.append(player)
            player.setAction("SEARCH_LADDER")
            trueSkill = player.getladder1v1Rating()

            deviation = trueSkill.getRating().getStandardDeviation()
            if deviation > 490 :
                player.getLobbyThread().sendJSON(dict(command="notice", style="info", text="<i>Welcome to the matchmaker system.</i><br><br><b>You will be randomnly matched until the system learn and know enough about you.</b><br>After that, you will be only matched against someone of your level.<br><br><b>So don't worry if your first games are uneven, this will get better over time !</b>"))
            elif deviation > 250 :
                progress = (500.0 - deviation) / 2.5
                player.getLobbyThread().sendJSON(dict(command="notice", style="info", text="The system is still learning you. <b><br><br>The learning phase is " + str(progress)+"% complete<b>"))
            
            return 1
        return 0

    def removePlayer(self, player) :
        
        if  player in self.players :
            self.players.remove(player)
            player.setAction("NOTHING")
            return 1
        return 0
    
    def getMatchQuality(self, player1, player2):
        
        matchup = [player1, player2]
        
        gameInfo = GameInfo()
        calculator = FactorGraphTrueSkillCalculator()
        return calculator.calculateMatchQuality(gameInfo, matchup)

    def getSelectedLadderMaps(self, playerId):
        query = QSqlQuery(self.db)
        query.prepare("SELECT idMap FROM ladder_map_selection WHERE idUser = ?")
        query.addBindValue(playerId)
        query.exec_()
        maps = []
        if query.size() > 0:
            while query.next():
                maps.append(int(query.value(0)))
        return maps

    def getPopularLadderMaps(self, count):
        query = QSqlQuery()
        query.prepare("SELECT `idMap` FROM `ladder_map_selection` GROUP BY `idMap` ORDER BY count(`idUser`) DESC LIMIT %i" % count)
        query.exec_()
        maps = []
        if query.size() > 0:
            while query.next():
                maps.append(int(query.value(0)))
        return maps

    def getMapName(self, mapId):
        query = QSqlQuery(self.db)
        query.prepare("SELECT filename FROM table_map WHERE id = ?")
        query.addBindValue(mapId)
        query.exec_()
        if query.size() > 0:
            query.first()
            return str(query.value(0)).split("/")[1].replace(".zip", "")
        else:
            return None

    def choose_ladder_map_pool(self, player1, player2):
        player_maps = [
            self.getSelectedLadderMaps(player1.getId()),
            self.getSelectedLadderMaps(player2.getId())
        ]

        common_maps = list(set(player_maps[0]).intersection(set(player_maps[1])))

        if len(common_maps) < 15:
            missing_maps = 15 - len(common_maps)
            choice = random.randint(0, 2)

            if choice == 1 or choice == 2:
                common_maps = common_maps + player_maps[choice-1][:missing_maps]


        if len(common_maps) < 15:
            missing_maps = 15 - len(common_maps)
            common_maps = common_maps + self.getPopularLadderMaps(missing_maps)[:missing_maps]

        return common_maps

    def startGame(self, player1, player2):
        gameName = str(player1.getLogin() + " Vs " + player2.getLogin())
        
        player1.setAction("HOST")
        gameUuid = self.createUuid(player1.getId())
        player2.setAction("JOIN")
        player1.setWantGame(True)

        map = "scmp_007"

        map_pool = self.choose_ladder_map_pool(player1, player2)

        mapChosen = random.choice(map_pool)
        map = self.getMapName(mapChosen)

        ngame = ladder1v1GameClass(gameUuid, self)

        uuid = ngame.getuuid()

        player1.setGame(uuid)
        player2.setGame(uuid)
        
        
        ngame.setLobbyState('Idle')
        #host is player 1
        
        ngame.setGameMap(map)
        
        ngame.setGameHostName(player1.getLogin())
        ngame.setGameHostUuid(player1.getId())
        ngame.setGameHostPort(player1.getGamePort())
        ngame.setGameHostLocalPort(player1.getGamePort())
        ngame.setGameName(gameName)
        ngame.setTime()
        
        #place the players
        ngame.placePlayer(player1.getLogin(), 1)
        ngame.placePlayer(player2.getLogin(), 2)
        
        ngame.addPlayerToJoin(player2)
        
        ngame.assignPlayerToTeam(player1.getLogin(), 1)
        ngame.assignPlayerToTeam(player2.getLogin(), 2)

        ngame.setLeaguePlayer(player1)
        ngame.setLeaguePlayer(player2)


        # player 2 will be in game
        
        self.addGame(ngame)

        
        #warn both players
        
        json = {}
        json["command"] = "game_launch"
        json["mod"] = self.gameTypeName
        json["mapname"] = str(map)
        json["reason"] = "ranked"
        json["uid"] = uuid
        json["args"] = ["/players 2", "/team 1"]
        
        player1.getLobbyThread().sendJSON(json)


    def searchForMatchup(self, player) :
        
        if  player in self.players :
        
            if player.getAction() != "SEARCH_LADDER" :
                return
                
            expandValue = player.getExpandLadder()

            trueSkill = player.getladder1v1Rating()

            deviation = trueSkill.getRating().getStandardDeviation()
            
            #minimum game quality to start a match.
            gameQuality = 0.8
            if deviation > 450 :
                gameQuality = 0.01               
            elif deviation > 350 :
                gameQuality = 0.1
            elif deviation > 300 :
                gameQuality = 0.7               
            elif deviation > 250 :
                gameQuality = 0.75
            else :
                gameQuality = 0.8
            
            # expand search
            gameQuality = gameQuality - expandValue
            if gameQuality < 0 :
                gameQuality = 0
                
            
            maxQuality = 0
            bestMatchupPlayer = ''

            for curPlayer in self.players :
                
                #check if we don't match again oursel
                if curPlayer.getLogin() != player.getLogin() :
                    #check if we don't match again a playing fella
                    if curPlayer.getAction() == "SEARCH_LADDER" :
                        curTrueSkill = curPlayer.getladder1v1Rating()

                        if deviation > 350 and curTrueSkill.getRating().getConservativeRating() > 1400 :
                            continue 

                        curMatchQuality = self.getMatchQuality(trueSkill, curTrueSkill)

                        if curMatchQuality > maxQuality :
                            maxQuality = curMatchQuality
                            bestMatchupPlayer = curPlayer
                #QtCore.QCoreApplication.processEvents()
            
            if maxQuality > gameQuality and bestMatchupPlayer != '' :

                #we've got a good matchup
                self.removePlayer(player)
                self.removePlayer(bestMatchupPlayer)
               
                self.startGame(player, bestMatchupPlayer)
                

        return 1
    
    def removeOldGames(self):
        '''Remove old games (invalids and not started)'''
        now = time.time()
        for game in reversed(self.games):

            diff = now - game.getTime()

            if game.getLobbyState() == 'open' and game.getNumPlayer() == 0 :
                
                game.setLobbyState('closed')      
                self.addDirtyGame(game.getuuid())        
                self.removeGame(game)

                continue

            if game.getLobbyState() == 'open' :
                host = game.getHostName()
                player = self.parent.players.findByName(host)

                if player == 0 : 
                    game.setLobbyState('closed')
                    self.addDirtyGame(game.getuuid())
                    self.removeGame(game)

                    continue
                else :
                    if player.getAction() != "HOST" :
                        
                        game.setLobbyState('closed')
                        self.addDirtyGame(game.getuuid())
                        self.removeGame(game)

                        continue

            
            if game.getLobbyState() == 'Idle' and diff > 60 :

                game.setLobbyState('closed')   
                self.addDirtyGame(game.getuuid())               
                self.removeGame(game)

                continue

            if game.getLobbyState() == 'playing' and diff > 60 * 60 * 8 : #if the game is playing for more than 8 hours

                game.setLobbyState('closed')
                self.addDirtyGame(game.getuuid())
                self.removeGame(game)

                continue
    