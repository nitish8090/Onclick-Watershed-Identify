import qgis.core
from qgis.utils import *
from qgis.core import *

QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.16", True)
qgs = QgsApplication([], True)
qgs.initQgis()

qgs.exitQgis()