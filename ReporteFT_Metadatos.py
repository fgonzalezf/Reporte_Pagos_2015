import arcpy, os, sys

Carpeta= sys.argv[1]
#Carpeta=r"D:\Proyecto\fernando.gonzalez\PRUEBAS\pruebas cargue\backup"
Reporte = Carpeta+ os.sep+ "ReporteGDB.txt"

archivo = open(Reporte, "w")
archivo.write("Reporte De FT y Tablas y Campo Responsable" +"\n")
def ListadoGDB():
    try:
        arcpy.env.workspace = Carpeta
        ListaGDB = arcpy.ListWorkspaces("*","Access")+arcpy.ListWorkspaces("*","FileGDB")
        return ListaGDB
    except:
        arcpy.AddError("Error el Recorrer Archivos")

def recorreGDB():
    ListaGDB=ListadoGDB()
    fc_count = len(ListaGDB)
    arcpy.SetProgressor("step", "Recorriendo Geodatabase",0, fc_count, 1)

    if ListaGDB is not None:
        for GDB in ListaGDB:
            arcpy.SetProgressorLabel("Procesando {0}...".format(os.path.basename(GDB)))
            arcpy.AddMessage("Geodatabase {0}...".format(os.path.basename(GDB)))
            archivo.write("\n"+"\n"+"*****"+os.path.basename(GDB) + "*******" +"\n"+"\n" )
            Geodatabase=GDB
            arcpy.env.workspace= Geodatabase
            ListaDatasets= arcpy.ListDatasets("","Feature")
            ListaTablas = arcpy.ListTables("Metadato*")
            if ListaDatasets is not None:
                for Dataset in ListaDatasets:
                    arcpy.env.workspace= Geodatabase+ os.sep+Dataset
                    ListaFeatuaresClass = arcpy.ListFeatureClasses()
                    if ListaFeatuaresClass is not None:
                        for fc in ListaFeatuaresClass:
                            print fc
                            #Buscar FT
                            if fc.lower().find ("ft_") !=- 1 or fc.lower().find ("error") !=- 1:
                                archivo.write("Features FT..." + fc +"\n" )
                            else:
                                ListaCampos = arcpy.ListFields(fc,"RESPONSABLE")
                                if ListaCampos is not None:
                                    for field in ListaCampos:
                                       archivo.write("Features con Campo "+ field.name +"...."+ fc +"\n" )
            if ListaTablas is not None:
                for table in ListaTablas:
                    archivo.write("Tablas de Metadato "+ "...."+ table +"\n" )
            arcpy.SetProgressorPosition()


recorreGDB()
archivo.close()
arcpy.SetProgressorPosition()





