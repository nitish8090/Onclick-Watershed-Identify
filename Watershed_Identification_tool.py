from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class PointTool(QgsMapTool):   
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas

    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        canvas.getCoordinates(point)

class MyCanvas(QgsMapCanvas):
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.initUI()
        self.setMyLayers()
        self.initTools()
        self.csv_file_path = r"D:\Nitish\_temp_delete\pointfile.csv"
        
    def setMyLayers(self):
        rlayer_path = r"D:\Nitish\1220_Dec\5_DEM_to_Stream_micro\Input Data\mndrayal_dem.img"
        self.rlayer = QgsRasterLayer(rlayer_path, "InDEM")
        self.setExtent(self.rlayer.extent())
        self.setLayers([self.rlayer])
        
    def initUI(self):
        button = QtWidgets.QPushButton(self)
        button.setText("Hello")
        
    def initTools(self):
        tool = PointTool(self)
        self.setMapTool(tool)
        
    def getCoordinates(self, point):
        print("Hello")
        long, lat = list(point)
        to_write = "lat,long,nn\n{},{},name".format(lat, long)
        with open(self.csv_file_path, 'w') as csv_file:
            csv_file.write(to_write)
        
        if self.canvasColor().name() == '#000000':
            self.setCanvasColor(Qt.white)
            self.refresh()
        else:
            self.setCanvasColor(Qt.black)
            self.refresh()
        
        uri = "file:///D:/Nitish/_temp_delete/pointfile.csv?delimiter=%s&xField=%s&yField=%s&crs=%s" % (",", "long", "lat", "epsg:4326")
        pointLayer = QgsVectorLayer(uri, 'New CSV','delimitedtext')
        
        symbol = QgsSymbol.defaultSymbol(pointLayer.geometryType())
        
        #symbol = renderer.symbol()
        #symbol.setColor(Qcolor.fromRgb(255,128,0))
        self.setLayers([pointLayer, self.rlayer])
        #canvas.refreshAllLayers() 
        
        if pointLayer.isValid():
            print("Okay")
            QgsProject.instance().addMapLayer(pointLayer)
        
canvas = MyCanvas()
canvas.show()


#uri = "file:///D:/Nitish/_temp_delete/pointfile.csv?delimiter=%s" % (",")
#pointLayer = QgsVectorLayer(uri, 'New CSV','delimitedtext')


