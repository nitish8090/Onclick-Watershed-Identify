from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from qgis.core import *
from qgis.gui import *
import sys


class MyCanvas(QgsMapCanvas):
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.initUI()
        self.setMyLayers()

    def setMyLayers(self):
        rlayer_path = r"D:\Nitish\1220_Dec\5_DEM_to_Stream_micro\Input Data\mndrayal_dem.img"
        self.rlayer = QgsRasterLayer(rlayer_path, "InDEM")
        if self.rlayer.isValid():
            print("Raster Loaded")
        self.setExtent(self.rlayer.extent())
        self.setLayers([self.rlayer])

    def initUI(self):
        button = QtWidgets.QPushButton(self)
        button.setText("Test Button")


# QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.16", True)
qgs = QgsApplication([], True)
# qgs.setPrefixPath(r"C:\Program Files\QGIS 3.16", True)

# Load providers
qgs.initQgis()
#
# canvas = MyCanvas()
# canvas.show()
#

# app = QApplication(sys.argv)
canvas = MyCanvas()
canvas.show()
sys.exit(qgs.exec_())
# qgs.exitQgis()

