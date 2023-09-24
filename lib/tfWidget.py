import sys, os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt6.QtGui import QPixmap, QImage

class tfWidget(QWidget):
    def __init__(self):
        super(tfWidget, self).__init__()

        # Load the pre-trained style transfer model
        self.model_url = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
        self.model = hub.load(self.model_url)

        # Create UI components
        self.layout = QVBoxLayout(self)

        self.contentLabel = QLabel("Content Image:")
        self.contentLineEdit = QLineEdit()
        self.contentBrowseButton = QPushButton("Browse")
        self.contentBrowseButton.clicked.connect(self.browse_content_image)

        self.styleLabel = QLabel("Style Image:")
        self.styleLineEdit = QLineEdit()
        self.styleBrowseButton = QPushButton("Browse")
        self.styleBrowseButton.clicked.connect(self.browse_style_image)

        self.processButton = QPushButton("Apply Style Transfer")
        self.processButton.clicked.connect(self.process_image)

        self.outputLabel = QLabel("Stylized Image:")
        self.outputImageLabel = QLabel()

        # Add components to layout
        self.layout.addWidget(self.contentLabel)
        self.layout.addWidget(self.contentLineEdit)
        self.layout.addWidget(self.contentBrowseButton)
        self.layout.addWidget(self.styleLabel)
        self.layout.addWidget(self.styleLineEdit)
        self.layout.addWidget(self.styleBrowseButton)
        self.layout.addWidget(self.processButton)
        self.layout.addWidget(self.outputLabel)
        self.layout.addWidget(self.outputImageLabel)

        self.setLayout(self.layout)

    def browse_content_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Content Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if fname:
            self.contentLineEdit.setText(fname)

    def browse_style_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Style Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if fname:
            self.styleLineEdit.setText(fname)

    def load_image(self, img_path):
        img = tf.io.read_file(img_path)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.resize(img, [512, 512])
        img = img[tf.newaxis, :]
        return img / 255.0

    def process_image(self):
        content_image_path = self.contentLineEdit.text()
        style_image_path = self.styleLineEdit.text()

        content_image = self.load_image(content_image_path)
        style_image = self.load_image(style_image_path)

        stylized_image = self.model(tf.constant(content_image), tf.constant(style_image))[0]

        # Convert tensor to QImage
        stylized_image = tf.image.convert_image_dtype(stylized_image, dtype=tf.uint8)
        batch_size, height, width, channel = stylized_image.shape
        stylized_image = stylized_image[0]  # Take the first image from the batch
        bytesPerLine = 3 * width
        qImg = QImage(stylized_image.numpy().data, width, height, bytesPerLine, QImage.Format.Format_RGB888)

        # Display QImage in QLabel
        pixmap = QPixmap.fromImage(qImg)
        self.outputImageLabel.setPixmap(pixmap)