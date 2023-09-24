import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

class Toolbox(QWidget):
    def __init__(self, layout=None, parent=None):
        super(Toolbox, self).__init__(parent)
        layout = QVBoxLayout(self)
        
        # Eraser slider
        self.eraserSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.eraserSlider.setMinimum(1)
        self.eraserSlider.setMaximum(20)
        layout.addWidget(QLabel("Eraser Size:"))
        layout.addWidget(self.eraserSlider)

        # Brush Size
        self.sizeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(20)
        layout.addWidget(QLabel("Size:"))
        layout.addWidget(self.sizeSlider)

        # Opacity
        self.opacitySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacitySlider.setMinimum(1)
        self.opacitySlider.setMaximum(100)
        layout.addWidget(QLabel("Opacity:"))
        layout.addWidget(self.opacitySlider)

        # Brush Style
        self.capStyleComboBox = QComboBox(self)
        self.capStyleComboBox.addItems(["Flat", "Square", "Round", "Tapered"])
        layout.addWidget(QLabel("Cap Style:"))
        layout.addWidget(self.capStyleComboBox)
        
        # At the end
        layout.addStretch(1)