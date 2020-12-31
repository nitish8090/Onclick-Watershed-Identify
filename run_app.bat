@echo off
SET OSGEO4W_ROOT=C:\Program Files\QGIS 3.16
call "%OSGEO4W_ROOT%"\bin\o4w_env.bat
 
@echo off
path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass-7.4.3\lib
path %PATH%;C:\Program Files\QGIS 3.16\apps\Qt5\bin
path %PATH%;C:\Program Files\QGIS 3.16\apps\Python37\Scripts
 
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python;%OSGEO4W_ROOT%\apps\qgis\python\plugins
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis

"C:\Program Files\QGIS 3.16\apps\Python37\python.exe" "C:\Users\lenovo1\PycharmProjects\QGIS_Dev\Watershed_Identification_tool.py"
pause
