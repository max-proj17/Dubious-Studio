
import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import ColorPalette
from lib import Toolbox

class DrawingCanvas(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(DrawingCanvas, self).__init__(scene, parent)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.isDrawing = False
        self.currentColor = QColor(Qt.GlobalColor.black)
        self.currentTool = "draw"

        self.currentEraserSize = 10

        self.currentSize = 1
        self.currentOpacity = 1.0
        self.currentCapStyle = Qt.PenCapStyle.FlatCap

        self.scaleFactor = 1.0
        self.rotationAngle = 0.0
        self.lastMousePosition = QPoint()

        self.setBackgroundBrush(QBrush(QColor(169, 169, 169)))  # Dark Grey Background

        # Create a white canvas item
        self.canvasItem = QGraphicsRectItem(0, 0, 1024, 1024)
        self.canvasItem.setBrush(QBrush(Qt.GlobalColor.white))

        # Set the scene rect to show the dark grey background around the canvas
        self.setSceneRect(-1024, -1024, 2048, 2048)

        # Center the canvas item in the scene
        self.canvasItem.setPos(-self.canvasItem.rect().width() / 2, -self.canvasItem.rect().height() / 2)
        self.scene().addItem(self.canvasItem)

    def setTool(self, tool):
        self.currentTool = tool

    def setColor(self, color):
        self.currentColor = QColor(color)

    def setEraserSize(self, eraser):
        self.currentEraserSize = eraser

    def setSize(self, size):
        self.currentSize = size

    def setOpacity(self, opacity):
        self.currentOpacity = opacity / 100.0

    def setCapStyle(self, capStyle):
        self.currentCapStyle = capStyle

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            factor = 1.1 if delta > 0 else 0.9
            self.scaleFactor *= factor

            # Get the position of the mouse cursor relative to the view
            cursor_pos = event.position().toPoint()
            # Map the cursor position to scene coordinates
            scene_pos = self.mapToScene(cursor_pos)

            # Adjust the view's center to zoom in/out at the cursor position
            view_center = self.mapToScene(self.viewport().rect().center())
            self.centerOn(view_center + (scene_pos - view_center) * (1 - factor))

            self.applyTransform()


    def mousePressEvent(self, event):
        print("Mouse Pressed")
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPoint = self.mapToScene(event.position().toPoint())
            self.endPoint = self.startPoint
            self.isDrawing = True
        elif event.button() == Qt.MouseButton.RightButton:
            self.lastMousePosition = event.globalPosition().toPoint()
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Enable scrolling drag mode
            self.setCursor(Qt.CursorShape.ClosedHandCursor)  # Change cursor to closed hand
            event.accept()

    def mouseMoveEvent(self, event):
        
        if self.isDrawing:
      
            self.endPoint = self.mapToScene(event.position().toPoint())
            
            pen = QPen(self.currentColor)

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
                    # Modified width calculation for sharper tapering
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
                if self.currentTool == "erase":
                    pen.setColor(Qt.GlobalColor.white)
                    pen.setWidth(10)
                self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y(), pen)

            self.startPoint = self.endPoint
        elif event.buttons() & Qt.MouseButton.RightButton:
            delta = event.globalPosition().toPoint() - self.lastMousePosition
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                self.rotationAngle += delta.x() * 0.5
            else:
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.lastMousePosition = event.globalPosition().toPoint()
            self.applyTransform()

    def mouseReleaseEvent(self, event):
        print("Mouse Released")
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDrawing = False
        elif event.button() == Qt.MouseButton.RightButton:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)  # Disable scrolling drag mode
            self.setCursor(Qt.CursorShape.ArrowCursor)  # Change cursor back to arrow
            event.accept()

    def applyTransform(self):
        # Reset the view transformation
        self.resetTransform()
        # Apply transformations to the canvas item
        transform = QTransform()
        transform.translate(self.canvasItem.rect().width() / 2, self.canvasItem.rect().height() / 2)
        transform.rotate(self.rotationAngle)
        transform.scale(self.scaleFactor, self.scaleFactor)
        transform.translate(-self.canvasItem.rect().width() / 2, -self.canvasItem.rect().height() / 2)
        self.canvasItem.setTransform(transform)

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-512, -512, 2048, 2048)  # Extend scene size to show dark grey background

        self.canvas = DrawingCanvas(self.scene, self)
        self.setCentralWidget(self.canvas)

        # Left Sidebar
        self.leftSidebar = QWidget()
        leftLayout = QVBoxLayout(self.leftSidebar)
            # HSV and RGB sliders
        self.colorSliders = ColorPalette.ColorSliders(self.leftSidebar)
        leftLayout.addWidget(self.colorSliders)
        self.colorSliders.hsvSliders.colorSelected.connect(lambda color: self.canvas.setColor(color))
        self.colorSliders.rgbSliders.colorSelected.connect(lambda color: self.canvas.setColor(color))
            # Presets can be an array of any length of hex codes "#xxxxxx"
        presets = ["#5A5A5A", "#FFD1DC", "#A2CFFE", "#FFFFB3", "#B2FFB2", "#E6CCFF", "#FFDAB9", "#B5EAD7", "#FFB6B9"]
        self.colorPalette = ColorPalette.ColorPalette(self.colorSliders, self.leftSidebar, presets=presets)
        leftLayout.addWidget(self.colorPalette)

        # Right Sidebar
            # Tools are on the right
        self.rightSidebar = QWidget()
        rightLayout = QVBoxLayout(self.rightSidebar)

        self.tools = ["draw", "erase"]
        self.toolButtons = QButtonGroup(self.rightSidebar)
        for tool in self.tools:
            btn = QPushButton(tool.capitalize())
            btn.setCheckable(True)
            self.toolButtons.addButton(btn)
            rightLayout.addWidget(btn)
            btn.clicked.connect(lambda checked, tool=tool: self.canvas.setTool(tool))

        self.toolButtons.buttons()[0].setChecked(True)

        self.colorPalette.colorList.itemClicked.connect(
            lambda: self.canvas.setColor(self.colorPalette.getSelectedColor()))

        # Connect slider value changed signal to setEraserSize method
        
        self.toolbox = Toolbox.Toolbox(layout=rightLayout, parent=self.rightSidebar)
        rightLayout.addWidget(self.toolbox)
        
        self.toolbox.sizeSlider.valueChanged.connect(self.canvas.setSize)
        self.toolbox.opacitySlider.valueChanged.connect(self.canvas.setOpacity)
        self.toolbox.eraserSlider.valueChanged.connect(self.canvas.setEraserSize)

        self.rightDock = QDockWidget("Tools", self)
        self.rightDock.setWidget(self.rightSidebar)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.rightDock)
        
        self.leftDock = QDockWidget("Colors", self)
        self.leftDock.setWidget(self.leftSidebar)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.leftDock)

        self.setGeometry(100, 100, 1144, 1144)  # Adjust window size to accommodate the larger canvas
        self.setWindowIcon(QIcon("resources/icon.png"))
        self.setWindowTitle('Dubious Studio')
        self.show()

        self.toolbox.capStyleComboBox.currentTextChanged.connect(self.setCapStyle)

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
