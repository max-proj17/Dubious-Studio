
import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QButtonGroup, QDockWidget, QColorDialog, QListWidget, QListWidgetItem, QGraphicsRectItem, QComboBox, QLabel, QSlider, QHBoxLayout, QStyledItemDelegate, QStyle, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor, QTransform, QBrush,  QPainterPath, QPainterPathStroker, QRadialGradient,  QPalette, QIcon, QImage
from PyQt6.QtCore import Qt, QPoint, QSize, QRectF, pyqtSignal, QPointF
import math

# For when/if we use the lib folder
# root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(root_folder)

# Needed for color palette
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
        self.eraserSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.eraserSlider.setMinimum(1)
        self.eraserSlider.setMaximum(20)
        self.layout.addWidget(QLabel("Eraser Size:"))
        self.layout.addWidget(self.eraserSlider)

        self.sizeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(20)
        self.layout.addWidget(QLabel("Size:"))
        self.layout.addWidget(self.sizeSlider)

        self.opacitySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacitySlider.setMinimum(1)
        self.opacitySlider.setMaximum(100)
        self.layout.addWidget(QLabel("Opacity:"))
        self.layout.addWidget(self.opacitySlider)
        
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
        
        #eraser slider
        self.eraserSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.eraserSlider.setMinimum(1)
        self.eraserSlider.setMaximum(20)
        self.layout.addWidget(QLabel("Eraser Size:"))
        self.layout.addWidget(self.eraserSlider)

        self.capStyleComboBox = QComboBox(self)
        self.capStyleComboBox.addItems(["Flat", "Square", "Round", "Tapered"])
        self.layout.addWidget(QLabel("Cap Style:"))
        self.layout.addWidget(self.capStyleComboBox)

        self.sizeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(20)
        self.layout.addWidget(QLabel("Size:"))
        self.layout.addWidget(self.sizeSlider)

        self.opacitySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacitySlider.setMinimum(1)
        self.opacitySlider.setMaximum(100)
        self.layout.addWidget(QLabel("Opacity:"))
        self.layout.addWidget(self.opacitySlider)
        
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
        
        self.capStyleComboBox = QComboBox(self)
        self.capStyleComboBox.addItems(["Flat", "Square", "Round", "Tapered"])
        self.layout.addWidget(QLabel("Cap Style:"))
        self.layout.addWidget(self.capStyleComboBox)

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


class DrawingCanvas(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(DrawingCanvas, self).__init__(scene, parent)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.isDrawing = False
        self.currentColor = QColor(Qt.GlobalColor.black)
        self.currentTool = "draw"

        self.currentEraserSize = 10

        self.currentSize = 1
        self.currentOpacity = 1.0
        self.currentCapStyle = Qt.PenCapStyle.FlatCap


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

    def setSize(self, size):
        self.currentSize = size

    def setOpacity(self, opacity):
        self.currentOpacity = opacity / 100.0

    def setCapStyle(self, capStyle):
        self.currentCapStyle = capStyle

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
        print("Mouse Pressed")
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
      
            self.endPoint = self.mapToScene(event.position().toPoint())
            
            pen = QPen(self.currentColor)

            
            if self.currentTool == "erase":
                pen.setColor(Qt.GlobalColor.white)
                pen.setWidth(self.currentEraserSize)  # Use the current eraser size
            self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y(), pen)

            color = QColor(self.currentColor)
            color.setAlphaF(self.currentOpacity)
            
            if self.currentCapStyle == "Tapered":
                path = QPainterPath(self.startPoint)
                path.lineTo(self.endPoint)
                distance = math.sqrt((self.startPoint.x() - self.endPoint.x())**2 + (self.startPoint.y() - self.endPoint.y())**2)
                segments = max(int(distance), 1)
                gradientPath = QPainterPath()
                for i in range(segments):
                    t = i / segments
                    p = path.pointAtPercent(t)
                    # Modified width calculation for sharper tapering
                    width = self.currentSize * (1 - (2*t - 1)**2)  
                    segmentStroker = QPainterPathStroker()
                    segmentStroker.setWidth(width)
                    segmentPath = QPainterPath(p)
                    segmentPath.lineTo(path.pointAtPercent((i + 1) / segments))
                    gradientPath.addPath(segmentStroker.createStroke(segmentPath))
                self.scene().addPath(gradientPath, QPen(color), QBrush(color))
            else:
                pen = QPen(color, self.currentSize)
                pen.setCapStyle(self.currentCapStyle)
                if self.currentTool == "erase":
                    pen.setColor(Qt.GlobalColor.white)
                    pen.setWidth(10)
                self.scene().addLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y(), pen)

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
        print("Mouse Released")
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

        # HSV and RGB sliders
        self.colorSliders = ColorSliders(self.sidebar)
        self.layout.addWidget(self.colorSliders)
        self.colorSliders.hsvSliders.colorSelected.connect(lambda color: self.canvas.setColor(color))
        self.colorSliders.rgbSliders.colorSelected.connect(lambda color: self.canvas.setColor(color))

        # Presets can be an array of any length of hex codes "#xxxxxx"
        presets = ["#5A5A5A", "#FFD1DC", "#A2CFFE", "#FFFFB3", "#B2FFB2", "#E6CCFF", "#FFDAB9", "#B5EAD7", "#FFB6B9"]
        self.colorPalette = ColorPalette(self.colorSliders, self.sidebar, presets=presets)
        self.layout.addWidget(self.colorPalette)

        # Tools
        self.tools = ["draw", "erase"]
        self.toolButtons = QButtonGroup(self.sidebar)
        for tool in self.tools:
            btn = QPushButton(tool.capitalize())
            btn.setCheckable(True)
            self.toolButtons.addButton(btn)
            self.layout.addWidget(btn)
            btn.clicked.connect(lambda checked, tool=tool: self.selectToolOrColor(tool))

        self.colorPalette.sizeSlider.valueChanged.connect(self.canvas.setSize)
        self.colorPalette.opacitySlider.valueChanged.connect(self.canvas.setOpacity)

        self.toolButtons.buttons()[0].setChecked(True)

        self.colorPalette.colorList.itemClicked.connect(
            lambda: self.canvas.setColor(self.colorPalette.getSelectedColor()))

        # Connect slider value changed signal to setEraserSize method
        self.colorPalette.eraserSlider.valueChanged.connect(self.canvas.setEraserSize)


        self.dock = QDockWidget("Tools", self)
        self.dock.setWidget(self.sidebar)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)


        self.setGeometry(100, 100, 1144, 1144)  # Adjust window size to accommodate the larger canvas
        self.setWindowIcon(QIcon("resources/icon.png"))
        self.setWindowTitle('Dubious Studio')
        self.show()


        self.colorPalette.capStyleComboBox.currentTextChanged.connect(self.setCapStyle)

    def setCapStyle(self, text):
        capStyles = {
            "Flat": Qt.PenCapStyle.FlatCap,
            "Square": Qt.PenCapStyle.SquareCap,
            "Round": Qt.PenCapStyle.RoundCap,
            "Tapered": "Tapered"
        }
        self.canvas.setCapStyle(capStyles.get(text, Qt.PenCapStyle.FlatCap))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawingApp()
    sys.exit(app.exec())
