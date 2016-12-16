import arcpy, os, sys

LayerEntrada=r""
SplitLayer=r""

workspace = os.path.dirname(LayerEntrada)

# Start an edit session. Must provide the workspace.
edit = arcpy.da.Editor(workspace)

# Edit session is started without an undo/redo stack for versioned data
#  (for second argument, use False for unversioned data)
edit.startEditing(False, True)

# Start an edit operation
edit.startOperation()

# Insert a row into the table.
with arcpy.da.InsertCursor(LayerEntrada, ('SHAPE@', 'Name')) as icur:
    icur.insertRow([(7642471.100, 686465.725), 'New School'])

# Stop the edit operation.
edit.stopOperation()

# Stop the edit session and save the changes
edit.stopEditing(True)
