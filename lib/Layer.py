import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox, QGraphicsItemGroup
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

class Layer:
    def __init__(self, name):
        self.name = name
        self.group = QGraphicsItemGroup()
        self.visible = True

    def addItem(self, item):
        self.group.addToGroup(item)

    def setVisible(self, visible):
        self.visible = visible
        self.group.setVisible(visible)
