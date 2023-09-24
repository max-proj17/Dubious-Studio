
import sys, os
from PyQt6.QtWidgets import QDialog, QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import ColorPalette
from lib import Toolbox
from lib import DrawingCanvas
from lib import AIWidget



class MaskDialog(QDialog):
    def __init__(self, parent=None):
        super(MaskDialog, self).__init__(parent)
        self.canvas = QImage(1024, 1024, QImage.Format.Format_ARGB32)
        self.layout = QVBoxLayout(self)
        
        self.view = QGraphicsView(self)
        self.layout.addWidget(self.view)
        
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        
        # Check if parent.scene is not None
        if parent and parent.scene:
            # Initialize the canvas with the current drawing from the main window
            self.canvas = QImage(1024, 1024, QImage.Format.Format_ARGB32)
            painter = QPainter(self.canvas)
            parent.scene.render(painter)
            painter.end()
        else:
            # Initialize with a blank canvas if parent.scene is None
            self.canvas = QImage(1024, 1022, QImage.Format.Format_ARGB32)
            self.canvas.fill(Qt.GlobalColor.transparent)
        
        self.isDrawing = False
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        
        self.doneButton = QPushButton("Done", self)
        self.layout.addWidget(self.doneButton)
        self.doneButton.clicked.connect(self.saveMaskAndClose)
        
        # Display the initial canvas
        self.scene.addPixmap(QPixmap.fromImage(self.canvas))
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPoint = self.view.mapToScene(event.pos())
            self.endPoint = self.startPoint
            self.isDrawing = True
            
    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = self.view.mapToScene(event.pos())
            
            painter = QPainter(self.canvas)
            # Use a fully transparent color for the transparent brush
            painter.setPen(QPen(QColor(255, 255, 255, 0), 10, Qt.PenCapStyle.RoundCap))
            
            painter.drawLine(self.startPoint, self.endPoint)
            painter.end()
            
            self.startPoint = self.endPoint
            self.scene.clear()
            self.scene.addPixmap(QPixmap.fromImage(self.canvas))
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDrawing = False
            
    def saveMaskAndClose(self):
        # Ensure the path is correct and writable
        save_path = "C:/Users/maxfi/Desktop/mask.png"
        self.canvas.save(save_path)
        self.accept()



class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-512, -512, 2048, 2048)  # Extend scene size to show dark grey background

        self.canvas = DrawingCanvas.DrawingCanvas(self.scene, self)
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
        
        self.toolbox = Toolbox.Toolbox(self, rightLayout, self.rightSidebar)
        rightLayout.addWidget(self.toolbox)
        
        self.ai_widget = AIWidget.AIWidget(self.rightSidebar)
        rightLayout.addWidget(self.ai_widget)
        
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
        
        self.createMaskButton = QPushButton("Create Mask", self)
        self.createMaskButton.clicked.connect(self.openMaskDialog)
        self.rightSidebar.layout().addWidget(self.createMaskButton)

    def setCapStyle(self, text):
        capStyles = {
            "Flat": Qt.PenCapStyle.FlatCap,
            "Square": Qt.PenCapStyle.SquareCap,
            "Round": Qt.PenCapStyle.RoundCap,
            "Tapered": "Tapered"
        }
        self.canvas.setCapStyle(capStyles.get(text, Qt.PenCapStyle.FlatCap))

    def saveCanvas(self, filename):
        # Create a QImage object with the same dimensions as the canvas
        image = QImage(QSize(1024, 1024), QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)  # Fill the image with a white background

        # Create a QPainter object to paint the scene onto the QImage
        painter = QPainter(image)
        
        sourceRect = QRectF(-512, -512, 1024, 1024)
        
        self.scene.render(painter, QRectF(0, 0, 1024, 1024), sourceRect)
        painter.end()

        # Save the QImage to the specified filename
        image.save(filename)
    def openMaskDialog(self):
        maskDialog = MaskDialog(self)
        maskDialog.exec()   
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())
