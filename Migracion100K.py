
import arcpy, os, sys

Entrada=r"D:\Proyecto\EDICION\DEPARTAMENTALES\BK_01_07_2016.gdb\Relieve\Curva_Nivel"
Salida=r"X:\PRUEBAS\Departamentales\Modelo_Departamentales\Bk4\ModeloDepartamentales.gdb\Relieve\Curva_Nivel"
#arcpy.env.workspace = Geodatabase

Datasets = arcpy.ListDatasets()


def MapaFields(fcEntrada, FcSalida):
    try:
        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(fcEntrada)
        fieldmappings.addTable(FcSalida)
        fieldmap = fieldmappings.getFieldMap(fieldmappings.findFieldMapIndex("TEMPID"))
        fieldmap.addInputField(FcSalida, "OBJECTID")
        return fieldmappings

    except Exception as ex:
        arcpy.AddMessage("Error en MapaFields..." + ex.message)
        return None

filedmappingsIn= MapaFields(Entrada,Salida)
arcpy.Append_management(Entrada,Salida,"NO_TEST",filedmappingsIn)