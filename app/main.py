import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QPoint

class DrawingCanvas(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(DrawingCanvas, self).__init__(scene, parent)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.isDrawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPoint = event.position().toPoint()
            self.endPoint = self.startPoint
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.position().toPoint()
            self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y())
            self.startPoint = self.endPoint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDrawing = False

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a white QGraphicsScene with 500x500 dimensions
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 800, 800)
        self.scene.setBackgroundBrush(Qt.GlobalColor.white)

        # Create the custom QGraphicsView for drawing
        self.canvas = DrawingCanvas(self.scene, self)
        self.setCentralWidget(self.canvas)

        self.setGeometry(100, 100, 820, 820)
        self.setWindowTitle('Drawing Canvas')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())
