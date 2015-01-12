# Embedded file name: scripts/client/gui/Scaleform/released\uragan_minimap_tankview.py
"""
mEDI_S
UrAGAn
Script uragan_minimap_tankview.py
Thx @ Makct
"""
import BigWorld, Math
import math
import Avatar
from debug_utils import *
from gui.Scaleform.Minimap import Minimap
from gui.WindowsManager import g_windowsManager
import BattleReplay
import os, json

enemymodellist = {}
MTVconfig = {}

def minimapvhc():
	global MTVconfig

	player = BigWorld.player()
	if player is None:
		return
	else:
		if not MTVconfig['showInBattleReplay']:
			replayCtrl = BattleReplay.g_replayCtrl
			if replayCtrl.isPlaying:
				return
		if not hasattr(player, 'isOnArena'):
			return
		if player.isOnArena:
			arena = player.arena
			vehicles = arena.vehicles
			for vehicleID, desc in vehicles.items():
				if player.team is not vehicles[vehicleID]['team'] and not MTVconfig['showEnemy']:
					None
				elif player.team is not vehicles[vehicleID]['team'] or MTVconfig['showAllySPG'] and 'SPG' in desc['vehicleType'].type.tags or MTVconfig['showAllyTD'] and 'AT-SPG' in desc['vehicleType'].type.tags:
					if desc['isAlive'] and player.playerVehicleID != vehicleID:
						entity = BigWorld.entity(vehicleID)
						if entity is not None:
							m, rot = getEntryMatrix(vehicleID)
							mm = Math.WGCombinedMP()
							mm.translationSrc = m.source
							mm.rotationSrc = rot
							enemymodellist[vehicleID] = g_windowsManager.battleWindow.minimap._Minimap__ownUI.addEntry(mm, g_windowsManager.battleWindow.minimap.zIndexManager.getVehicleIndex(vehicleID) - 50)
							g_windowsManager.battleWindow.minimap._Minimap__ownUI.entryInvoke(enemymodellist[vehicleID], ('gotoAndStop', ['cursorNormal']))
						elif enemymodellist.has_key(vehicleID):
							g_windowsManager.battleWindow.minimap._Minimap__ownUI.delEntry(enemymodellist[vehicleID])
							enemymodellist.pop(vehicleID)
					elif enemymodellist.has_key(vehicleID):
						g_windowsManager.battleWindow.minimap._Minimap__ownUI.delEntry(enemymodellist[vehicleID])
						enemymodellist.pop(vehicleID)

		return


def getEntryMatrix(id):
	matrix = BigWorld.entities[id].matrix
	rotMatrix = BigWorld.entities[id].appearance.modelsDesc['gun']['model'].matrix
	m = Math.WGTranslationOnlyMP()
	m.source = matrix
	return (m, rotMatrix)


def minimapvhc_clb():
	minimapvhc()
	BigWorld.callback(1.0, minimapvhc_clb)

def loadMTVConfig():
	global MTVconfig

	config_file = os.getcwd() + os.sep + 'res_mods' + os.sep + 'configs' + os.sep + 'minimap_tankview.xc'

	if not os.path.exists(config_file):
		LOG_NOTE("config file missing (" + config_file + ")")
	else:
		#LOG_NOTE("load config (" + config_file + ")")
		try:
			MTVconfig = json.loads( open(config_file).read() )
		except:
			import traceback
			LOG_NOTE('config load fail (' + config_file + ')')
			LOG_NOTE(traceback.format_exc())

	#default config settings
	if not MTVconfig.has_key("showInBattleReplay"):
		MTVconfig['showInBattleReplay'] = False
	if not MTVconfig.has_key("showAllySPG"):
		MTVconfig['showAllySPG'] = True
	if not MTVconfig.has_key("showAllyTD"):
		MTVconfig['showAllyTD'] = False
	if not MTVconfig.has_key("showEnemy"):
		MTVconfig['showEnemy'] = False

loadMTVConfig()
minimapvhc_clb()
