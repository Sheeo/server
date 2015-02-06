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
from PySide import QtSql

import time
import gameModes.coopGame
reload(gameModes.coopGame)
from gameModes.coopGame import coopGame

class coopGamesContainerClass(gamesContainerClass):
    '''Class for custom claustrophobia games'''

    def __init__(self, db, parent = None):
        super(coopGamesContainerClass, self).__init__("coop", "coop", db, parent)

        self.host = False
        self.live = True
        self.join = False

        self.parent = parent
        
        self.listable = False
     
        self.version = 3
        self.betaPass = False
        self.parent = parent
    
    def addBasicGame(self, player, newgame, gamePort):
        
        playerLogin = player.getLogin()
        playerUuid = player.getId()
        playerState = player.getAction()
        session = player.getSession()
        gameUuid = self.createUuid(playerUuid)
        
        if playerState == "PLAYING" :
            return False
        elif playerState == "HOST" :
            return False
        elif playerState == "JOIN" :
            return False
        
        # check if the host is already hosting something.
        for game in self.games:
            if game.getLobbyState == 'open' :
                if game.getHostName() == playerLogin :
                    return False
                if game.getHostId() == session :
                    return False
        
        ngame = coopGame(gameUuid, self)
        ngame.setLobbyState('Idle')
        ngame.setGameHostName(playerLogin)
        ngame.setGameHostUuid(playerUuid)
        ngame.setGameHostPort(gamePort)
        ngame.setGameHostLocalPort(gamePort)
        ngame.setGameName(newgame)
        ngame.setTime()
        self.games.append(ngame)
        return ngame