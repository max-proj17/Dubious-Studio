import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, \
    QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QComboBox, QLabel, QSlider
from PyQt6.QtGui import QPen, QColor, QPainterPath, QPainterPathStroker, QBrush
from PyQt6.QtCore import Qt, QPoint, QSize, QPointF


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
        self.capStyleComboBox.addItems(["Flat", "Square", "Round", "Tapered"])
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
        self.currentCapStyle = Qt.PenCapStyle.FlatCap

    def setTool(self, tool):
        self.currentTool = tool

    def setColor(self, color):
        self.currentColor = QColor(color)

    def setSize(self, size):
        self.currentSize = size

    def setOpacity(self, opacity):
        self.currentOpacity = opacity / 100.0

    def setCapStyle(self, capStyle):
        self.currentCapStyle = capStyle

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPoint = self.mapToScene(event.position().toPoint())
            self.endPoint = self.startPoint
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = self.mapToScene(event.position().toPoint())
            color = QColor(self.currentColor)
            color.setAlphaF(self.currentOpacity)

            if self.currentCapStyle == "Tapered":
                path = QPainterPath(self.startPoint)
                path.lineTo(self.endPoint)
                distance = math.sqrt((self.startPoint.x() - self.endPoint.x())**2 + (self.startPoint.y() - self.endPoint.y())**2)
                segments = max(int(distance), 1)
                gradientPath = QPainterPath()
                for i in range(segments):
                    t = i / segments
                    p = path.pointAtPercent(t)
                    # Modified width calculation for smoother tapering
                    width = self.currentSize * (1 - (2*t - 1)**2)  
                    segmentStroker = QPainterPathStroker()
                    segmentStroker.setWidth(width)
                    segmentPath = QPainterPath(p)
                    segmentPath.lineTo(path.pointAtPercent((i + 1) / segments))
                    gradientPath.addPath(segmentStroker.createStroke(segmentPath))
                self.scene().addPath(gradientPath, QPen(color), QBrush(color))
            else:
                pen = QPen(color, self.currentSize)
                pen.setCapStyle(self.currentCapStyle)
                self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y(), pen)

            self.startPoint = self.endPoint



    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDrawing = False


class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 500, 500)
        self.scene.setBackgroundBrush(Qt.GlobalColor.white)

        self.canvas = DrawingCanvas(self.scene, self)
        self.setCentralWidget(self.canvas)

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

        self.colorPalette.capStyleComboBox.currentTextChanged.connect(self.setCapStyle)

    def setCapStyle(self, text):
        capStyles = {
            "Flat": Qt.PenCapStyle.FlatCap,
            "Square": Qt.PenCapStyle.SquareCap,
            "Round": Qt.PenCapStyle.RoundCap,
            "Tapered": "Tapered"
        }
        self.canvas.setCapStyle(capStyles.get(text, Qt.PenCapStyle.FlatCap))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())
