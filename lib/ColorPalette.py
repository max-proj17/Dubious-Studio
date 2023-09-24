import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

class NonDraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super(NonDraggableListWidget, self).__init__(parent)

    def startDrag(self, actions):
        pass

class HSVSliders(QWidget):
    def __init__(self, parent=None):
        super(HSVSliders, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.hueSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.hueSlider.setMaximum(359)  # Hue range: 0-359
        self.hueSlider.valueChanged.connect(self.updateColor)
        self.hueSpinBox = QSpinBox(self)
        self.hueSpinBox.setMinimum(0)
        self.hueSpinBox.setMaximum(359)

        self.saturationSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.saturationSlider.setMaximum(255)  # Saturation range: 0-255
        self.saturationSlider.valueChanged.connect(self.updateColor)
        self.saturationSpinBox = QSpinBox(self)
        self.saturationSpinBox.setMinimum(0)
        self.saturationSpinBox.setMaximum(255)

        self.valueSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.valueSlider.setMaximum(255)  # Value range: 0-255
        self.valueSlider.valueChanged.connect(self.updateColor)
        self.valueSpinBox = QSpinBox(self)
        self.valueSpinBox.setMinimum(0)
        self.valueSpinBox.setMaximum(255)

        self.layout.addWidget(QLabel("Hue"))
        self.layout.addWidget(self.hueSlider)
        self.layout.addWidget(self.hueSpinBox)
        self.layout.addWidget(QLabel("Saturation"))
        self.layout.addWidget(self.saturationSlider)
        self.layout.addWidget(self.saturationSpinBox)
        self.layout.addWidget(QLabel("Value"))
        self.layout.addWidget(self.valueSlider)
        self.layout.addWidget(self.valueSpinBox)
        
        self.hueSlider.valueChanged.connect(self.hueSpinBox.setValue)
        self.hueSpinBox.valueChanged.connect(self.hueSlider.setValue)
        self.saturationSlider.valueChanged.connect(self.saturationSpinBox.setValue)
        self.saturationSpinBox.valueChanged.connect(self.saturationSlider.setValue)
        self.valueSlider.valueChanged.connect(self.valueSpinBox.setValue)
        self.valueSpinBox.valueChanged.connect(self.valueSlider.setValue)
        
        self.hueSpinBox.setValue(0)
        self.saturationSpinBox.setValue(255)
        self.valueSpinBox.setValue(255)
        
        self.layout.addStretch(1)

    def updateColor(self):
        hue = self.hueSlider.value()
        saturation = self.saturationSlider.value()
        value = self.valueSlider.value()
        color = QColor.fromHsv(hue, saturation, value)
        # the next line used to work, but now it doesn't? just keep it in case we need it later.
        # self.parent().colorPreview.setStyleSheet(f"background-color: {color.name()}")
        self.colorSelected.emit(color)

    colorSelected = pyqtSignal(QColor)

class RGBSliders(QWidget):
    def __init__(self, parent=None):
        super(RGBSliders, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.redSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.redSlider.setMaximum(255)
        self.redSlider.valueChanged.connect(self.updateColor)
        self.redSpinBox = QSpinBox(self)
        self.redSpinBox.setMinimum(0)
        self.redSpinBox.setMaximum(255)
        self.redSpinBox.setValue(255)

        self.greenSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.greenSlider.setMaximum(255)
        self.greenSlider.valueChanged.connect(self.updateColor)
        self.greenSpinBox = QSpinBox(self)
        self.greenSpinBox.setMinimum(0)
        self.greenSpinBox.setMaximum(255)
        self.greenSpinBox.setValue(255)

        self.blueSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.blueSlider.setMaximum(255)
        self.blueSlider.valueChanged.connect(self.updateColor)
        self.blueSpinBox = QSpinBox(self)
        self.blueSpinBox.setMinimum(0)
        self.blueSpinBox.setMaximum(255)
        self.blueSpinBox.setValue(255)

        self.layout.addWidget(QLabel("Red"))
        self.layout.addWidget(self.redSlider)
        self.layout.addWidget(self.redSpinBox)
        self.layout.addWidget(QLabel("Green"))
        self.layout.addWidget(self.greenSlider)
        self.layout.addWidget(self.greenSpinBox)
        self.layout.addWidget(QLabel("Blue"))
        self.layout.addWidget(self.blueSlider)
        self.layout.addWidget(self.blueSpinBox)
        
        self.redSlider.valueChanged.connect(self.redSpinBox.setValue)
        self.redSpinBox.valueChanged.connect(self.redSlider.setValue)
        self.greenSlider.valueChanged.connect(self.greenSpinBox.setValue)
        self.greenSpinBox.valueChanged.connect(self.greenSlider.setValue)
        self.blueSlider.valueChanged.connect(self.blueSpinBox.setValue)
        self.blueSpinBox.valueChanged.connect(self.blueSlider.setValue)
        
        self.layout.addStretch(1)

    def updateColor(self):
        red = self.redSlider.value()
        green = self.greenSlider.value()
        blue = self.blueSlider.value()
        color = QColor(red, green, blue)
        self.parent().colorPreview.setStyleSheet(f"background-color: {color.name()}")
        self.colorSelected.emit(color)

    colorSelected = pyqtSignal(QColor)

class ColorSliders(QWidget):
    def __init__(self, parent=None):
        super(ColorSliders, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # HSV and RGB Sliders
        self.hsvRgbLayout = QHBoxLayout()
        self.layout.addLayout(self.hsvRgbLayout)
        self.hsvSliders = HSVSliders(self)
        self.rgbSliders = RGBSliders(self)
        self.hsvRgbLayout.addWidget(self.hsvSliders)
        self.hsvRgbLayout.addWidget(self.rgbSliders)

        # HSV Colorspace Circle
        self.colorCircle = HSVColorSpaceCircle(self)
        self.layout.addWidget(self.colorCircle)
        self.layout.setAlignment(self.colorCircle, Qt.AlignmentFlag.AlignCenter)
        self.colorCircle.colorSelected.connect(self.setColor)

        # Color Preview
        self.colorPreview = QLabel(self)
        self.colorPreview.setFixedSize(QSize(100, 50))
        self.colorPreview.setAutoFillBackground(True)
        self.layout.addWidget(self.colorPreview)
        self.layout.setAlignment(self.colorPreview, Qt.AlignmentFlag.AlignCenter)

        self.hsvSliders.colorSelected.connect(self.updateFromHSV)
        self.rgbSliders.colorSelected.connect(self.updateFromRGB)
        
        self.updating = False
        
        self.hsvSliders.updateColor()
        self.rgbSliders.updateColor()
        
        self.layout.addStretch(1)
        
    def setColor(self, color):
        # Update HSV sliders
        self.hsvSliders.hueSlider.setValue(color.hue())
        self.hsvSliders.saturationSlider.setValue(color.saturation())
        self.hsvSliders.valueSlider.setValue(color.value())
        
        # Update RGB sliders
        self.rgbSliders.redSlider.setValue(color.red())
        self.rgbSliders.greenSlider.setValue(color.green())
        self.rgbSliders.blueSlider.setValue(color.blue())

    def updateFromHSV(self, color):
        if not self.updating:
            self.updating = True
            self.rgbSliders.redSlider.setValue(color.red())
            self.rgbSliders.greenSlider.setValue(color.green())
            self.rgbSliders.blueSlider.setValue(color.blue())
            self.updating = False
            
            self.colorCircle.hue = color.hue()
            self.colorCircle.saturation = color.saturation()
            self.colorCircle.value = color.value()
            self.colorCircle.update()

    def updateFromRGB(self, color):
        if not self.updating:
            self.updating = True
            self.hsvSliders.hueSlider.setValue(color.hue())
            self.hsvSliders.saturationSlider.setValue(color.saturation())
            self.hsvSliders.valueSlider.setValue(color.value())
            self.updating = False
            
            self.colorCircle.hue = color.hue()
            self.colorCircle.saturation = color.saturation()
            self.colorCircle.value = color.value()
            self.colorCircle.update()

class ColorItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        
        # Check if the item is selected
        if option.state & QStyle.StateFlag.State_Selected:
            # Set the color and width of the border
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            # Draw a rectangle around the item
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))

class ColorPalette(QWidget):
    def __init__(self, colorSliders, parent=None, presets=None):
        super(ColorPalette, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Store the colorSliders reference
        self.colorSliders = colorSliders

        # Define the sliders here
        
        self.colorList = NonDraggableListWidget(self)
        self.colorList.setDragDropMode(QListWidget.DragDropMode.NoDragDrop)
        self.colorList.setDragEnabled(False)
        self.colorList.setDragDropOverwriteMode(False)
        self.colorList.setViewMode(QListWidget.ViewMode.IconMode)
        self.colorList.setGridSize(QSize(60, 60))
        self.colorList.setFlow(QListWidget.Flow.LeftToRight)
        self.colorList.setWrapping(True)
        self.colorList.setSelectionMode(QListWidget.SelectionMode.SingleSelection)  # Set selection mode
        self.colorList.setItemDelegate(ColorItemDelegate(self.colorList))  # Set the custom delegate
        self.layout.addWidget(self.colorList)
        
        if presets:
            self.addPresetColors(presets)

        # Buttons layout
        self.buttonsLayout = QHBoxLayout()
        self.addColorButton = QPushButton("Add Selected Color", self)
        self.removeColorButton = QPushButton("Remove Color", self)
        self.buttonsLayout.addWidget(self.addColorButton)
        self.buttonsLayout.addWidget(self.removeColorButton)
        self.layout.addLayout(self.buttonsLayout)

        self.addColorButton.clicked.connect(self.addColor)
        self.removeColorButton.clicked.connect(self.removeColor)
        self.colorList.itemClicked.connect(self.updateSelectedColorAppearance)
        
        self.layout.addStretch(1)

    def updateSelectedColorAppearance(self, item):
        selected_color = item.background().color()
        
        # Update the color preview in the sliders widget
        self.colorSliders.colorPreview.setStyleSheet(f"background-color: {selected_color.name()}")
        
        # Update the sliders to match the selected color
        self.colorSliders.setColor(selected_color)

    def addColor(self):
        color = self.colorSliders.colorPreview.palette().color(QPalette.ColorRole.Window)
        item = QListWidgetItem()
        item.setBackground(color)
        item.setSizeHint(QSize(50, 50))
        self.colorList.addItem(item)
        
    def removeColor(self):
        currentRow = self.colorList.currentRow()
        if currentRow != -1:  # Check if a color is selected
            self.colorList.takeItem(currentRow)

    def getSelectedColor(self):
        item = self.colorList.currentItem()
        if item:
            return item.background().color()
        return None
    
    def updateSlidersAndPreview(self, item):
        selected_color = item.background().color()
        
        # Update the color preview in the sliders widget
        self.colorSliders.colorPreview.setStyleSheet(f"background-color: {selected_color.name()}")
        
        # Update the sliders to match the selected color
        self.colorSliders.setColor(selected_color)
        
    def addPresetColors(self, colors):
        for color in colors:
            item = QListWidgetItem()
            item.setBackground(QColor(color))
            item.setSizeHint(QSize(50, 50))
            self.colorList.addItem(item)

class HSVColorSpaceCircle(QWidget):
    colorSelected = pyqtSignal(QColor)
    
    def __init__(self, colorSliders, parent=None):
        super(HSVColorSpaceCircle, self).__init__(parent)
        self.hsvSliders = colorSliders.hsvSliders
        self.setFixedSize(220, 220)  # Set a fixed size for the widget
        self.hsvImage = self.generateHSVImage()

        # Connect the valueChanged signal of the value slider to the onValueSliderChanged method
        self.hsvSliders.valueSlider.valueChanged.connect(self.onValueSliderChanged)
        
    def onValueSliderChanged(self):
        self.hsvImage = self.generateHSVImage()
        self.update()

    def generateHSVImage(self):
        image = QImage(self.size(), QImage.Format.Format_ARGB32)
        image.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() / 2.0
        center_y = self.height() / 2.0
        max_radius = min(self.width(), self.height()) / 2.0 - 10

        for x in range(self.width()):
            for y in range(self.height()):
                dx = x - center_x
                dy = y - center_y
                distance_from_center = math.sqrt(dx**2 + dy**2)
                
                if distance_from_center <= max_radius:
                    hue = (math.degrees(math.atan2(dy, dx)) + 360) % 360
                    saturation = (distance_from_center / max_radius) * 255
                    value = self.hsvSliders.valueSlider.value()
                    color = QColor.fromHsv(int(hue), int(saturation), int(value))
                    painter.setPen(color)
                    painter.drawPoint(x, y)

        painter.end()
        return image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the pre-generated HSV image
        painter.drawImage(0, 0, self.hsvImage)

        # Draw the indicator for the current color
        center = QPoint(self.width() // 2, self.height() // 2)
        radius = min(self.width(), self.height()) // 2 - 10
        hue = self.hsvSliders.hueSlider.value()
        saturation = self.hsvSliders.saturationSlider.value() / 255.0
        indicator_radius = radius * saturation
        indicator_x = center.x() + indicator_radius * math.cos(math.radians(hue))
        indicator_y = center.y() + indicator_radius * math.sin(math.radians(hue))
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawEllipse(QPoint(round(indicator_x), round(indicator_y)), 5, 5)

        painter.end()

    def mousePressEvent(self, event):
        self.updateColorFromCircle(event.position().toPoint())

    def mouseMoveEvent(self, event):
        self.updateColorFromCircle(event.position().toPoint())

    def updateColorFromCircle(self, point):
        # Calculate hue and saturation from the point's position
        dx = point.x() - self.width() / 2
        dy = point.y() - self.height() / 2
        hue = (math.degrees(math.atan2(dy, dx)) + 360) % 360

        # Calculate the maximum possible distance (radius) taking into account the 10-pixel margin
        max_distance = min(self.width(), self.height()) / 2 - 10

        # Scale the actual distance to the range [0, 255] to get the saturation
        actual_distance = math.sqrt(dx**2 + dy**2)
        saturation = min(actual_distance / max_distance * 255, 255)

        # Update the HSV sliders
        self.hsvSliders.hueSlider.setValue(int(hue))
        self.hsvSliders.saturationSlider.setValue(int(saturation))

        # Emit the colorSelected signal
        color = QColor.fromHsv(int(hue), int(saturation), self.hsvSliders.valueSlider.value())
        self.colorSelected.emit(color)
        