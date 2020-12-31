from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import Qt
import sys
import qgis

import processing
from processing.core.Processing import Processing


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
    def __init__(self, dem_path):
        super(MyCanvas, self).__init__()
        self.setWindowTitle("Watershed Tool")

        # Initialize paths and all
        self.csv_file_path = r"temp_dir\store_coordinates.csv"
        self.dem_path = dem_path

        self.pointLayer = None
        self.dem_layer = None
        self.long, self.lat = 0, 0

        # Initialize the functionality of the app
        self.initUI()
        self.setMyLayers()
        self.initTools()

    def setMyLayers(self):
        # Sets the DEM to display
        self.dem_layer = QgsRasterLayer(self.dem_path, "InDEM")
        if self.dem_layer.isValid():
            print("Raster Loaded")
        self.setExtent(self.dem_layer.extent())
        self.setLayers([self.dem_layer])

    def initUI(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setText("Test Button")
        self.button.released.connect(self.generateBasin())

        label = QtWidgets.QLabel(self)
        label.setText(self.dem_path.split("\\")[-1])

    def initTools(self):
        tool = PointTool(self)
        self.setMapTool(tool)

    def getCoordinates(self, point):
        print("Hello")
        self.long, self.lat = list(point)
        to_write = "lat,long,nn\n{},{},name".format(self.lat, self.long)
        with open(self.csv_file_path, 'w') as csv_file:
            csv_file.write(to_write)

        uri = "file:///{}/{}?delimiter={}&xField={}&yField={}&crs={}".format(sys.path[0], self.csv_file_path,
                                                                             ",", "long", "lat", "EPSG:32643")
        self.pointLayer = QgsVectorLayer(uri, 'New CSV', 'delimitedtext')
        if self.pointLayer.isValid():
            print("Point Loaded and Created")

        self.setLayers([self.pointLayer, self.dem_layer])
        # self.refreshAllLayers()
        # self.generateBasin()

    def generateBasin(self):
        basin_path = 'temp_dir/hehl.tif'
        coordinate_string = '{},{} [EPSG:32643]'.format(self.long, self.lat)
        processing.run("grass7:r.water.outlet", {'input': dem_path,
                                                 'coordinates': coordinate_string,
                                                 'output': basin_path,
                                                 'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0,
                                                 'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': ''})
        basin_raster = QgsRasterLayer(basin_path, "basin")
        if basin_raster.isValid():
            print("Basin Raster Created")
        self.setLayers([basin_raster, self.pointLayer, self.dem_layer])
        self.refreshAllLayers()


# QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.16", True)
# Create a reference to the QgsApplication.  Setting the second argument to False disables the GUI.
qgs = QgsApplication([], True)
# qgs.setPrefixPath(r"C:\Program Files\QGIS 3.16", True)

# Load providers
qgs.initQgis()
Processing.initialize()

# Create canvas and show
dem_path = sys.path[0] + r"\example_raster\dem.img"
canvas = MyCanvas(dem_path=dem_path)
canvas.show()



# qgs.exitQgis()
sys.exit(qgs.exec_())
