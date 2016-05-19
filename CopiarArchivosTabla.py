__author__ = 'fgonzalezf'

import arcpy, os,sys

CarpetaEntrada= r"D:\Museo\FOTOS VERTEBRADOS EDITADO"
CarpetaSalida=r"D:\Museo\ParaServidor\VERTEBRADOS"
Tabla =r"D:\Museo\Museo SIG.mdb\Museo\vertebrados"
Campo="IMAGEN"

arcpy.env.workspace=CarpetaEntrada
arcpy.env.overwriteOutput=True
ListaArchivos= arcpy.ListFiles()

for archivo in ListaArchivos:
    print archivo
    rows=arcpy.SearchCursor(Tabla)
    for row in rows:
        if row.getValue(Campo)!=None:

            Nombre= str(row.getValue(Campo))
            if Nombre==archivo:
                arcpy.Copy_management(archivo,CarpetaSalida+os.sep+Nombre)