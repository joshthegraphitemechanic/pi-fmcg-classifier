import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(__file__).parent.parent / config_path
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load configuration settings from config.json in project root - REQUIRED, no defaults"""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(
                    f"config.json must be in project root. Expected: {self.config_path.absolute()}"
                )

            with open(self.config_path, "r") as f:
                self.config = json.load(f)

            self.validate_config()

        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror(
                "Configuration Error", f"Failed to load or validate config: {e}"
            )
            # Exit if config is invalid, as the app cannot run.
            exit()

    def validate_config(self):
        """Validate that all required sections and keys exist"""
        required_sections = [
            "camera",
            "collection",
            "classification",
            "ui",
            "paths",
            "sensors",
        ]
        missing_sections = [
            section for section in required_sections if section not in self.config
        ]
        if missing_sections:
            raise ValueError(f"Missing required config sections: {missing_sections}")

        required_keys = {
            "camera": ["image_width", "image_height", "capture_format", "quality"],
            "collection": [
                "trigger_mode",
                "auto_capture_interval",
                "images_per_session",
            ],
            "classification": [
                "model_path",
                "confidence_threshold",
                "auto_classify_interval",
            ],
            "ui": [
                "font_family",
                "base_screen",
                "font_sizes",
                "window_sizing",
                "colors",
            ],
            "paths": ["captured_images", "classification_results", "models", "logo"],
            "sensors": ["ir_sensor_pin", "voltage_threshold", "trigger_delay_ms"],
        }

        for section, keys in required_keys.items():
            if section not in self.config:
                continue
            missing_keys = [key for key in keys if key not in self.config[section]]
            if missing_keys:
                raise ValueError(
                    f"Missing required keys in [{section}]: {missing_keys}"
                )

    def get(self, section, default=None):
        return self.config.get(section, default)

    def save_config(self, new_config):
        """Save the updated configuration to config.json"""
        try:
            with open(self.config_path, "w") as f:
                json.dump(new_config, f, indent=4)
            self.config = new_config
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")
            return False

    def __getitem__(self, key):
        return self.config[key]
