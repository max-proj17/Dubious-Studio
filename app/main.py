import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QSlider, QLabel, QHBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette
from PyQt6.QtCore import Qt, QPoint, QSize, pyqtSignal

# For when/if we use the lib folder
# root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(root_folder)


class HSVSliders(QWidget):
    def __init__(self, parent=None):
        super(HSVSliders, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.hueSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.hueSlider.setMaximum(359)  # Hue range: 0-359
        self.hueSlider.valueChanged.connect(self.updateColor)

        self.saturationSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.saturationSlider.setMaximum(255)  # Saturation range: 0-255
        self.saturationSlider.valueChanged.connect(self.updateColor)

        self.valueSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.valueSlider.setMaximum(255)  # Value range: 0-255
        self.valueSlider.valueChanged.connect(self.updateColor)

        self.layout.addWidget(QLabel("Hue"))
        self.layout.addWidget(self.hueSlider)
        self.layout.addWidget(QLabel("Saturation"))
        self.layout.addWidget(self.saturationSlider)
        self.layout.addWidget(QLabel("Value"))
        self.layout.addWidget(self.valueSlider)

    def updateColor(self):
        hue = self.hueSlider.value()
        saturation = self.saturationSlider.value()
        value = self.valueSlider.value()
        color = QColor.fromHsv(hue, saturation, value)
        self.parent().colorPreview.setStyleSheet(f"background-color: {color.name()}")
        self.colorSelected.emit(color)

    colorSelected = pyqtSignal(QColor)

class RGBSliders(QWidget):
    def __init__(self, parent=None):
        super(RGBSliders, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.redSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.redSlider.setMaximum(255)
        self.redSlider.valueChanged.connect(self.updateColor)

        self.greenSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.greenSlider.setMaximum(255)
        self.greenSlider.valueChanged.connect(self.updateColor)

        self.blueSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.blueSlider.setMaximum(255)
        self.blueSlider.valueChanged.connect(self.updateColor)

        self.layout.addWidget(QLabel("Red"))
        self.layout.addWidget(self.redSlider)
        self.layout.addWidget(QLabel("Green"))
        self.layout.addWidget(self.greenSlider)
        self.layout.addWidget(QLabel("Blue"))
        self.layout.addWidget(self.blueSlider)

    def updateColor(self):
        red = self.redSlider.value()
        green = self.greenSlider.value()
        blue = self.blueSlider.value()
        color = QColor(red, green, blue)
        self.parent().colorPreview.setStyleSheet(f"background-color: {color.name()}")
        self.colorSelected.emit(color)

    colorSelected = pyqtSignal(QColor)

class ColorSliders(QWidget):
    def __init__(self, parent=None):
        super(ColorSliders, self).__init__(parent)
        self.layout = QVBoxLayout(self)  # Change from QHBoxLayout to QVBoxLayout

        self.hsvRgbLayout = QHBoxLayout()  # New layout for HSV and RGB sliders
        self.layout.addLayout(self.hsvRgbLayout)  # Add this layout to the main layout

        self.hsvSliders = HSVSliders(self)
        self.rgbSliders = RGBSliders(self)

        self.hsvRgbLayout.addWidget(self.hsvSliders)  # Add to the new layout
        self.hsvRgbLayout.addWidget(self.rgbSliders)  # Add to the new layout

        self.colorPreview = QLabel(self)
        self.colorPreview.setFixedSize(QSize(100, 50))
        self.colorPreview.setAutoFillBackground(True)
        self.layout.addWidget(self.colorPreview)
        self.layout.setAlignment(self.colorPreview, Qt.AlignmentFlag.AlignCenter)  # Center the color preview

        self.hsvSliders.colorSelected.connect(self.updateFromHSV)
        self.rgbSliders.colorSelected.connect(self.updateFromRGB)
        
        self.updating = False
        
        self.hsvSliders.updateColor()
        self.rgbSliders.updateColor()

    def updateFromHSV(self, color):
        if not self.updating:
            self.updating = True
            self.rgbSliders.redSlider.setValue(color.red())
            self.rgbSliders.greenSlider.setValue(color.green())
            self.rgbSliders.blueSlider.setValue(color.blue())
            self.updating = False

    def updateFromRGB(self, color):
        if not self.updating:
            self.updating = True
            self.hsvSliders.hueSlider.setValue(color.hue())
            self.hsvSliders.saturationSlider.setValue(color.saturation())
            self.hsvSliders.valueSlider.setValue(color.value())
            self.updating = False

class ColorPalette(QWidget):
    def __init__(self, hsvSliders, parent=None):
        super(ColorPalette, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.hsvSliders = hsvSliders

        self.colorList = QListWidget(self)
        self.layout.addWidget(self.colorList)

        self.addColorButton = QPushButton("Add Selected Color", self)
        self.layout.addWidget(self.addColorButton)

        self.addColorButton.clicked.connect(self.addColor)

    def addColor(self):
        color = self.hsvSliders.colorPreview.palette().color(QPalette.ColorRole.Window)
        item = QListWidgetItem()
        item.setBackground(color)
        item.setSizeHint(QSize(50, 50))
        self.colorList.addItem(item)

    def getSelectedColor(self):
        item = self.colorList.currentItem()
        if item:
            return item.background().color()
        return None

class DrawingCanvas(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(DrawingCanvas, self).__init__(scene, parent)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.isDrawing = False
        self.currentColor = QColor(Qt.GlobalColor.black)
        self.currentTool = "draw"

    def setTool(self, tool):
        self.currentTool = tool

    def setColor(self, color):
        self.currentColor = QColor(color)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPoint = event.position().toPoint()
            self.endPoint = self.startPoint
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.position().toPoint()
            pen = QPen(self.currentColor)
            if self.currentTool == "erase":
                pen.setColor(Qt.GlobalColor.white)
                pen.setWidth(10)
            self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y(), pen)
            self.startPoint = self.endPoint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDrawing = False

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a white QGraphicsScene with 500x500 dimensions
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 500, 500)
        self.scene.setBackgroundBrush(Qt.GlobalColor.white)

        # Create the custom QGraphicsView for drawing
        self.canvas = DrawingCanvas(self.scene, self)
        self.setCentralWidget(self.canvas)

        # Sidebar with color options and tools
        self.sidebar = QWidget()
        self.layout = QVBoxLayout(self.sidebar)

        # HSV and RGB sliders
        self.colorSliders = ColorSliders(self.sidebar)
        self.layout.addWidget(self.colorSliders)
        self.colorSliders.hsvSliders.colorSelected.connect(lambda color: self.canvas.setColor(color))
        self.colorSliders.rgbSliders.colorSelected.connect(lambda color: self.canvas.setColor(color))

        self.colorPalette = ColorPalette(self.colorSliders, self.sidebar)  # Pass the HSVSliders instance
        self.layout.addWidget(self.colorPalette)

        # Tools
        self.tools = ["draw", "erase"]
        self.toolButtons = QButtonGroup(self.sidebar)
        for tool in self.tools:
            btn = QPushButton(tool.capitalize())
            btn.setCheckable(True)
            self.toolButtons.addButton(btn)
            self.layout.addWidget(btn)
            btn.clicked.connect(lambda checked, tool=tool: self.selectToolOrColor(tool))

        self.toolButtons.buttons()[0].setChecked(True)

        self.colorPalette.colorList.itemClicked.connect(lambda: self.canvas.setColor(self.colorPalette.getSelectedColor()))

        self.dock = QDockWidget("Tools", self)
        self.dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.setGeometry(100, 100, 620, 520)
        self.setWindowTitle('Drawing Canvas')
        self.show()

    def selectToolOrColor(self, tool):
        if tool == "draw":
            self.canvas.setTool("draw")
        elif tool == "erase":
            self.canvas.setTool("erase")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())