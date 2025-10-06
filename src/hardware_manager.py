import threading
import time
from datetime import datetime
import os
from tkinter import messagebox
from pathlib import Path


class HardwareManager:
    def __init__(self, config_manager, ui_manager):
        self.config_manager = config_manager
        self.ui_manager = ui_manager
        self.is_collecting = False
        self.is_classifying = False
        self.collection_thread = None
        self.classification_thread = None
        self.image_count = 0
        self.classification_count = 0

    def start_collection_mode(self):
        """Start collection mode."""
        if self.is_classifying:
            messagebox.showwarning("Warning", "Please stop classification mode first")
            return

        self.is_collecting = True
        self.image_count = 0
        self.ui_manager.show_page("collection")
        self.collection_thread = threading.Thread(
            target=self.collection_loop, daemon=True
        )
        self.collection_thread.start()

    def stop_collection_mode(self):
        """Stop collection mode."""
        self.is_collecting = False
        if self.collection_thread and self.collection_thread.is_alive():
            self.collection_thread.join(timeout=1.0)
        self.ui_manager.show_page("main")

    def collection_loop(self):
        """Main loop for image collection mode."""
        collection_config = self.config_manager.get("collection", {})
        interval = collection_config.get("auto_capture_interval", 2.0)
        max_images = collection_config.get("images_per_session", 100)

        while self.is_collecting and self.image_count < max_images:
            self.simulate_image_capture()
            self.image_count += 1
            self.ui_manager.update_collection_count(self.image_count)

            if self.is_collecting:  # Check again before sleeping
                time.sleep(interval)

        # Auto-stop when session complete
        if self.is_collecting:
            self.stop_collection_mode()

    def simulate_image_capture(self):
        """Placeholder for capturing an image."""
        print(f"Simulating image capture {self.image_count + 1}")
        # TODO: Add actual camera capture logic here
        # This would interface with the camera hardware
        pass

    def start_classification_mode(self):
        """Start classification mode."""
        if self.is_collecting:
            messagebox.showwarning("Warning", "Please stop collection mode first")
            return

        # Check if model exists
        classification_config = self.config_manager.get("classification", {})
        model_path = Path(
            classification_config.get("model_path", "../models/pretrained/model.tflite")
        )

        if not model_path.exists():
            camera_config = self.config_manager.get("camera", {})
            width = camera_config.get("image_width", 224)
            height = camera_config.get("image_height", 224)
            messagebox.showerror(
                "Error",
                f"No trained model found!\n\nPlease:\n1. Collect images ({width}x{height})\n2. Train model\n3. Place model.tflite in models/pretrained/",
            )
            return

        self.is_classifying = True
        self.classification_count = 0
        self.ui_manager.show_page("classification")
        self.classification_thread = threading.Thread(
            target=self.classification_loop, daemon=True
        )
        self.classification_thread.start()

    def stop_classification_mode(self):
        """Stop classification mode."""
        self.is_classifying = False
        if self.classification_thread and self.classification_thread.is_alive():
            self.classification_thread.join(timeout=1.0)
        self.ui_manager.show_page("main")

    def classification_loop(self):
        """Main loop for classification mode."""
        classification_config = self.config_manager.get("classification", {})
        interval = classification_config.get("auto_classify_interval", 3.0)

        while self.is_classifying:
            self.simulate_classification()
            self.classification_count += 1
            self.ui_manager.update_classification_count(self.classification_count)

            if self.is_classifying:  # Check again before sleeping
                time.sleep(interval)

    def simulate_classification(self):
        """Placeholder for classifying an image."""
        print(f"Simulating image classification {self.classification_count + 1}")
        # TODO: Add actual classification logic here
        # This would capture, preprocess, and classify an image
        pass
