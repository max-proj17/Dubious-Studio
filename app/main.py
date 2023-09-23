import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QSlider, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF
from PyQt6.QtGui import QPainterPath


class ColorPalette(QWidget):
    def __init__(self, parent=None):
        super(ColorPalette, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.colorList = QListWidget(self)
        self.layout.addWidget(self.colorList)

        self.addColorButton = QPushButton("Add Color", self)
        self.layout.addWidget(self.addColorButton)

        self.addColorButton.clicked.connect(self.addColor)

        #eraser slider
        self.eraserSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.eraserSlider.setMinimum(1)
        self.eraserSlider.setMaximum(20)
        self.layout.addWidget(QLabel("Eraser Size:"))
        self.layout.addWidget(self.eraserSlider)

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
        self.currentEraserSize = 10;

        def mouseMoveEvent(self, event):
            if self.isDrawing:
                # Get the current point
                self.endPoint = self.mapToScene(event.position().toPoint())

                # Get the bounds of the canvasItem
                rect = self.canvasItem.mapToScene(self.canvasItem.rect()).boundingRect()

                # Adjust the endPoint if it is outside the bounds of the canvasItem
                if not rect.contains(self.endPoint):
                    x = min(max(self.endPoint.x(), rect.left()), rect.right())
                    y = min(max(self.endPoint.y(), rect.top()), rect.bottom())
                    self.endPoint = QPointF(x, y)

                # Draw the line
                pen = QPen(self.currentColor)
                if self.currentTool == "erase":
                    pen.setColor(Qt.GlobalColor.white)
                    pen.setWidth(10)
                self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y(),
                                     pen)
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
            # Get the current point
            self.endPoint = self.mapToScene(event.position().toPoint())

            # Get the bounds of the canvasItem
            rect = self.canvasItem.rect()

            # Map the start and end points to the canvasItem's coordinate system
            startPointInItem = self.canvasItem.mapFromScene(self.startPoint)
            endPointInItem = self.canvasItem.mapFromScene(self.endPoint)

            # Check if the startPoint and endPoint are within the bounds of the canvas item
            if rect.contains(startPointInItem) and rect.contains(endPointInItem):
                pen = QPen(self.currentColor)
                if self.currentTool == "erase":
                    pen.setColor(Qt.GlobalColor.white)
                    pen.setWidth(10)
                self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y(),
                                     pen)
                self.startPoint = self.endPoint
            else:
                # Reset the startPoint when the mouse moves outside the canvas
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

        self.toolButtons.buttons()[0].setChecked(True)

        self.colorPalette.colorList.itemClicked.connect(
            lambda: self.canvas.setColor(self.colorPalette.getSelectedColor()))

        # Connect slider value changed signal to setEraserSize method
        self.colorPalette.eraserSlider.valueChanged.connect(self.canvas.setEraserSize)


        self.dock = QDockWidget("Tools", self)
        self.dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.setGeometry(100, 100, 1144, 1144)  # Adjust window size to accommodate the larger canvas
        self.setWindowTitle('Drawing Canvas')
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())

