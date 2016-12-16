import arcpy, os ,sys,datetime

Geodatabase=r"X:\PRUEBAS\XYZ\10K_V10.4_02_05_2016_BOGOTA_CON_ANOTACIONES.mdb"
ArchivoXYZ=r"X:\PRUEBAS\XYZ\190IC1.xyz"
responsable=r"CHAVEZ"

FeatureClass= Geodatabase+ os.sep+"Relieve"+os.sep+"Modelo_Digital_Terreno_P"
archivo = open(ArchivoXYZ, "r")

if arcpy.Exists(FeatureClass):
    fields = ['ALTURA_SOBRE_NIVEL_MAR', 'RESPONSABLE', 'FECHA_MODIFICACION',"SHAPE@"]
    cursor = arcpy.da.InsertCursor(FeatureClass, fields)
    for linea in archivo.readlines():
        linea=linea.strip('\n')
        Larray=linea.split(" ")
        print Larray
        point = arcpy.Point(float(Larray[0]),float(Larray[1]),float(Larray[2]))


        cursor.insertRow((Larray[2], responsable,datetime.datetime.now(),point))
    del cursor
