import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, \
    QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QComboBox, QLabel, QSlider
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF


class ColorPalette(QWidget):
    def __init__(self, parent=None):
        super(ColorPalette, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.colorList = QListWidget(self)
        self.layout.addWidget(self.colorList)

        self.addColorButton = QPushButton("Add Color", self)
        self.layout.addWidget(self.addColorButton)

        self.addColorButton.clicked.connect(self.addColor)

        self.capStyleComboBox = QComboBox(self)
        self.capStyleComboBox.addItems(["Flat", "Square", "Round"])
        self.layout.addWidget(QLabel("Cap Style:"))
        self.layout.addWidget(self.capStyleComboBox)

        self.sizeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(20)
        self.layout.addWidget(QLabel("Size:"))
        self.layout.addWidget(self.sizeSlider)

        self.opacitySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacitySlider.setMinimum(1)
        self.opacitySlider.setMaximum(100)
        self.layout.addWidget(QLabel("Opacity:"))
        self.layout.addWidget(self.opacitySlider)

    def addColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            item = QListWidgetItem()
            item.setBackground(QColor(color))
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

        self.currentSize = 1
        self.currentOpacity = 1.0
        self.currentShape = "Round"
        self.currentCapStyle = Qt.PenCapStyle.FlatCap

    def setTool(self, tool):
        self.currentTool = tool

    def setColor(self, color):
        self.currentColor = QColor(color)

    def setSize(self, size):
        self.currentSize = size

    def setOpacity(self, opacity):
        self.currentOpacity = opacity / 100.0  # Convert to a value between 0 and 1

    def setShape(self, shape):
        self.currentShape = shape

    def setCapStyle(self, capStyle):
        self.currentCapStyle = capStyle

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            #self.startPoint = event.position().toPoint()
            self.startPoint = self.mapToScene((event.position().toPoint()))
            self.endPoint = self.startPoint
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            # self.endPoint = event.position().toPoint()
            self.endPoint = self.mapToScene(event.position().toPoint())
            pen = QPen(self.currentColor)
            ## testing this block below, it breaks da code
            #pen = QPen(self.currentColor, self.currentSize)
            #pen.setCapStyle(self.currentCapStyle)  # Set the current cap style
            #pen.setOpacity(self.currentOpacity)
            #until here
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

        self.colorPalette = ColorPalette(self.sidebar)
        self.layout.addWidget(self.colorPalette)

        self.tools = ["draw", "erase"]
        self.toolButtons = QButtonGroup(self.sidebar)
        for tool in self.tools:
            btn = QPushButton(tool.capitalize())
            btn.setCheckable(True)
            self.toolButtons.addButton(btn)
            self.layout.addWidget(btn)
            btn.clicked.connect(lambda checked, tool=tool: self.canvas.setTool(tool))

        #connect sliders to drawing canvas
        self.colorPalette.sizeSlider.valueChanged.connect(self.canvas.setSize)
        self.colorPalette.opacitySlider.valueChanged.connect(self.canvas.setOpacity)

        self.toolButtons.buttons()[0].setChecked(True)

        self.colorPalette.colorList.itemClicked.connect(lambda: self.canvas.setColor(self.colorPalette.getSelectedColor()))

        self.dock = QDockWidget("Tools", self)
        self.dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.setGeometry(100, 100, 620, 520)
        self.setWindowTitle('Drawing Canvas')
        self.show()

        # more drawing cap stuff
        self.colorPalette.capStyleComboBox.currentTextChanged.connect(self.setCapStyle)

    def setCapStyle(self, text):
        capStyles = {
            "Flat": Qt.PenCapStyle.FlatCap,
            "Square": Qt.PenCapStyle.SquareCap,
            "Round": Qt.PenCapStyle.RoundCap
        }
        self.canvas.setCapStyle(capStyles.get(text, Qt.PenCapStyle.FlatCap))
        # until here


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())
