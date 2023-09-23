import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint

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

        self.colors = ["black", "red", "green", "blue", "yellow"]
        self.colorButtons = QButtonGroup(self.sidebar)
        for color in self.colors:
            btn = QPushButton(color.capitalize())
            btn.setStyleSheet(f"background-color: {color}")
            btn.setCheckable(True)
            self.colorButtons.addButton(btn)
            self.layout.addWidget(btn)
            btn.clicked.connect(lambda checked, color=color: self.canvas.setColor(color))

        self.tools = ["draw", "erase"]
        self.toolButtons = QButtonGroup(self.sidebar)
        for tool in self.tools:
            btn = QPushButton(tool.capitalize())
            btn.setCheckable(True)
            self.toolButtons.addButton(btn)
            self.layout.addWidget(btn)
            btn.clicked.connect(lambda checked, tool=tool: self.canvas.setTool(tool))

        self.colorButtons.buttons()[0].setChecked(True)
        self.toolButtons.buttons()[0].setChecked(True)

        self.dock = QDockWidget("Tools", self)
        self.dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.setGeometry(100, 100, 620, 520)
        self.setWindowTitle('Drawing Canvas')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())
