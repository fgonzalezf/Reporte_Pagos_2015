import arcpy,os,sys

Geoadatabase = r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\Calculo_Planchas\Migracion_Modelo_25K\Integrada_06_07_2016.gdb"


def CalcularHoja(FeatuareClass,indice,Campo,Valor):
    try:
        arcpy.MakeFeatureLayer_management(indice,"LayerExtent",Campo+"='"+Valor+"'")
        arcpy.MakeFeatureLayer_management(FeatuareClass,"LayerCapa")
        arcpy.SelectLayerByLocation_management("LayerCapa","INTERSECT","LayerExtent","-2 METERS","NEW_SELECTION")
        result = arcpy.GetCount_management("LayerCapa")
        count=int(result.getOutput(0))
        if count>0:
            workspace = os.path.dirname(Geoadatabase)
            edit = arcpy.da.Editor(workspace)
            edit.startEditing(False, True)
            edit.startOperation()

            with arcpy.da.UpdateCursor("LayerCapa", "HOJA") as cursor:
                for row in cursor:
                    if row[0] is None:
                        row[0]=Valor
                        cursor.updateRow(row)

            edit.stopOperation()
            edit.stopEditing(True)
    except:
        pass
    arcpy.Delete_management("LayerExtent")
    arcpy.Delete_management("LayerCapa")


def ListadoHojas(FeatureClass):
    Listado=[]
    with arcpy.da.SearchCursor(FeatureClass, "HOJA") as cursor:
        for row in cursor:
            Listado.append(row[0])
    return Listado


arcpy.env.workspace= Geoadatabase

ListaDatasets=arcpy.ListDatasets()
Indice=Geoadatabase+os.sep+"Indice_Mapas\Indice_Hoja_Cartografica"
Planchas=ListadoHojas(Indice)
NumeroPlanchas=len(Planchas)
FeatuaresConInformacion=[]
print "Recorriendo Geodatabase"
for dataset in ListaDatasets:
    arcpy.env.workspace=Geoadatabase+os.sep+dataset
    ListaFeatureClass= arcpy.ListFeatureClasses()
    for fc in ListaFeatureClass:
        result = arcpy.GetCount_management(fc)
        count=int(result.getOutput(0))
        if fc !="Indice_Hoja_Cartografica" and count>0:
            print fc
            FeatuaresConInformacion.append(Geoadatabase+os.sep+dataset+os.sep+fc)



print fc
NumeroCapas = len(FeatuaresConInformacion)
print "Numero de Capas "+str(NumeroCapas)
capaActual=0
for Feat in FeatuaresConInformacion:
    capaActual=capaActual+1
    planchaActual=0
    for plancha in Planchas:
        planchaActual=planchaActual+1
        print os.path.basename(Feat)
        print os.path.basename(Feat)+"...(" +str(capaActual)+  os.sep+str(NumeroCapas) + ")"  + "..."+ plancha + "...." + str(planchaActual)+" de "+str(NumeroPlanchas)
        CalcularHoja(Feat,Indice,"HOJA",plancha)
