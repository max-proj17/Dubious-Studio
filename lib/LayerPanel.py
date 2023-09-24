import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from lib.Layer import Layer


class LayerPanel(QWidget):
    layerSelected = pyqtSignal(Layer)

    def __init__(self, parent=None):
        super(LayerPanel, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.layerList = QListWidget(self)
        self.layout.addWidget(self.layerList)

        self.addButton = QPushButton("Add Layer", self)
        self.layout.addWidget(self.addButton)
        self.addButton.clicked.connect(self.addLayer)

        self.removeButton = QPushButton("Remove Layer", self)
        self.layout.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.removeLayer)

        self.layers = []

    def addLayer(self):
        layerName, ok = QInputDialog.getText(self, "New Layer", "Layer Name:")
        if ok and layerName:
            layer = Layer(layerName)
            self.layers.append(layer)
            self.layerList.addItem(layerName)
            self.layerSelected.emit(layer)

    def removeLayer(self):
        currentItem = self.layerList.currentItem()
        if currentItem:
            index = self.layerList.row(currentItem)
            del self.layers[index]
            self.layerList.takeItem(index)

    def selectLayer(self, index):
        if 0 <= index < len(self.layers):
            self.layerSelected.emit(self.layers[index])
