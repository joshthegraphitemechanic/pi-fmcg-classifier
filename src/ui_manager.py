import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime


class UIManager:
    def __init__(self, root, config_manager, app_callbacks):
        self.root = root
        self.config_manager = config_manager
        self.app_callbacks = app_callbacks
        self.config = self.config_manager.config
        self.colors = self.config["ui"]["colors"]
        self.font_family = self.config["ui"]["font_family"]
        self.fonts = {}
        self.pages = {}
        self.config_entries = {}

        self.setup_styling()
        self.calculate_responsive_fonts()
        self.setup_gui()

    def setup_styling(self):
        """Set up the application's color scheme and styles."""
        self.root.configure(bg=self.colors["bg_main"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.colors["bg_main"])
        style.configure(
            "TLabel",
            background=self.colors["bg_main"],
            foreground=self.colors["text_main"],
        )
        style.configure(
            "TButton",
            background=self.colors["btn_primary"],
            foreground=self.colors["text_white"],
        )
        style.map("TButton", background=[("active", self.colors["btn_primary_dark"])])

    def calculate_responsive_fonts(self):
        """Calculate font sizes based on screen dimensions."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        base_screen = self.config["ui"]["base_screen"]
        base_width = base_screen["width"]
        base_height = base_screen["height"]

        # Calculate scaling factors
        width_scale = screen_width / base_width
        height_scale = screen_height / base_height
        scale_factor = min(
            width_scale, height_scale
        )  # Use smaller scale to ensure everything fits

        font_sizes = self.config["ui"]["font_sizes"]
        self.fonts = {}

        for font_type, font_config in font_sizes.items():
            base_size = font_config["base"]
            min_size = font_config["minimum"]
            scaled_size = max(min_size, int(base_size * scale_factor))
            self.fonts[font_type] = scaled_size

        print(f"Screen: {screen_width}x{screen_height}, Scale: {scale_factor:.2f}")
        print(f"Font sizes: {self.fonts}")

    def setup_gui(self):
        """Set up the main GUI layout and pages."""
        self.root.title("Factory Line Quality Control")

        # Always fullscreen for factory environment
        self.root.attributes("-fullscreen", True)

        self.main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.setup_main_page()
        self.setup_collection_page()
        self.setup_classification_page()
        self.setup_settings_page()

        self.show_page("main")

    def show_page(self, page_name):
        """Show the specified page and hide others."""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)

    def setup_main_page(self):
        """Setup the main page with collection, classification, and settings buttons."""
        page = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.pages["main"] = page

        # Header with title
        header_frame = tk.Frame(page, bg=self.colors["primary"], height=120)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="FACTORY LINE QUALITY CONTROL",
            font=(self.font_family, self.fonts.get("title", 24), "bold"),
            bg=self.colors["primary"],
            fg=self.colors["text_white"],
        )
        title_label.pack(expand=True)

        # Main buttons frame
        buttons_frame = tk.Frame(page, bg=self.colors["bg_main"])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Configure grid
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.rowconfigure(0, weight=4)
        buttons_frame.rowconfigure(1, weight=1)

        # Collection Mode Button
        collection_btn = tk.Button(
            buttons_frame,
            text="START\nCOLLECTION\nMODE",
            command=self.app_callbacks["start_collection"],
            font=(self.font_family, self.fonts.get("button_main", 16), "bold"),
            bg=self.colors["btn_collection"],
            fg=self.colors["text_white"],
            relief="raised",
            bd=5,
            cursor="hand2",
        )
        collection_btn.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Classification Mode Button
        classification_btn = tk.Button(
            buttons_frame,
            text="START\nCLASSIFICATION\nMODE",
            command=self.app_callbacks["start_classification"],
            font=(self.font_family, self.fonts.get("button_main", 16), "bold"),
            bg=self.colors["btn_classification"],
            fg=self.colors["text_white"],
            relief="raised",
            bd=5,
            cursor="hand2",
        )
        classification_btn.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        # Settings Button
        settings_btn = tk.Button(
            buttons_frame,
            text="[SETTINGS]",
            command=self.app_callbacks["show_settings"],
            font=(self.font_family, self.fonts.get("button_secondary", 14), "bold"),
            bg=self.colors["btn_secondary"],
            fg=self.colors["text_white"],
            relief="raised",
            bd=4,
            cursor="hand2",
        )
        settings_btn.grid(row=1, column=0, columnspan=2, padx=15, pady=15, sticky="ew")

    def setup_collection_page(self):
        """Setup the collection mode page with live stats and stop button."""
        page = tk.Frame(self.main_container, bg=self.colors["bg_white"])
        self.pages["collection"] = page

        # Header
        header_frame = tk.Frame(page, bg=self.colors["success"], height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="[COLLECTION MODE ACTIVE]",
            font=(self.font_family, self.fonts.get("title", 24), "bold"),
            bg=self.colors["success"],
            fg=self.colors["text_white"],
        )
        title_label.pack(expand=True)

        # Status frame
        status_frame = tk.LabelFrame(
            page,
            text="[LIVE STATISTICS]",
            font=(self.font_family, self.fonts.get("label_large", 18), "bold"),
            bg=self.colors["bg_panel"],
            fg=self.colors["text_dark"],
            bd=3,
            relief="groove",
            padx=20,
            pady=15,
        )
        status_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=(0, 30))

        # Images collected counter
        tk.Label(
            status_frame,
            text="Images Collected:",
            font=(self.font_family, self.fonts.get("label_large", 18), "bold"),
            bg=self.colors["bg_panel"],
            fg=self.colors["text_dark"],
        ).pack(pady=20)

        self.collection_count_label = tk.Label(
            status_frame,
            text="0",
            font=(self.font_family, 48, "bold"),
            bg=self.colors["bg_panel"],
            fg=self.colors["btn_collection"],
        )
        self.collection_count_label.pack(pady=20)

        # Stop button
        stop_btn = tk.Button(
            page,
            text="[STOP COLLECTION]",
            command=self.app_callbacks["stop_collection"],
            font=(self.font_family, self.fonts.get("button_secondary", 14), "bold"),
            bg=self.colors["btn_danger"],
            fg=self.colors["text_white"],
            relief="raised",
            bd=4,
            height=3,
            width=20,
            cursor="hand2",
        )
        stop_btn.pack(pady=20)

    def setup_classification_page(self):
        """Setup the classification mode page with live stats and stop button."""
        page = tk.Frame(self.main_container, bg=self.colors["bg_white"])
        self.pages["classification"] = page

        # Header
        header_frame = tk.Frame(page, bg=self.colors["info"], height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="[CLASSIFICATION MODE ACTIVE]",
            font=(self.font_family, self.fonts.get("title", 24), "bold"),
            bg=self.colors["info"],
            fg=self.colors["text_white"],
        )
        title_label.pack(expand=True)

        # Status frame
        status_frame = tk.LabelFrame(
            page,
            text="[LIVE STATISTICS]",
            font=(self.font_family, self.fonts.get("label_large", 18), "bold"),
            bg=self.colors["bg_panel"],
            fg=self.colors["text_dark"],
            bd=3,
            relief="groove",
            padx=20,
            pady=15,
        )
        status_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=(0, 30))

        # Classifications made counter
        tk.Label(
            status_frame,
            text="Classifications Made:",
            font=(self.font_family, self.fonts.get("label_large", 18), "bold"),
            bg=self.colors["bg_panel"],
            fg=self.colors["text_dark"],
        ).pack(pady=20)

        self.classification_count_label = tk.Label(
            status_frame,
            text="0",
            font=(self.font_family, 48, "bold"),
            bg=self.colors["bg_panel"],
            fg=self.colors["btn_classification"],
        )
        self.classification_count_label.pack(pady=20)

        # Stop button
        stop_btn = tk.Button(
            page,
            text="[STOP CLASSIFICATION]",
            command=self.app_callbacks["stop_classification"],
            font=(self.font_family, self.fonts.get("button_secondary", 14), "bold"),
            bg=self.colors["btn_danger"],
            fg=self.colors["text_white"],
            relief="raised",
            bd=4,
            height=3,
            width=20,
            cursor="hand2",
        )
        stop_btn.pack(pady=20)

    def setup_settings_page(self):
        """Setup the settings page with editable config values."""
        page = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.pages["settings"] = page

        # Header
        header_frame = tk.Frame(page, bg=self.colors["secondary"], height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="[SYSTEM SETTINGS]",
            font=(self.font_family, self.fonts.get("title", 24), "bold"),
            bg=self.colors["secondary"],
            fg=self.colors["text_white"],
        )
        title_label.pack(expand=True)

        # Main content area
        main_frame = tk.Frame(page, bg=self.colors["bg_main"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create scrollable frame
        canvas = tk.Canvas(main_frame, bg=self.colors["bg_main"])
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_main"])

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Settings sections
        self.create_settings_section(
            scrollable_frame,
            "Camera Settings",
            "camera",
            [
                ("Image Width", "image_width"),
                ("Image Height", "image_height"),
                ("Capture Format", "capture_format"),
                ("Quality", "quality"),
            ],
        )

        self.create_settings_section(
            scrollable_frame,
            "Collection Settings",
            "collection",
            [
                ("Trigger Mode", "trigger_mode"),
                ("Auto Capture Interval (sec)", "auto_capture_interval"),
                ("Images Per Session", "images_per_session"),
            ],
        )

        self.create_settings_section(
            scrollable_frame,
            "Classification Settings",
            "classification",
            [
                ("Model Path", "model_path"),
                ("Confidence Threshold", "confidence_threshold"),
                ("Auto Classify Interval (sec)", "auto_classify_interval"),
            ],
        )

        # Control buttons
        button_frame = tk.Frame(page, bg=self.colors["bg_main"])
        button_frame.pack(fill=tk.X, pady=20)

        save_btn = tk.Button(
            button_frame,
            text="[SAVE SETTINGS]",
            command=self.save_settings,
            font=(self.font_family, self.fonts.get("button_secondary", 14), "bold"),
            bg=self.colors["success"],
            fg=self.colors["text_white"],
            relief="raised",
            bd=4,
            cursor="hand2",
        )
        save_btn.pack(side=tk.LEFT, padx=(20, 10), pady=10)

        back_btn = tk.Button(
            button_frame,
            text="[BACK TO MAIN]",
            command=self.app_callbacks["show_main"],
            font=(self.font_family, self.fonts.get("button_secondary", 14), "bold"),
            bg=self.colors["btn_secondary"],
            fg=self.colors["text_white"],
            relief="raised",
            bd=4,
            cursor="hand2",
        )
        back_btn.pack(side=tk.RIGHT, padx=(10, 20), pady=10)

    def create_settings_section(self, parent, title, config_section, fields):
        """Create a settings section with labeled entry fields."""
        section_frame = tk.LabelFrame(
            parent,
            text=f"[{title.upper()}]",
            font=(self.font_family, self.fonts.get("label_large", 16), "bold"),
            bg=self.colors["bg_panel"],
            fg=self.colors["text_dark"],
            bd=2,
            relief="groove",
            padx=15,
            pady=10,
        )
        section_frame.pack(fill=tk.X, padx=20, pady=10)

        # Grid configuration
        section_frame.columnconfigure(1, weight=1)

        # Initialize section in config_entries if not exists
        if config_section not in self.config_entries:
            self.config_entries[config_section] = {}

        # Create fields
        for i, (label, key) in enumerate(fields):
            # Label
            tk.Label(
                section_frame,
                text=f"{label}:",
                font=(self.font_family, self.fonts.get("label_medium", 12)),
                bg=self.colors["bg_panel"],
                fg=self.colors["text_dark"],
                anchor="w",
            ).grid(row=i, column=0, sticky="w", padx=(10, 20), pady=5)

            # Entry widget
            entry = tk.Entry(
                section_frame,
                font=(self.font_family, self.fonts.get("label_medium", 12)),
                bg=self.colors["bg_white"],
                fg=self.colors["text_dark"],
                relief="solid",
                bd=1,
                width=30,
            )
            entry.grid(row=i, column=1, sticky="ew", padx=(0, 10), pady=5)

            # Store reference and set current value
            self.config_entries[config_section][key] = entry
            current_value = self.config.get(config_section, {}).get(key, "")
            entry.insert(0, str(current_value))

    def save_settings(self):
        """Save the current settings from the UI to the config file."""
        new_config = self.config_manager.config.copy()

        for section, fields in self.config_entries.items():
            if section not in new_config:
                new_config[section] = {}
            for field, widget in fields.items():
                value = self.get_entry_value(
                    widget, type(new_config[section].get(field, ""))
                )
                new_config[section][field] = value

        if self.config_manager.save_config(new_config):
            messagebox.showinfo(
                "Success",
                "Settings saved successfully. Please restart the application for changes to take effect.",
            )
        else:
            messagebox.showerror("Error", "Failed to save settings.")

    def get_entry_value(self, widget, field_type):
        """Get value from a settings entry widget, converting to the correct type."""
        value = widget.get()
        try:
            if field_type == int:
                return int(value)
            elif field_type == float:
                return float(value)
            elif field_type == bool:
                return value.lower() in ("true", "1", "yes", "on")
            else:
                return value
        except (ValueError, TypeError):
            return value

    def update_collection_count(self, count):
        """Update the collection count display (thread-safe)."""
        if hasattr(self, "collection_count_label"):
            self.root.after(
                0, lambda: self.collection_count_label.config(text=str(count))
            )

    def update_classification_count(self, count):
        """Update the classification count display (thread-safe)."""
        if hasattr(self, "classification_count_label"):
            self.root.after(
                0, lambda: self.classification_count_label.config(text=str(count))
            )
