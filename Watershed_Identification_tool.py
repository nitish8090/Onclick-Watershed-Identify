from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import Qt
import sys


class PointTool(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas

    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        canvas.getCoordinates(point)
        print(list(point))


class MyCanvas(QgsMapCanvas):
    def __init__(self):
        super(MyCanvas, self).__init__()
        # Initialize paths and all
        self.csv_file_path = r"store_coordinates.csv"
        self.dem_path = r"D:\Nitish\1220_Dec\5_DEM_to_Stream_micro\Input Data\mndrayal_dem.img"

        self.pointLayer = None
        self.dem_layer = None

        # Initialize the functionality of the app
        self.initUI()
        self.setMyLayers()
        self.initTools()

    def setMyLayers(self):
        """
        Sets the DEM to display
        """
        self.dem_layer = QgsRasterLayer(self.dem_path, "InDEM")
        if self.dem_layer.isValid():
            print("Raster Loaded")
        self.setExtent(self.dem_layer.extent())
        self.setLayers([self.dem_layer])

    def initUI(self):
        button = QtWidgets.QPushButton(self)
        button.setText("Test Button")

    def initTools(self):
        tool = PointTool(self)
        self.setMapTool(tool)

    def getCoordinates(self, point):
        print("Hello")
        long, lat = list(point)
        to_write = "lat,long,nn\n{},{},name".format(lat, long)
        with open(self.csv_file_path, 'w') as csv_file:
            csv_file.write(to_write)

        uri = "file:///" + sys.path[0] + "/store_coordinates.csv?delimiter=%s&xField=%s&yField=%s&crs=%s" % (
            ",", "long", "lat", "epsg:4326")
        self.pointLayer = QgsVectorLayer(uri, 'New CSV', 'delimitedtext')
        if self.pointLayer.isValid():
            print("Point Loaded and Created")

        # symbol = QgsSymbol.defaultSymbol(pointLayer.geometryType())
        # symbol = renderer.symbol()
        # symbol.setColor(Qcolor.fromRgb(255,128,0))

        self.setLayers([self.pointLayer, self.dem_layer])
        canvas.refreshAllLayers()


# QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.16", True)

# Create a reference to the QgsApplication.  Setting the second argument to False disables the GUI.
qgs = QgsApplication([], True)
qgs.setPrefixPath(r"C:\Program Files\QGIS 3.16", True)

# Load providers
qgs.initQgis()

canvas = MyCanvas()
canvas.show()

# qgs.exitQgis()
sys.exit(qgs.exec_())
