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
from PySide import QtSql
from PySide import QtCore

from PySide.QtSql import *

import gameModes.ladderGame
reload(gameModes.ladderGame)
from gameModes.ladderGame import ladder1v1GameClass



class ladder1v1GamesContainerClass(gamesContainerClass):
    '''Class for 1vs1 ladder games'''
    MAP_COUNT=15
    
    def __init__(self, db, parent = None):
        super(ladder1v1GamesContainerClass, self).__init__("ladder1v1", "ladder 1 vs 1" ,db, parent)
        
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

    def fillMapsQuery(self, maps, query):
        n = self.MAP_COUNT-len(maps)
        if n <= 0:
            return

        query = QSqlQuery(self.db)    
        query.prepare(query % n)
        query.exec_()

        if query.size() > 0:
            while query.next():
                maps.append(query.value(0))

        return maps
    end

    def fillPopularMaps(self, maps):
        return self.fillMapsQuery(maps, "SELECT `idMap` FROM `ladder_map_selection` GROUP BY `idMap` ORDER BY count(`idUser`) DESC LIMIT %i")

    def fillRandomMaps(self, maps):
        return self.fillMapsQuery(maps, "SELECT `idmap` FROM `ladder_map` ORDER BY RAND( ) LIMIT %i")

    def fillPlayerMaps(self, maps, player_maps):
        n = self.MAP_COUNT-len(maps)
        if n <= 0:
            return

        maps = maps + player_maps
        return maps[:n]

    def startGame(self, player1, player2) :
        #start game
        
        #first clean old games that didnt start.
        for game in self.getGames() :
            if game.getLobbyState() == 'Idle' :
                for player in game.getPlayers() :
                    if player.getLogin() == player1.getLogin() or player.getLogin() == player2.getLogin() :
                        self.remove(game)
                        continue

        gameName = str(player1.getLogin() + " Vs " + player2.getLogin())
        
        #creating the game
        
        
        
        player1.setAction("HOST")
        
        gameUuid = self.createUuid(player1.getId())
        
        player2.setAction("JOIN")
        
        player1.setWantGame(True)

        map = "scmp_007"
        #self.db.open()
            
        query = QSqlQuery(self.db)
        # get player map selection for player 1
        
        query.prepare("SELECT CASE WHEN :p1 THEN 0 ELSE 1 END, idMap FROM ladder_map_selection WHERE idUser IN (:p1, :p2)")
        query.addBindValue('p1', player1.getId())
        query.addBindValue('p2', player2.getId())
        
        maps = []
        maps.append([])
        if query.size() > 0:
            while query.next():
                maps[query.value(0)].append(query.value[1])
        
        mapPool = list(set(maps[0]).intersection(set(maps[1])))

        # random players maps, then popular and finally random, will stop at 15 in pool
        self.fillPlayerMaps(mapPool, maps[random.randint(0,1)])
        self.fillPopularMaps(mapPool)
        self.fillRandomMaps(mapPool)
        
        mapChosen = random.choice(mapPool)

        query.prepare("SELECT filename FROM table_map WHERE id = ?")
        query.addBindValue(mapChosen)
        query.exec_()
        if query.size() > 0:
            query.first()
            map = str(query.value(0)).split("/")[1].replace(".zip", "")

        ngame = ladder1v1GameClass(gameUuid, self)

        uuid = ngame.getuuid()

        player1.setGame(uuid)
        player2.setGame(uuid)
        
        
        ngame.setLobbyState('Idle')
        #host is player 1
        
        ngame.setGameMap(map)
        
        ngame.setGameHostName(player1.getLogin())
        ngame.setGameHostUuid(player1.getId())
        ngame.setGameHostPort( player1.getGamePort())
        ngame.setGameHostLocalPort( player1.getGamePort())
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
        
#        player1.getLobbyThread().sendReply("LADDER_START", player2.getLogin(), int(1))
        
        
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
    
