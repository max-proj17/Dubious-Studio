import sys
import os
import time
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDir, QThread, pyqtSignal
from dotenv import load_dotenv


class TextToImageProcessingThread(QThread):
    finished_signal = pyqtSignal(dict)  # Signal to emit the result of the processing
    
    def __init__(self, stablexl_key, prompt):
        super().__init__()
        self.stablexl_key = stablexl_key
        self.prompt = prompt
        
    def run(self):
        # Perform the image processing here
        result = {}
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        url = "https://clipdrop-api.co/text-to-image/v1"
        headers = {"x-api-key": self.stablexl_key}
        
        files = {
            'prompt': (None, self.prompt, 'text/plain')
        }
        
        response = requests.post(url, headers=headers, files=files)
        
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

        
class TextToImageWidget(QWidget):
    def __init__(self, stablexl_key):
        super().__init__()
        self.stablexl_key = stablexl_key  # Store the API key
        # Initialize UI components for Text to Image tool
        self.init_ui()
        
    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create prompt input field
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter prompt describing the content to generate")
        layout.addWidget(self.prompt_input)
        
        # Create process button
        self.process_btn = QPushButton('Generate Image')
        self.process_btn.clicked.connect(self.process_image)
        layout.addWidget(self.process_btn)

        # Create image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # Set layout
        self.setLayout(layout)
            
    def process_image(self):
        print("Generating image...")
        prompt = self.prompt_input.text().strip()
        if self.stablexl_key:
            self.processing_thread = TextToImageProcessingThread(self.stablexl_key, prompt)
            self.processing_thread.finished_signal.connect(self.on_image_processed)
            self.processing_thread.start()
            
    def on_image_processed(self, result):
        if 'new_image_path' in result:
            pixmap = QPixmap(result['new_image_path'])
            scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
        elif 'error' in result:
            print(f"Error: Unable to generate image. {result['error']}")
