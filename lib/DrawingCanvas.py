import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

# Use QPixmap as  a canvas to draw on
# Make sure the canvas transformations are not affected "rotate, pan, etc)"
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
        self.currentCapStyle = Qt.PenCapStyle.RoundCap

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
            
            # Tapered brush style
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
                    pen.setWidth(self.currentEraserSize)
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