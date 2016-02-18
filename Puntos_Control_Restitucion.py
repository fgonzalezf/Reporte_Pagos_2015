__author__ = 'fernando.gonzalez'
import arcpy, os, sys

DGN = r"X:\PRUEBAS\INGRID\Prueba1\BOYACA_10000_BOG_171IVD2_V7.dgn"
Carpeta= r"X:\PRUEBAS\INGRID\Prueba1"
sistemaReferencia = r"C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\National Grids\South America\MAGNA Colombia Bogota.prj"
arcpy.env.workspace= DGN
arcpy.env.overwriteOutput=True
#DGN = sys.argv[1]
#Carpeta= sys.argv[2]
#sistemaReferencia = sys.arg[3]
tempGeodata=arcpy.CreatePersonalGDB_management(Carpeta,"temp")
#puntos dgn
spatialRef = arcpy.SpatialReference(sistemaReferencia)

dataset = arcpy.CreateFeatureDataset_management(tempGeodata,"Temp",spatialRef)

for fcDGN in arcpy.ListFeatureClasses():
    if fcDGN=="Point":
        ptGeodata=arcpy.FeatureClassToFeatureClass_conversion(fcDGN,dataset,fcDGN)
        semillaBosque = arcpy.FeatureClassToFeatureClass_conversion(fcDGN,dataset,"SemillaBosque",""" "Level" = 40 """)
    elif fcDGN=="Polyline":
        lnGeodata=arcpy.FeatureClassToFeatureClass_conversion(fcDGN,dataset,fcDGN)
        lineaBosque = arcpy.FeatureClassToFeatureClass_conversion(fcDGN,dataset,"LineaBosque",""" "Level" = 40 """)
        grilla= arcpy.FeatureClassToFeatureClass_conversion(fcDGN,dataset,"Grilla",""" "Level" = 63 """)
        BosquePoli= arcpy.FeatureToPolygon_management([lineaBosque,grilla],Carpeta+os.sep+"temp.mdb"+os.sep+"Bosque")






