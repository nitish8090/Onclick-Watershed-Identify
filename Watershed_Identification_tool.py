__author__ = "Nitish Patel"
__date__ = "3 January 2021"

"""
****************************************************************************
    Watershed Tool
    ---------------------
    Date                 : January 2021
    Copyright            : 
    Email                : 
*****************************************************************************
*                                                                           *
*   Development Notes:                                                      *
*                                                                           *
*****************************************************************************
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from qgis.core import *
from qgis.gui import *
# from qgis.PyQt.QtCore import Qt
import sys
# import qgis
from PyQt5.QtCore import QObject, pyqtSlot

import processing
from processing.core.Processing import Processing


# TODO: Fix processing not found in pycharm


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
        # TODO: Make this to accept file from file dialog
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
        # TODO: Change Button name
        self.button = QtWidgets.QPushButton(self)
        self.button.setText("Generate Watershed")
        self.button.released.connect(self.generateBasin)

        # TODO: Change button name and give function
        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setText("Generate Water")

        # TODO: Make a proper open file dailog and forward its value to dem raster
        self.openFileNameDialog()

        label = QtWidgets.QLabel(self)
        label.setText(self.dem_path.split("\\")[-1])

    # TODO: Make this function better and understand it
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Python Files (*.py)",
                                                  options=options)
        if fileName:
            print(fileName)

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
        self.basin_path = 'temp_dir/{}_basin.tif'.format(self.dem_path.split("\\")[-1].split(".")[0])
        coordinate_string = '{},{} [EPSG:32643]'.format(self.long, self.lat)
        processing.run("grass7:r.water.outlet", {'input': dem_path,
                                                 'coordinates': coordinate_string,
                                                 'output': self.basin_path,
                                                 'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0,
                                                 'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': ''})
        # Making basin raster a self solved the problem of raster not shhowing on the screen
        self.basin_raster = QgsRasterLayer(self.basin_path, "basin")
        if self.basin_raster.isValid():
            print("Basin Raster Created")
        self.setLayers([self.basin_raster, self.pointLayer, self.dem_layer])
        self.refreshAllLayers()


if __name__ == '__main__':
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
