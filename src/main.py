#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi Image Classifier - Factory Line Quality Control
Application Entry Point
"""

import tkinter as tk
from utils.config_manager import ConfigManager
from ui_manager import UIManager
from hardware_manager import HardwareManager


class Application:
    def __init__(self):
        """Initialize the application with proper separation of concerns."""
        # Initialize configuration
        self.config_manager = ConfigManager("../config.json")

        # Initialize root window
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Setup callbacks for UI events
        self.callbacks = {
            "start_collection": self.start_collection_mode,
            "stop_collection": self.stop_collection_mode,
            "start_classification": self.start_classification_mode,
            "stop_classification": self.stop_classification_mode,
            "show_settings": self.show_settings_page,
            "show_main": self.show_main_page,
            "exit": self.cleanup_and_exit,
        }

        # Initialize UI manager
        self.ui_manager = UIManager(self.root, self.config_manager, self.callbacks)

        # Initialize hardware manager
        self.hardware_manager = HardwareManager(self.config_manager, self.ui_manager)

        # Setup exit handling
        self.root.bind("<Control-Shift-Q>", self.show_exit_dialog)

        # Setup data directories
        self.setup_directories()

    def setup_directories(self):
        """Create necessary directories for data storage."""
        from pathlib import Path

        paths_config = self.config_manager.get("paths", {})

        self.images_dir = Path(paths_config["captured_images"])
        self.results_dir = Path(paths_config["classification_results"])
        self.data_dir = self.images_dir.parent

        self.data_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)

    # Callback methods for UI events
    def start_collection_mode(self):
        """Start collection mode."""
        self.hardware_manager.start_collection_mode()

    def stop_collection_mode(self):
        """Stop collection mode."""
        self.hardware_manager.stop_collection_mode()

    def start_classification_mode(self):
        """Start classification mode."""
        self.hardware_manager.start_classification_mode()

    def stop_classification_mode(self):
        """Stop classification mode."""
        self.hardware_manager.stop_classification_mode()

    def show_settings_page(self):
        """Navigate to settings page."""
        self.ui_manager.show_page("settings")

    def show_main_page(self):
        """Navigate to main page."""
        self.ui_manager.show_page("main")

    def show_exit_dialog(self, event):
        """Show exit confirmation dialog when Ctrl+Shift+Q is pressed."""
        from tkinter import messagebox

        result = messagebox.askyesno(
            "Exit", "Are you sure you want to exit the application?"
        )
        if result:
            self.cleanup_and_exit()

    def on_closing(self):
        """Handle window close event - prevent normal closing for factory use."""
        pass  # Do nothing - prevent accidental closing in factory environment

    def cleanup_and_exit(self):
        """Clean shutdown of the application."""
        self.hardware_manager.stop_collection_mode()
        self.hardware_manager.stop_classification_mode()
        self.root.destroy()

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()
