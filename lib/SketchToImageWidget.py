import sys
import os
import time
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDir, QThread, pyqtSignal
from dotenv import load_dotenv

#####################################
# Each GAIT from ClipDrop and OpenAI
# Needs to Have
# 1. A ImageProcessingThread
# 2. A tool process class that can be modular with AIWidget
######################################
class ImageProcessingThread(QThread):
    finished_signal = pyqtSignal(dict)  # Signal to emit the result of the processing
    
    def __init__(self, image_path, stablexl_key, prompt):
        super().__init__()
        self.image_path = image_path
        self.stablexl_key = stablexl_key
        self.prompt = prompt
        
    def run(self):
        # Perform the image processing here
        result = {}
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
      
        
        url = "https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image"
        headers = {"x-api-key": self.stablexl_key}
        
        old_image_name = os.path.basename(self.image_path)
        
        with open(self.image_path, 'rb') as image_file:
            files = {'sketch_file': (old_image_name, image_file, 'image/png')}
            data = {'prompt': self.prompt}
            response = requests.post(url, headers=headers, files=files, data=data)
    
        if response.status_code == 200:
            timestamp = int(time.time())
            new_image_name = f'new_image_{timestamp}.jpg'
            new_image_path = os.path.join(desktop_path, new_image_name)
            
            with open(new_image_path, 'wb') as new_image_file:
                new_image_file.write(response.content)
            
            result['new_image_path'] = new_image_path
        else:
            result['error'] = f"API Response: {response.status_code}, {response.text}"
        
        self.finished_signal.emit(result)
        
class SketchToImageWidget(QWidget):
    def __init__(self, stablexl_key):
        super().__init__()
        self.stablexl_key = stablexl_key  # Store the API key
        # Initialize UI components for Sketch to Image tool
        self.init_ui()
        
    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create upload button
        self.upload_btn = QPushButton('Upload Image')
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn)

        # Create prompt input field
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter prompt describing the content to generate")
        layout.addWidget(self.prompt_input)
        
        # Create process button
        self.process_btn = QPushButton('Process Image')
        self.process_btn.clicked.connect(self.process_image)
        layout.addWidget(self.process_btn)

        # Create image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # Set layout
        self.setLayout(layout)
        
    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', QDir.homePath(), 'Images (*.png)')
        if file_name:
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
            self.current_image_path = file_name
            
    def process_image(self):
        print("Processing image...")
        prompt = self.prompt_input.text().strip()
        if hasattr(self, 'current_image_path') and self.stablexl_key:
            self.processing_thread = ImageProcessingThread(self.current_image_path, self.stablexl_key, prompt)
            self.processing_thread.finished_signal.connect(self.on_image_processed)
            self.processing_thread.start()
            
    def on_image_processed(self, result):
        if 'new_image_path' in result:
            pixmap = QPixmap(result['new_image_path'])
            scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
            self.current_image_path = result['new_image_path']
        elif 'error' in result:
            print(f"Error: Unable to process image. {result['error']}")