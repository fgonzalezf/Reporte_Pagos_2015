import arcpy,os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox2"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Reporte de Pagos 2016"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        #Primer Parametro

        param0 = arcpy.Parameter(
        displayName="Tabla de Pagos de Entrada",
        name="TablaPagos",
        datatype="GPTableView",
        parameterType="Required",
        direction="Input")

        #Segundo Parametro

        param1 = arcpy.Parameter(
        displayName="Actividad Contractual",
        name="Actividad",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        param1.filter.type="ValueList"
        param1.filter.list=["Control Restitución","Control Calidad Digital","Actualización 100K","Control Actualización","Control Calidad Gráfico","Edición","Estandarización","Metadato"]

        #Tercer Parametro

        param2 = arcpy.Parameter(
        displayName="Número de Contrato",
        name="NumeroContrato",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        #Cuarto Parametro

        param3 = arcpy.Parameter(
        displayName="Reportar Periodo",
        name="ReportarPeriodo",
        datatype="GPBoolean",
        parameterType="Required",
        direction="Input")

        param3.value=False

        #Cuarto Parametro

        param4 = arcpy.Parameter(
        displayName="Periodo a Reportar",
        name="PeriodoReportar",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

        param5 = arcpy.Parameter(
        displayName="PDF Salida",
        name="PdfSalida",
        datatype="DEFile",
        parameterType="Required",
        direction="Output")

        param5.filterlist = ['pdf']

        params=[param0,param1,param2,param3,param4,param5]
        return params
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
