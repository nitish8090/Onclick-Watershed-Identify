# To change backgorund color with a click

if self.canvasColor().name() == '#000000':
    self.setCanvasColor(Qt.white)
    self.refresh()
else:
    self.setCanvasColor(Qt.black)
    self.refresh()