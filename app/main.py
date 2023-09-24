
import sys, os, time
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox, QSplashScreen
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import ColorPalette
from lib import Toolbox
from lib import DrawingCanvas
from lib import AIWidget
from lib import tfWidget

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
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    pixmap = QPixmap("resources/giphy.gif")
    splash = QSplashScreen(pixmap)
    splash.show()
    time.sleep(3)
    window = DrawingApp()
    window.show()
    splash.finish(window)
    sys.exit(app.exec())
