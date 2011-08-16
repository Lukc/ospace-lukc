#
#  Copyright 2001 - 2011 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of Outer Space.
#
#  Outer Space is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Outer Space is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Outer Space; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
from ige import log
from ige.ospace.Const import *
import ige.ospace.Rules as Rules
import ige.ospace.Utils as Utils

from ai_tools import *

client = None
db = None
playerID = None
player = None

def planetManager():
	pass

def shipDesignManager():
	# currently no designs for EDEN
	pass

def attackManager():
	pass
		
def run(aclient):
	global client, db, player, playerID
	client = aclient
	db = client.db
	player = client.getPlayer()
	playerID = client.getPlayerID()
	
	tool_parseDB(client, db)

	shipDesignManager()	
	planetManager()

	attackManager()	
	client.saveDB()

