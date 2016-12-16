import arcpy, os, sys

CarpetaEntrada = r"\\carto150\proyecto$\julio.alvarez\Julio\2014\INFORMES 25K\Proyecto 2016\Informes\Consolidado_GDB_Inconsistencias\Consolidado_GDB_Inconsistencias_2016\EDICION"
GeoodatabaseSalida= r"D:\Proyecto\EDICION\Consolidado_BORRAR\INTEGRADA\INTEGRADA_EDICION.gdb"

arcpy.env.workspace= CarpetaEntrada

ListaGeo= arcpy.ListWorkspaces("*","Access")
i=1
for gdb in ListaGeo:
    arcpy.env.workspace=gdb
    ListaFeat = arcpy.ListFeatureClasses("IN*")
    print gdb + "...."+ str(i)+ " de " + str(len(ListaGeo))
    for fc in ListaFeat:
        try:
            arcpy.Append_management(fc, GeoodatabaseSalida+ os.sep+ "INCONSISTENCIAS","NO_TEST")
        except:
            print "No migrada...."+ gdb
    i=i+1