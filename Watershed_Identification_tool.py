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

from PyQt5 import QtWidgets, QtGui                          # For buttons and Fonts
from PyQt5.QtWidgets import QFileDialog                     # For file dialog
# from PyQt5.QtWidgets import QApplication, QMainWindow
from qgis.core import *
from qgis.gui import *
# from qgis.PyQt.QtCore import Qt
import sys
# import os
# import qgis
# from PyQt5.QtCore import QObject, pyqtSlot

import processing
from processing.core.Processing import Processing


# TODO: Fix processing not found in pycharm


class PointTool(QgsMapTool):
    """
    Point selection tool used to generate point on clicking
    and forward it to the canvas and processing part
    """
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas

    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        canvas.getCoordinates(point)        # Forwarding coordinates to canvas


class MyCanvas(QgsMapCanvas):
    """
    Main Canvas Class
    """
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.setWindowTitle("Watershed Tool")
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))

        # Initialize paths and all
        self.csv_file_path = r"temp_dir\store_coordinates.csv"

        self.pointLayer = None
        self.long, self.lat = 0, 0

        # Initialize the functionality of the app
        self.initUI()
        self.initTools()

    def initUI(self):

        self.resize(1013, 808)  # Resize Window

        # Button to open DEM Raster
        self.openDemBtn = QtWidgets.QPushButton(self)
        self.openDemBtn.setGeometry(QtCore.QRect(350, 280, 291, 151))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.openDemBtn.setFont(font)
        self.openDemBtn.setObjectName("open_dem_btn")
        self.openDemBtn.setText("OPEN DEM")
        self.openDemBtn.released.connect(self.openFileNameDialog)
        self.openDemBtn.released.connect(self.openDemBtn.deleteLater)

        # Button to Generate Watershed Basin
        self.generateWatershedBtn = QtWidgets.QPushButton(self)
        self.generateWatershedBtn.setGeometry(QtCore.QRect(0, 30, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.generateWatershedBtn.setFont(font)
        self.generateWatershedBtn.setObjectName("generate_watershed_btn")
        self.generateWatershedBtn.setText("Generate Watershed")
        self.generateWatershedBtn.released.connect(self.generateBasin)

        # Button to generate Streams
        # TODO: Connect this to a function to generate streams
        self.generateStreamsBtn = QtWidgets.QPushButton(self)
        self.generateStreamsBtn.setGeometry(QtCore.QRect(0, 80, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.generateStreamsBtn.setFont(font)
        self.generateStreamsBtn.setObjectName("generate_streams_btn")
        self.generateStreamsBtn.setText("Generate Streams")
        self.generateStreamsBtn.released.connect(self.generateStreams)

        # TODO: Set these three labels to work
        self.dem_name = QtWidgets.QLabel(self)
        self.dem_name.setGeometry(QtCore.QRect(10, 10, 261, 21))
        self.dem_name.setObjectName("label_3")
        self.dem_name.setText("DEM Name:")

        self.xLabel = QtWidgets.QLabel(self)
        self.xLabel.setGeometry(QtCore.QRect(10, 160, 161, 41))
        self.xLabel.setObjectName("x_label")
        self.xLabel.setText("X: ")

        self.yLabel = QtWidgets.QLabel(self)
        self.yLabel.setGeometry(QtCore.QRect(10, 210, 161, 41))
        self.yLabel.setObjectName("y_label")
        self.yLabel.setText("Y: ")

    def setDemLayer(self, dem_path):

        # Sets the DEM to display
        self.dem_layer = QgsRasterLayer(dem_path, "InDEM")
        if self.dem_layer.isValid():
            print("Raster Loaded")
        self.setExtent(self.dem_layer.extent())
        self.setLayers([self.dem_layer])

    # TODO: Make this function better and understand it
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dem_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Image Files (*.img *.tif);;GeoTIFF Files (*.tif)",
                                                  options=options)
        if dem_path:
            self.setDemLayer(dem_path)

    def initTools(self):
        # Point Tool to get points
        tool = PointTool(self)
        self.setMapTool(tool)

    def getCoordinates(self, point):
        # Used to get coordinate from point tool
        self.long, self.lat = list(point)
        to_write = "lat,long,nn\n{},{},name".format(self.lat, self.long)
        with open(self.csv_file_path, 'w') as csv_file:
            csv_file.write(to_write)

        uri = "file:///{}/{}?delimiter={}&xField={}&yField={}&crs={}".format(sys.path[0], self.csv_file_path,
                                                                             ",", "long", "lat", "EPSG:32643")
        self.pointLayer = QgsVectorLayer(uri, 'New CSV', 'delimitedtext')
        if self.pointLayer.isValid():
            print("Point Loaded and Created")

        self.xLabel.setText("X: {}".format(self.long))
        self.yLabel.setText("Y: {}".format(self.lat))
        self.setLayers([self.pointLayer, self.dem_layer])

    def generateBasin(self):
        # Generate Basin on button click
        self.basin_path = 'temp_dir/dem_basin.tif'
        coordinate_string = '{},{} [EPSG:32643]'.format(self.long, self.lat)
        processing.run("grass7:r.water.outlet", {'input': self.dem_layer,
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

    def generateStreams(self):
        pass


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
    canvas = MyCanvas()
    canvas.show()

    # qgs.exitQgis()
    sys.exit(qgs.exec_())
