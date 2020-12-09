# Buffer zones project 

## Libraries importing 
import os
from qgis.core import (QgsVectorLayer)
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing

## Project definition et libraries test 

project_path= os.getcwd()
rpg_path = project_path + ("/RPG_parcelles_SDAGE_2018.shp")
rpg_layer = iface.addVectorLayer(rpg_path, "RPG2_2018", "ogr")
type(rpg_layer)

## Test Pyqgis : import a given layer from the QGIS interface and displaying random features 
mc = iface.mapCanvas()
bati = mc.currentLayer()
bati.name()

for ft in rpg_layer.getFeatures():
    print (ft["ID_PARCEL"])
