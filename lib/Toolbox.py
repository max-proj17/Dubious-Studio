import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox, QFileDialog
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF, QFile
import math

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import AIWidget

dark_mode = QFile("lib/dark-mode.qss")

class Toolbox(QWidget):
    def __init__(self, drawingApp, layout=None, parent=None):
        super(Toolbox, self).__init__(parent)
        self.drawingApp = drawingApp
        layout = QVBoxLayout(self)
        
        self.dark_mode_toggle = QPushButton("Toggle Dark Mode", self)
        self.dark_mode_toggle.clicked.connect(self.toggle_dark_mode)
        self.dark_mode_active = False
        self.dark_mode_toggle.setCheckable(True)
        layout.addWidget(self.dark_mode_toggle)
        
        # Eraser slider
        self.eraserSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.eraserSlider.setMinimum(1)
        self.eraserSlider.setMaximum(20)
        layout.addWidget(QLabel("Eraser Size:"))
        layout.addWidget(self.eraserSlider)
        self.eraserSlider.setValue(10)

        # Brush Size
        self.sizeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(20)
        layout.addWidget(QLabel("Size:"))
        layout.addWidget(self.sizeSlider)
        self.sizeSlider.setValue(1)

        # Opacity
        self.opacitySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacitySlider.setMinimum(1)
        self.opacitySlider.setMaximum(100)
        layout.addWidget(QLabel("Opacity:"))
        layout.addWidget(self.opacitySlider)
        self.opacitySlider.setValue(100)

        # Brush Style
        self.capStyleComboBox = QComboBox(self)
        self.capStyleComboBox.addItems(["Flat", "Square", "Round", "Tapered"])
        layout.addWidget(QLabel("Cap Style:"))
        layout.addWidget(self.capStyleComboBox)
        self.capStyleComboBox.setCurrentIndex(2)
        
        # AI Widget
        # self.ai_widget = AIWidget.AIWidget()
        # layout.addWidget(self.ai_widget)
        
        # At the end
        self.saveButton = QPushButton("Save as .png", self)
        self.saveButton.clicked.connect(self.saveCanvas)
        layout.addWidget(self.saveButton)
        
        layout.addStretch(1)
        
    def saveCanvas(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Canvas", "", "PNG Files (*.png);;All Files (*)")
        if filename:
            if not filename.endswith('.png'):
                filename += '.png'
            self.drawingApp.saveCanvas(filename)

    def toggle_dark_mode(self):
        print("Toggling dark mode...")  # Debug print
        if self.dark_mode_toggle.isChecked():
            with open("lib/dark-mode.qss", "r") as file:
                dark_mode = file.read()
                print(dark_mode)  # Debug print
                QApplication.instance().setStyleSheet(dark_mode)
        else:
            QApplication.instance().setStyleSheet("")
