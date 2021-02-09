
path_to_data="D:/Aspexit/Formations_internes/Creation_plugin_QGIS/Data_tests/Final_zoning.shp"
vlayer = iface.addVectorLayer(path_to_data, "Airports layer", "ogr")


######## CHARGEMENT RASTER ################

path_to_tif = "D:/Aspexit/Formations_internes/Creation_plugin_QGIS/Data_tests/Altitude.tif"
rlayer = QgsRasterLayer(path_to_tif, "SRTM")

###### UTILISATION DE COUCHES DEJA CHARGEES #################
mc=iface.mapCanvas()
layer=mc.currentLayer()
layer.name()


###### ACCEDER AUX CHAMPS D'UNE COUCHE ###########
for feature in layer.getFeatures():
    print (feature["nom_var"])    ## Accès au champ "nom_var"


##### LISTER TOUS LES ALGOS QGIS DISPOS ####
from qgis import processing
for alg in QgsApplication.processingRegistry().algorithms():
        print(alg.id(), "->", alg.displayName())
		
		
####  EXEMPLES DE DEUX ALGOS ENCHAINES VECTEUR ###################

myresult = processing.run("native:buffer", {'INPUT': layer,
					      'DISTANCE': 100.0,
					      'SEGMENTS': 10,
					      'DISSOLVE': True,
					      'END_CAP_STYLE': 0,
					      'JOIN_STYLE': 0,
					      'MITER_LIMIT': 10,
					      'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})           #### SAUVEGARDE DANS UN FICHIER TEMPORAIRE
					              
myresult2 = processing.run("native:buffer", {'INPUT': myresult['OUTPUT'],
					       'DISTANCE': 100.0,
					       'SEGMENTS': 10,
					       'DISSOLVE': True,
					       'END_CAP_STYLE': 0,
					       'JOIN_STYLE': 0,
					       'MITER_LIMIT': 10,
						   'OUTPUT': 'D:/test2.shp'})
						   
						   
######### AJOUTER UNE COUCHE DANS LE CANVAS DE QGIS ##########
QgsProject.instance().addMapLayer(myresult['output'])

####  EXEMPLES DE TRAITEMENT RASTER ###################					   
# r.neighbors
alg_params = {
    '-a': False,
    '-c': False,
    'GRASS_RASTER_FORMAT_META': '',
    'GRASS_RASTER_FORMAT_OPT': '',
    'GRASS_REGION_CELLSIZE_PARAMETER': 0,
    'GRASS_REGION_PARAMETER': None,
    'gauss': None,
    'input': rlayer,
    'method': 0,
    'quantile': '',
    'selection': None,
    'size': 3,
    'weight': '',
    'output': QgsProcessing.TEMPORARY_OUTPUT
}
# Attention, la couche créée est juste le nom de la couche temporaire pour les rasters, il faut aller la recharger ensuite
int_rast = processing.run('grass7:r.neighbors', alg_params)
rlayer2 = QgsRasterLayer(int_rast['output'], "Couche_inter")
rlayer2.name()




#### SAUVEGARDER UN FICHIER DANS UNE COUCHE SHAPEFILE ####

save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = "ESRI Shapefile"
save_options.fileEncoding = "UTF-8"
error = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                "testdata/my_new_shapefile",
                                                save_options)
if error[0] == QgsVectorFileWriter.NoError:
    print("success again!")
else:
  print(error)
  
 
 
 
####  TRAITEMENT QUAND PAS DE REPERTOIRE D ###################

# Attention aux slash
# Rajouter "r" devant le chemin de travail. 


####  BUG avec import processing ###################
#Essayer d'abord : import qgis
#Et ensuite from qgis import processing




#### REPROJETER UNE COUCHE ##############

path_to_data="D:/Aspexit/Formations_internes/Creation_plugin_QGIS/Data_tests/Final_zoning.shp"
vlayer = iface.addVectorLayer(path_to_data, "Airports layer", "ogr")

alg_params = {
    'INPUT': vlayer,
    'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
    'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
}

test = processing.run('native:reprojectlayer', alg_params)
QgsProject.instance().addMapLayer(test['OUTPUT'])