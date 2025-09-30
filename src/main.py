#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi Image Classifier - Factory Line Quality Control
Fullscreen GUI for touchscreen operation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import os
from pathlib import Path


class FactoryLineGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Factory Line Quality Control")

        # For development - windowed mode. Change to fullscreen for Pi deployment
        # self.root.geometry("900x700")
        self.root.attributes("-fullscreen", True)  # Enable this for Pi
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # State variables
        self.is_collecting = False
        self.is_classifying = False
        self.image_count = 0
        self.classification_count = 0

        # Create data directories
        self.setup_directories()

        # Setup GUI
        self.setup_gui()

        # Status update thread
        self.update_thread_running = True
        self.status_thread = threading.Thread(
            target=self.update_status_loop, daemon=True
        )
        self.status_thread.start()

    def setup_directories(self):
        """Create necessary directories for data storage"""
        self.data_dir = Path("../data")
        self.images_dir = self.data_dir / "captured_images"
        self.results_dir = self.data_dir / "classification_results"

        self.data_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)

    def setup_styling(self):
        """Configure color scheme and styling"""
        # Define color palette
        self.colors = {
            "bg_dark": "#1e1e1e",
            "bg_medium": "#2d2d2d",
            "bg_light": "#3d3d3d",
            "text_white": "#ffffff",
            "text_gray": "#cccccc",
            "accent_blue": "#0078d4",
            "accent_green": "#107c10",
            "accent_red": "#d13438",
            "accent_orange": "#ff8c00",
            "button_active": "#005a9e",
            "button_hover": "#106ebe",
        }

    def setup_gui(self):
        """Setup the main GUI layout with enhanced styling"""
        # Configure colors and styling
        self.setup_styling()

        # Main container with dark background
        self.root.configure(bg="#1e1e1e")
        main_frame = tk.Frame(self.root, bg="#1e1e1e", padx=40, pady=30)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Title with enhanced styling
        title_label = tk.Label(
            main_frame,
            text="FACTORY LINE QUALITY CONTROL",
            font=("Arial", 32, "bold"),
            bg="#1e1e1e",
            fg="#ffffff",
            pady=20,
        )
        title_label.grid(
            row=0, column=0, columnspan=2, pady=(0, 40), sticky=(tk.W, tk.E)
        )

        # Status section
        self.setup_status_section(main_frame)

        # Control buttons section
        self.setup_control_section(main_frame)

        # Statistics section
        self.setup_stats_section(main_frame)

        # Exit button (hidden - Ctrl+Shift+Q to show)
        self.root.bind("<Control-Shift-Q>", self.show_exit_button)

    def setup_status_section(self, parent):
        """Setup status display section with enhanced styling"""
        status_frame = tk.LabelFrame(
            parent,
            text="SYSTEM STATUS",
            font=("Arial", 18, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_white"],
            bd=2,
            relief="ridge",
            padx=20,
            pady=15,
        )
        status_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 30), padx=10
        )
        status_frame.columnconfigure(1, weight=1)

        # Current mode with status indicator
        tk.Label(
            status_frame,
            text="Current Mode:",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_gray"],
        ).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.mode_label = tk.Label(
            status_frame,
            text="STANDBY",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent_blue"],
        )
        self.mode_label.grid(row=0, column=1, sticky=tk.W, padx=(20, 0), pady=10)

        # System time
        tk.Label(
            status_frame,
            text="System Time:",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_gray"],
        ).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.time_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 16),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_white"],
        )
        self.time_label.grid(row=1, column=1, sticky=tk.W, padx=(20, 0), pady=10)

        # Sensor status with indicator
        tk.Label(
            status_frame,
            text="IR Sensor:",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_gray"],
        ).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.sensor_label = tk.Label(
            status_frame,
            text="NOT CONNECTED",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent_red"],
        )
        self.sensor_label.grid(row=2, column=1, sticky=tk.W, padx=(20, 0), pady=10)

    def setup_control_section(self, parent):
        """Setup control buttons section with large, factory-appropriate buttons"""
        control_frame = tk.LabelFrame(
            parent,
            text="CONTROLS",
            font=("Arial", 18, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_white"],
            bd=2,
            relief="ridge",
            padx=20,
            pady=15,
        )
        control_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 30), padx=10
        )
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)

        # Large Collection mode button
        self.collect_button = tk.Button(
            control_frame,
            text="START\nCOLLECTION\nMODE",
            command=self.toggle_collection,
            font=("Arial", 16, "bold"),
            bg=self.colors["accent_green"],
            fg=self.colors["text_white"],
            activebackground=self.colors["button_active"],
            activeforeground=self.colors["text_white"],
            relief="raised",
            bd=3,
            height=4,
            width=15,
        )
        self.collect_button.grid(row=0, column=0, padx=15, pady=15, sticky=(tk.W, tk.E))

        # Large Classification mode button
        self.classify_button = tk.Button(
            control_frame,
            text="START\nCLASSIFICATION\nMODE",
            command=self.toggle_classification,
            font=("Arial", 16, "bold"),
            bg=self.colors["accent_blue"],
            fg=self.colors["text_white"],
            activebackground=self.colors["button_active"],
            activeforeground=self.colors["text_white"],
            relief="raised",
            bd=3,
            height=4,
            width=15,
        )
        self.classify_button.grid(
            row=0, column=1, padx=15, pady=15, sticky=(tk.W, tk.E)
        )

        # Export data button
        export_button = tk.Button(
            control_frame,
            text="EXPORT\nDATA",
            command=self.export_data,
            font=("Arial", 14, "bold"),
            bg=self.colors["accent_orange"],
            fg=self.colors["text_white"],
            activebackground=self.colors["button_active"],
            activeforeground=self.colors["text_white"],
            relief="raised",
            bd=2,
            height=3,
            width=12,
        )
        export_button.grid(row=1, column=0, padx=15, pady=(0, 15), sticky=(tk.W, tk.E))

        # Settings button
        settings_button = tk.Button(
            control_frame,
            text="SETTINGS",
            command=self.open_settings,
            font=("Arial", 14, "bold"),
            bg=self.colors["bg_light"],
            fg=self.colors["text_white"],
            activebackground=self.colors["button_active"],
            activeforeground=self.colors["text_white"],
            relief="raised",
            bd=2,
            height=3,
            width=12,
        )
        settings_button.grid(
            row=1, column=1, padx=15, pady=(0, 15), sticky=(tk.W, tk.E)
        )

    def setup_stats_section(self, parent):
        """Setup statistics display section with enhanced styling"""
        stats_frame = tk.LabelFrame(
            parent,
            text="STATISTICS",
            font=("Arial", 18, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_white"],
            bd=2,
            relief="ridge",
            padx=20,
            pady=15,
        )
        stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(3, weight=1)

        # Images collected
        tk.Label(
            stats_frame,
            text="Images Collected:",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_gray"],
        ).grid(row=0, column=0, sticky=tk.W, pady=15)
        self.images_count_label = tk.Label(
            stats_frame,
            text="0",
            font=("Arial", 20, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent_green"],
        )
        self.images_count_label.grid(
            row=0, column=1, sticky=tk.W, padx=(20, 40), pady=15
        )

        # Classifications made
        tk.Label(
            stats_frame,
            text="Classifications Made:",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_gray"],
        ).grid(row=0, column=2, sticky=tk.W, pady=15)
        self.classifications_count_label = tk.Label(
            stats_frame,
            text="0",
            font=("Arial", 20, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent_blue"],
        )
        self.classifications_count_label.grid(
            row=0, column=3, sticky=tk.W, padx=(20, 0), pady=15
        )

        # Session start time
        tk.Label(
            stats_frame,
            text="Session Started:",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_gray"],
        ).grid(row=1, column=0, sticky=tk.W, pady=(0, 15))
        self.session_start_label = tk.Label(
            stats_frame,
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            font=("Arial", 14),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_white"],
        )
        self.session_start_label.grid(
            row=1, column=1, columnspan=3, sticky=tk.W, padx=(20, 0), pady=(0, 15)
        )

    def toggle_collection(self):
        """Toggle collection mode on/off"""
        if self.is_collecting:
            self.stop_collection()
        else:
            self.start_collection()

    def start_collection(self):
        """Start image collection mode"""
        if self.is_classifying:
            messagebox.showwarning("Warning", "Please stop classification mode first")
            return

        self.is_collecting = True
        self.collect_button.config(
            text="STOP\nCOLLECTION", bg=self.colors["accent_red"]
        )
        self.mode_label.config(text="COLLECTING IMAGES", fg=self.colors["accent_green"])

        # Start collection thread
        self.collection_thread = threading.Thread(
            target=self.collection_loop, daemon=True
        )
        self.collection_thread.start()

    def stop_collection(self):
        """Stop image collection mode"""
        self.is_collecting = False
        self.collect_button.config(
            text="START\nCOLLECTION\nMODE", bg=self.colors["accent_green"]
        )
        self.mode_label.config(text="STANDBY", fg=self.colors["accent_blue"])

    def toggle_classification(self):
        """Toggle classification mode on/off"""
        if self.is_classifying:
            self.stop_classification()
        else:
            self.start_classification()

    def start_classification(self):
        """Start image classification mode"""
        if self.is_collecting:
            messagebox.showwarning("Warning", "Please stop collection mode first")
            return

        # Check if model exists
        model_path = Path("../models/pretrained/model.tflite")
        if not model_path.exists():
            messagebox.showerror(
                "Error",
                "No trained model found!\n\nPlease:\n1. Collect images\n2. Train model using Liner.ai\n3. Place model.tflite in models/pretrained/",
            )
            return

        self.is_classifying = True
        self.classify_button.config(
            text="STOP\nCLASSIFICATION", bg=self.colors["accent_red"]
        )
        self.mode_label.config(
            text="CLASSIFYING IMAGES", fg=self.colors["accent_orange"]
        )

        # Start classification thread
        self.classification_thread = threading.Thread(
            target=self.classification_loop, daemon=True
        )
        self.classification_thread.start()

    def stop_classification(self):
        """Stop image classification mode"""
        self.is_classifying = False
        self.classify_button.config(
            text="START\nCLASSIFICATION\nMODE", bg=self.colors["accent_blue"]
        )
        self.mode_label.config(text="STANDBY", fg=self.colors["accent_blue"])

    def collection_loop(self):
        """Main collection loop - runs in separate thread"""
        while self.is_collecting:
            # TODO: Check IR sensor for object detection
            # For now, simulate with a timer
            time.sleep(2)  # Simulate 2-second interval for testing

            if self.is_collecting:  # Check again in case it was stopped
                # TODO: Capture image with camera
                self.simulate_image_capture()

    def classification_loop(self):
        """Main classification loop - runs in separate thread"""
        while self.is_classifying:
            # TODO: Check IR sensor for object detection
            # For now, simulate with a timer
            time.sleep(3)  # Simulate 3-second interval for testing

            if self.is_classifying:  # Check again in case it was stopped
                # TODO: Capture and classify image
                self.simulate_classification()

    def simulate_image_capture(self):
        """Simulate capturing an image (placeholder for real camera)"""
        self.image_count += 1
        print(f"Image captured: {self.image_count}")

    def simulate_classification(self):
        """Simulate classifying an image (placeholder for real classifier)"""
        self.classification_count += 1
        print(f"Image classified: {self.classification_count}")

    def export_data(self):
        """Export collected data to USB or network location"""
        messagebox.showinfo(
            "Export",
            "Data export functionality will be implemented here.\n\nWill include:\n- All captured images\n- Classification results CSV\n- Session statistics",
        )

    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo(
            "Settings",
            "Settings panel will be implemented here.\n\nWill include:\n- IR sensor distance threshold\n- Camera settings\n- Export locations\n- Calibration options",
        )

    def update_status_loop(self):
        """Update status information periodically"""
        while self.update_thread_running:
            # Update time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.config(text=current_time)

            # Update counts
            self.images_count_label.config(text=str(self.image_count))
            self.classifications_count_label.config(text=str(self.classification_count))

            # TODO: Update sensor status

            time.sleep(1)

    def show_exit_button(self, event):
        """Show exit button when Ctrl+Shift+Q is pressed"""
        result = messagebox.askyesno(
            "Exit", "Are you sure you want to exit the application?"
        )
        if result:
            self.cleanup_and_exit()

    def on_closing(self):
        """Handle window close event - prevent normal closing for factory use"""
        pass  # Do nothing - prevent accidental closing in factory environment

    def cleanup_and_exit(self):
        """Clean shutdown of the application"""
        self.is_collecting = False
        self.is_classifying = False
        self.update_thread_running = False
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = FactoryLineGUI()
    app.run()
