# Embedded file name: scripts/client/gui/Scaleform/released\uragan_minimap_tankview.py
"""
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
enemymodellist = {}

def minimapvhc():
	player = BigWorld.player()
	if player is None:
		return
	else:
		replayCtrl = BattleReplay.g_replayCtrl
		if replayCtrl.isPlaying:
			return
		if not hasattr(player, 'isOnArena'):
			return
		if player.isOnArena:
			arena = player.arena
			vehicles = arena.vehicles
			for vehicleID, desc in vehicles.items():
				activeTurretPosition = desc['vehicleType'].activeTurretPosition
				if activeTurretPosition != 0:
					LOG_WARNING(activeTurretPosition)
				if player.team is not vehicles[vehicleID]['team'] or 'SPG' in desc['vehicleType'].type.tags:
					if desc['isAlive'] and player.playerVehicleID != vehicleID:
						entity = BigWorld.entity(vehicleID)
						if entity is not None:
							m, rot = getEntryMatrix(vehicleID)
							mm = Math.WGCombinedMP()
							mm.translationSrc = m.source
							mm.rotationSrc = rot
							enemymodellist[vehicleID] = g_windowsManager.battleWindow.minimap._Minimap__ownUI.addEntry(mm, g_windowsManager.battleWindow.minimap.zIndexManager.getVehicleIndex(vehicleID) - 100)
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


minimapvhc_clb()
