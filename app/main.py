import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QListWidget, QListWidgetItem, QSlider, QLabel, QHBoxLayout, QStyledItemDelegate, QStyle
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette, QIcon
from PyQt6.QtCore import Qt, QPoint, QSize, pyqtSignal

# For when/if we use the lib folder
# root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(root_folder)

# Needed for color palette
class NonDraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super(NonDraggableListWidget, self).__init__(parent)

    def startDrag(self, actions):
        pass

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
        
    def setColor(self, color):
        # Update HSV sliders
        self.hsvSliders.hueSlider.setValue(color.hue())
        self.hsvSliders.saturationSlider.setValue(color.saturation())
        self.hsvSliders.valueSlider.setValue(color.value())
        
        # Update RGB sliders
        self.rgbSliders.redSlider.setValue(color.red())
        self.rgbSliders.greenSlider.setValue(color.green())
        self.rgbSliders.blueSlider.setValue(color.blue())

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

class ColorItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        
        # Check if the item is selected
        if option.state & QStyle.StateFlag.State_Selected:
            # Set the color and width of the border
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            # Draw a rectangle around the item
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))

class ColorPalette(QWidget):
    def __init__(self, colorSliders, parent=None, presets=None):
        super(ColorPalette, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Store the colorSliders reference
        self.colorSliders = colorSliders

        self.colorList = NonDraggableListWidget(self)
        self.colorList.setDragDropMode(QListWidget.DragDropMode.NoDragDrop)
        self.colorList.setDragEnabled(False)
        self.colorList.setDragDropOverwriteMode(False)
        self.colorList.setViewMode(QListWidget.ViewMode.IconMode)
        self.colorList.setGridSize(QSize(60, 60))
        self.colorList.setFlow(QListWidget.Flow.LeftToRight)
        self.colorList.setWrapping(True)
        self.colorList.setSelectionMode(QListWidget.SelectionMode.SingleSelection)  # Set selection mode
        self.colorList.setItemDelegate(ColorItemDelegate(self.colorList))  # Set the custom delegate
        self.layout.addWidget(self.colorList)
        
        if presets:
            self.addPresetColors(presets)

        # Buttons layout
        self.buttonsLayout = QHBoxLayout()
        self.addColorButton = QPushButton("Add Selected Color", self)
        self.removeColorButton = QPushButton("Remove Color", self)
        self.buttonsLayout.addWidget(self.addColorButton)
        self.buttonsLayout.addWidget(self.removeColorButton)
        self.layout.addLayout(self.buttonsLayout)

        self.addColorButton.clicked.connect(self.addColor)
        self.removeColorButton.clicked.connect(self.removeColor)
        self.colorList.itemClicked.connect(self.updateSelectedColorAppearance)

    def updateSelectedColorAppearance(self, item):
        selected_color = item.background().color()
        
        # Update the color preview in the sliders widget
        self.colorSliders.colorPreview.setStyleSheet(f"background-color: {selected_color.name()}")
        
        # Update the sliders to match the selected color
        self.colorSliders.setColor(selected_color)

    def addColor(self):
        color = self.colorSliders.colorPreview.palette().color(QPalette.ColorRole.Window)
        item = QListWidgetItem()
        item.setBackground(color)
        item.setSizeHint(QSize(50, 50))
        self.colorList.addItem(item)
        
    def removeColor(self):
        currentRow = self.colorList.currentRow()
        if currentRow != -1:  # Check if a color is selected
            self.colorList.takeItem(currentRow)

    def getSelectedColor(self):
        item = self.colorList.currentItem()
        if item:
            return item.background().color()
        return None
    
    def updateSlidersAndPreview(self, item):
        selected_color = item.background().color()
        
        # Update the color preview in the sliders widget
        self.colorSliders.colorPreview.setStyleSheet(f"background-color: {selected_color.name()}")
        
        # Update the sliders to match the selected color
        self.colorSliders.setColor(selected_color)
        
    def addPresetColors(self, colors):
        for color in colors:
            item = QListWidgetItem()
            item.setBackground(QColor(color))
            item.setSizeHint(QSize(50, 50))
            self.colorList.addItem(item)

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

        # Presets can be an array of any length of hex codes "#xxxxxx"
        presets = ["#5A5A5A", "#FFD1DC", "#A2CFFE", "#FFFFB3", "#B2FFB2", "#E6CCFF", "#FFDAB9", "#B5EAD7", "#FFB6B9"]
        self.colorPalette = ColorPalette(self.colorSliders, self.sidebar, presets=presets)
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
        self.setWindowTitle('Dubious Studio')
        self.setWindowIcon(QIcon("resources/icon.png"))
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