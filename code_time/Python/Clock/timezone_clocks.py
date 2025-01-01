import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from zoneinfo import ZoneInfo
import pytz
import math
import json
import os
import threading
import time
import traceback

# ------------------ CONSTANTS & LOCALIZATION ------------------ #

LOCALIZATION = {
    "en": {
        "app_title": "World Timezone Clocks",
        "search_label": "Search Timezone:",
        "favorites_label": "Favorite Timezones:",
        "no_selection_warning": "Please select a timezone from the list.",
        "invalid_selection_warning": "Please select a specific timezone, not a region.",
        "digital_clock": "Digital Clock",
        "analog_clock": "Analog Clock",
        "earth_clock": "Earth Clock",
        "show_hide_dark_mode": "Toggle Dark Mode",
        "load_favorite": "Load Favorite",
        "save_favorite": "Save Favorite",
        "region_timezone": "Timezone",
        "countries_column": "Countries",
        "utc_offset": "UTC Offset",
        "dst": "DST",
        "date": "Date",
        "error_title": "Error",
        "info_title": "Information",
        "warning_title": "Warning",
        "save_favorite_success": "Favorite timezone saved successfully.",
        "load_favorite_success": "Favorite timezone loaded successfully.",
        "save_favorite_fail": "Failed to save favorite timezone.",
        "load_favorite_fail": "Failed to load favorite timezone.",
    },
    "es": {
        "app_title": "Relojes de Zonas Horarias",
        "search_label": "Buscar Zona Horaria:",
        "favorites_label": "Zonas Favoritas:",
        "no_selection_warning": "Por favor seleccione una zona horaria de la lista.",
        "invalid_selection_warning": "Seleccione una zona específica, no solo la región.",
        "digital_clock": "Reloj Digital",
        "analog_clock": "Reloj Analógico",
        "earth_clock": "Reloj Terrestre",
        "show_hide_dark_mode": "Cambiar Modo Oscuro",
        "load_favorite": "Cargar Favorito",
        "save_favorite": "Guardar Favorito",
        "region_timezone": "Zona Horaria",
        "countries_column": "Países",
        "utc_offset": "UTC",
        "dst": "Horario de Verano",
        "date": "Fecha",
        "error_title": "Error",
        "info_title": "Información",
        "warning_title": "Advertencia",
        "save_favorite_success": "Zona horaria favorita guardada exitosamente.",
        "load_favorite_success": "Zona horaria favorita cargada exitosamente.",
        "save_favorite_fail": "Error al guardar la zona horaria favorita.",
        "load_favorite_fail": "Error al cargar la zona horaria favorita.",
    }
}

CURRENT_LANG = "en"  # Switch to "es" for Spanish, or implement a language selector

# ------------------ DARK MODE THEMES ------------------ #

LIGHT_BG = "#F0F0F0"
LIGHT_FG = "#000000"
DARK_BG = "#2E2E2E"
DARK_FG = "#FFFFFF"

# ------------------ HELPER FUNCTIONS ------------------ #

def get_localized_text(key: str) -> str:
    """Retrieve a localized string from LOCALIZATION based on CURRENT_LANG."""
    return LOCALIZATION.get(CURRENT_LANG, LOCALIZATION["en"]).get(key, key)

def load_session():
    """Load user session data from session.json if it exists."""
    try:
        if os.path.exists("session.json"):
            with open("session.json", "r", encoding="utf-8") as file:
                return json.load(file)
    except Exception as e:
        print(f"Error loading session: {e}")
    return {}

def save_session(data: dict):
    """Save user session data to session.json."""
    try:
        with open("session.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving session: {e}")

# ------------------ TIMEZONE & GROUPING ------------------ #

def get_timezones_grouped():
    """
    Retrieves all timezones, groups them by their region, 
    and maps them to the countries that observe them.
    """
    grouped_timezones = {}
    try:
        for tz in pytz.all_timezones:
            if '/' in tz:
                region, city = tz.split('/', 1)
            else:
                region = 'Other'
                city = tz
            if region not in grouped_timezones:
                grouped_timezones[region] = {}
            # Gather countries
            countries = []
            for country_code, timezones in pytz.country_timezones.items():
                if tz in timezones:
                    country = pytz.country_names.get(country_code, "Unknown")
                    countries.append(country)
            if not countries:
                countries.append("Unknown")
            grouped_timezones[region][tz] = countries
    except Exception as e:
        print(f"Error grouping timezones: {e}")
    return grouped_timezones

# ------------------ DIGITAL CLOCK ------------------ #

class DigitalClock(tk.Frame):
    """
    A Frame that displays a digital clock for a specific timezone.
    """
    def __init__(self, parent, timezone_str, dark_mode=False):
        super().__init__(parent)
        self.timezone_str = timezone_str
        try:
            self.timezone = ZoneInfo(timezone_str)
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Invalid timezone: {timezone_str}")
            print(f"Error initializing ZoneInfo for {timezone_str}: {e}")
            self.timezone = ZoneInfo("UTC")
        self.dark_mode = dark_mode

        # Label for time
        self.time_label = tk.Label(self, font=("Helvetica", 48))
        self.time_label.pack(expand=True, fill=tk.BOTH)

        # Info label
        self.info_label = tk.Label(self, font=("Helvetica", 12))
        self.info_label.pack(fill=tk.X)

        # Start update thread
        self.stop_threads = False
        self.update_thread = threading.Thread(target=self.update_clock, daemon=True)
        self.update_thread.start()

        # Apply theme
        self.apply_theme()

    def apply_theme(self):
        """Apply dark or light theme to the digital clock."""
        bg_color = DARK_BG if self.dark_mode else LIGHT_BG
        fg_color = DARK_FG if self.dark_mode else LIGHT_FG
        self.configure(bg=bg_color)
        self.time_label.configure(bg=bg_color, fg=fg_color)
        self.info_label.configure(bg=bg_color, fg=fg_color)

    def update_clock(self):
        """Continuously updates the digital clock."""
        while not self.stop_threads:
            try:
                now = datetime.datetime.now(self.timezone)
                current_time = now.strftime("%H:%M:%S")
                offset_hrs = now.utcoffset().total_seconds() / 3600 if now.utcoffset() else 0
                offset_label = f"{get_localized_text('utc_offset')}: UTC{offset_hrs:+.1f}"
                dst_label = f"{get_localized_text('dst')}: {'Yes' if now.dst() else 'No'}"
                date_label = f"{get_localized_text('date')}: {now.strftime('%Y-%m-%d')}"
                info_text = f"{offset_label} | {dst_label} | {date_label}"

                def update_ui():
                    self.time_label.config(text=current_time)
                    self.info_label.config(text=info_text)

                self.time_label.after(0, update_ui)
            except Exception as e:
                print(f"Error updating digital clock: {e}")
                traceback.print_exc()
            time.sleep(1)

# ------------------ ANALOG CLOCK ------------------ #

class AnalogClock(tk.Frame):
    """
    A Frame that displays an analog clock for a specific timezone.
    """
    def __init__(self, parent, timezone_str, dark_mode=False):
        super().__init__(parent)
        self.timezone_str = timezone_str
        try:
            self.timezone = ZoneInfo(timezone_str)
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Invalid timezone: {timezone_str}")
            print(f"Error initializing ZoneInfo for {timezone_str}: {e}")
            self.timezone = ZoneInfo("UTC")
        self.dark_mode = dark_mode

        # Canvas for analog clock
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.center_x = 200
        self.center_y = 200
        self.radius = 180

        self.draw_clock_face()

        # Start update thread
        self.stop_threads = False
        self.update_thread = threading.Thread(target=self.update_clock, daemon=True)
        self.update_thread.start()

        # Apply theme
        self.apply_theme()

    def apply_theme(self):
        """Apply dark or light theme to the analog clock."""
        bg_color = DARK_BG if self.dark_mode else LIGHT_BG
        fg_color = DARK_FG if self.dark_mode else LIGHT_FG
        self.canvas.configure(bg=bg_color)
        # Update existing items
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if "hands" in tags or "hour_marks" in tags:
                self.canvas.itemconfig(item, fill=fg_color, outline=fg_color)

    def draw_clock_face(self):
        """Draw the static parts of the analog clock."""
        try:
            # Outer circle
            self.canvas.create_oval(
                self.center_x - self.radius, self.center_y - self.radius,
                self.center_x + self.radius, self.center_y + self.radius,
                width=4, outline="black"
            )
            # Hour markings
            for hour in range(1, 13):
                angle = math.pi / 6 * (hour - 3)
                x = self.center_x + self.radius * 0.85 * math.cos(angle)
                y = self.center_y + self.radius * 0.85 * math.sin(angle)
                self.canvas.create_text(x, y, text=str(hour), font=("Helvetica", 14, "bold"), fill="black")
        except Exception as e:
            print(f"Error drawing analog clock face: {e}")
            traceback.print_exc()

    def update_clock(self):
        """Continuously updates the analog clock."""
        while not self.stop_threads:
            try:
                now = datetime.datetime.now(self.timezone)
                hours = now.hour % 12
                minutes = now.minute
                seconds = now.second

                # Calculate angles
                sec_angle = math.pi / 30 * seconds - math.pi / 2
                min_angle = math.pi / 30 * minutes + (math.pi / 1800) * seconds - math.pi / 2
                hour_angle = math.pi / 6 * hours + (math.pi / 360) * minutes - math.pi / 2

                def draw_hands():
                    self.canvas.delete("hands")
                    # Hour hand
                    hour_length = self.radius * 0.5
                    hour_x = self.center_x + hour_length * math.cos(hour_angle)
                    hour_y = self.center_y + hour_length * math.sin(hour_angle)
                    self.canvas.create_line(
                        self.center_x, self.center_y, hour_x, hour_y,
                        width=6, fill="black", tags="hands"
                    )
                    # Minute hand
                    min_length = self.radius * 0.75
                    min_x = self.center_x + min_length * math.cos(min_angle)
                    min_y = self.center_y + min_length * math.sin(min_angle)
                    self.canvas.create_line(
                        self.center_x, self.center_y, min_x, min_y,
                        width=4, fill="blue", tags="hands"
                    )
                    # Second hand
                    sec_length = self.radius * 0.9
                    sec_x = self.center_x + sec_length * math.cos(sec_angle)
                    sec_y = self.center_y + sec_length * math.sin(sec_angle)
                    self.canvas.create_line(
                        self.center_x, self.center_y, sec_x, sec_y,
                        width=2, fill="red", tags="hands"
                    )

                self.canvas.after(0, draw_hands)
            except Exception as e:
                print(f"Error updating analog clock: {e}")
                traceback.print_exc()
            time.sleep(1)

# ------------------ EARTH CLOCK ------------------ #

class EarthClock(tk.Frame):
    """
    A Frame that visualizes the Earth's rotation and current timezone.
    """
    def __init__(self, parent, timezone_str, dark_mode=False):
        super().__init__(parent)
        self.timezone_str = timezone_str
        try:
            self.timezone = ZoneInfo(timezone_str)
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Invalid timezone: {timezone_str}")
            print(f"Error initializing ZoneInfo for {timezone_str}: {e}")
            self.timezone = ZoneInfo("UTC")
        self.dark_mode = dark_mode

        # Canvas for Earth clock
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.center_x = 300
        self.center_y = 300
        self.radius = 250

        self.rotation_angle = 0

        self.draw_earth()

        # Start update thread
        self.stop_threads = False
        self.update_thread = threading.Thread(target=self.update_earth_clock, daemon=True)
        self.update_thread.start()

        # Bind click on Earth canvas
        self.canvas.bind("<Button-1>", self.on_earth_click)

        # Apply theme
        self.apply_theme()

    def apply_theme(self):
        """Apply dark or light theme to the Earth clock."""
        bg_color = DARK_BG if self.dark_mode else LIGHT_BG
        fg_color = DARK_FG if self.dark_mode else LIGHT_FG
        self.canvas.configure(bg=bg_color)
        # Update existing items
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if "continent" in tags:
                self.canvas.itemconfig(item, fill="green" if not self.dark_mode else "darkgreen")
            elif "terminator" in tags:
                self.canvas.itemconfig(item, fill="#ADD8E6" if not self.dark_mode else "#000080")  # Light blue for day, dark blue for night
            elif "timezone_line" in tags:
                self.canvas.itemconfig(item, fill="red")
            elif "equator" in tags or "prime_meridian" in tags:
                self.canvas.itemconfig(item, fill=fg_color)
            elif "earth_outline" in tags:
                self.canvas.itemconfig(item, outline=fg_color)
            elif "night_shadow" in tags:
                self.canvas.itemconfig(item, fill="#00000030" if self.dark_mode else "#00000010")  # Semi-transparent shadow

    def draw_earth(self):
        """Draw the Earth with continents, equator, prime meridian, and terminators."""
        try:
            # Earth circle
            self.canvas.create_oval(
                self.center_x - self.radius, self.center_y - self.radius,
                self.center_x + self.radius, self.center_y + self.radius,
                fill="lightblue", outline="black", width=2, tags="earth_outline"
            )
            # Equator
            self.canvas.create_line(
                self.center_x - self.radius, self.center_y,
                self.center_x + self.radius, self.center_y,
                fill="black", width=2, tags="equator"
            )
            # Prime Meridian
            self.canvas.create_line(
                self.center_x, self.center_y - self.radius,
                self.center_x, self.center_y + self.radius,
                fill="black", width=2, tags="prime_meridian"
            )
            # Simplified continents
            continents = [
                # North America
                [(250, 200), (270, 180), (290, 200), (270, 220)],
                # Europe
                [(300, 150), (320, 130), (340, 150), (320, 170)],
                # Africa
                [(350, 300), (370, 280), (390, 300), (370, 320)],
                # Asia
                [(400, 150), (420, 130), (440, 150), (420, 170)],
                # Australia
                [(500, 400), (520, 380), (540, 400), (520, 420)],
                # South America
                [(250, 400), (270, 380), (290, 400), (270, 420)],
            ]
            for continent in continents:
                self.canvas.create_polygon(
                    continent,
                    fill="green", outline="black", tags="continent"
                )
            # Terminator
            self.terminator = self.canvas.create_polygon(
                self.calculate_terminator_polygon(),
                fill="#00000010",  # Semi-transparent black
                outline="",
                tags="night_shadow"
            )
            # Timezone line
            self.timezone_line = self.canvas.create_line(0, 0, 0, 0, fill="red", width=3, tags="timezone_line")
        except Exception as e:
            print(f"Error drawing Earth clock: {e}")
            traceback.print_exc()

    def calculate_terminator_polygon(self):
        """Calculate the polygon points for the night shadow based on current time."""
        try:
            now = datetime.datetime.utcnow()
            # Calculate the current longitude of the sun (assuming UTC)
            sun_long = (now.hour + now.minute/60 + now.second/3600) * 15  # 360 degrees / 24 hours
            angle = math.radians(sun_long - 90)  # Adjust so 0 radians is at top

            # Calculate two points on the circumference for the terminator
            x1 = self.center_x + self.radius * math.cos(angle)
            y1 = self.center_y + self.radius * math.sin(angle)
            x2 = self.center_x + self.radius * math.cos(angle + math.pi)
            y2 = self.center_y + self.radius * math.sin(angle + math.pi)

            # Define a large polygon covering the night side
            return [
                x1, y1,
                x2, y2,
                self.center_x + self.radius * math.cos(angle + math.pi + math.pi / 2), 
                self.center_y + self.radius * math.sin(angle + math.pi + math.pi / 2),
                self.center_x + self.radius * math.cos(angle - math.pi / 2), 
                self.center_y + self.radius * math.sin(angle - math.pi / 2)
            ]
        except Exception as e:
            print(f"Error calculating terminator polygon: {e}")
            traceback.print_exc()
            return []

    def update_earth_clock(self):
        """
        Update the Earth clock visuals:
        - Update terminator
        - Update timezone line based on selected timezone
        """
        while not self.stop_threads:
            try:
                now = datetime.datetime.now(self.timezone)
                # Calculate UTC offset in hours
                offset_hrs = now.utcoffset().total_seconds() / 3600 if now.utcoffset() else 0
                # Each hour represents 15 degrees longitude
                longitude = offset_hrs * 15

                # Calculate angle for timezone line
                angle = math.radians(longitude - 90)  # Adjust so 0 radians is at top

                # Update terminator
                terminator_coords = self.calculate_terminator_polygon()
                self.canvas.coords(self.terminator, terminator_coords)

                # Update timezone line
                end_x = self.center_x + self.radius * math.cos(angle)
                end_y = self.center_y + self.radius * math.sin(angle)
                self.canvas.coords(self.timezone_line, self.center_x, self.center_y, end_x, end_y)
            except Exception as e:
                print(f"Error updating Earth clock: {e}")
                traceback.print_exc()
            time.sleep(1)

    def on_earth_click(self, event):
        """Handle click on Earth canvas by showing approximate longitude."""
        try:
            # Translate click coordinates into approximate longitude
            dx = event.x - self.center_x
            dy = event.y - self.center_y
            dist = math.hypot(dx, dy)
            if dist <= self.radius:
                # The user clicked inside the Earth circle
                angle = math.degrees(math.atan2(dy, dx))
                # Convert angle so that 0 degrees is at top
                longitude_approx = (angle + 90) % 360
                if longitude_approx > 180:
                    longitude_approx -= 360  # Convert to -180 to 180
                messagebox.showinfo(
                    "Earth Click",
                    f"You clicked near longitude ≈ {longitude_approx:.1f}°"
                )
        except Exception as e:
            print(f"Error handling Earth click: {e}")
            traceback.print_exc()

# ------------------ MULTI CLOCK WINDOW ------------------ #

class MultiClockWindow(tk.Toplevel):
    """
    A Toplevel window containing multiple tabs:
    - Digital Clock
    - Analog Clock
    - Earth Clock
    Each clock is displayed in a separate ttk.Notebook tab.
    """
    def __init__(self, parent, timezone_str, dark_mode=False):
        super().__init__(parent)
        self.timezone_str = timezone_str
        try:
            self.timezone = ZoneInfo(timezone_str)
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Invalid timezone: {timezone_str}")
            print(f"Error initializing ZoneInfo for {timezone_str}: {e}")
            self.timezone = ZoneInfo("UTC")
        self.dark_mode = dark_mode
        # Window setup
        self.title(f"{timezone_str}")
        self.geometry("900x700")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create frames for each tab
        self.digital_frame = ttk.Frame(self.notebook)
        self.analog_frame = ttk.Frame(self.notebook)
        self.earth_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.digital_frame, text=get_localized_text("digital_clock"))
        self.notebook.add(self.analog_frame, text=get_localized_text("analog_clock"))
        self.notebook.add(self.earth_frame, text=get_localized_text("earth_clock"))

        # Digital clock
        self.digital_clock = DigitalClock(self.digital_frame, timezone_str, dark_mode)
        self.digital_clock.pack(fill=tk.BOTH, expand=True)

        # Analog clock
        self.analog_clock = AnalogClock(self.analog_frame, timezone_str, dark_mode)
        self.analog_clock.pack(fill=tk.BOTH, expand=True)

        # Earth clock
        self.earth_clock = EarthClock(self.earth_frame, timezone_str, dark_mode)
        self.earth_clock.pack(fill=tk.BOTH, expand=True)

        # Info label at bottom
        self.info_label = tk.Label(self, font=("Helvetica", 12))
        self.info_label.pack(fill=tk.X, side=tk.BOTTOM)

        # Apply theme
        self.apply_theme()

    def apply_theme(self):
        """Apply dark or light theme to elements in this window."""
        try:
            bg_color = DARK_BG if self.dark_mode else LIGHT_BG
            fg_color = DARK_FG if self.dark_mode else LIGHT_FG
            self.configure(bg=bg_color)
            self.info_label.configure(bg=bg_color, fg=fg_color)
        except Exception as e:
            print(f"Error applying theme to MultiClockWindow: {e}")
            traceback.print_exc()

    def on_close(self):
        """Handle closing the window and stopping threads."""
        try:
            if hasattr(self, 'digital_clock') and hasattr(self.digital_clock, 'stop_threads'):
                self.digital_clock.stop_threads = True
            if hasattr(self, 'analog_clock') and hasattr(self.analog_clock, 'stop_threads'):
                self.analog_clock.stop_threads = True
            if hasattr(self, 'earth_clock') and hasattr(self.earth_clock, 'stop_threads'):
                self.earth_clock.stop_threads = True
            self.destroy()
        except Exception as e:
            print(f"Error closing MultiClockWindow: {e}")
            traceback.print_exc()

# ------------------ MAIN APPLICATION ------------------ #

class TimezoneApp(tk.Tk):
    """
    Main application window that lists all timezones grouped by region, 
    with search, localization, dark mode, and session management.
    """
    def __init__(self):
        super().__init__()
        self.title(get_localized_text("app_title"))
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Load session data
        self.session = load_session()
        self.dark_mode = self.session.get("dark_mode", False)

        # Load grouped timezones
        self.grouped_timezones = get_timezones_grouped()

        # Create UI
        self.create_widgets()
        self.apply_theme()

    # ------------------ THEME HANDLING ------------------ #

    def apply_theme(self):
        """Switch between light and dark mode in the main window."""
        try:
            bg_color = DARK_BG if self.dark_mode else LIGHT_BG
            fg_color = DARK_FG if self.dark_mode else LIGHT_FG

            self.configure(bg=bg_color)
            # Update frames and labels
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame):
                    widget.configure(style="TFrame")
                if isinstance(widget, tk.Label):
                    widget.configure(bg=bg_color, fg=fg_color)
                if isinstance(widget, ttk.Button):
                    pass  # ttk buttons adapt based on theme

            # Update Treeview background
            style = ttk.Style(self)
            if self.dark_mode:
                style.configure("Treeview", background="#4D4D4D", foreground="white", fieldbackground="#4D4D4D")
                style.configure("Treeview.Heading", background="#333333", foreground="white")
            else:
                style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
                style.configure("Treeview.Heading", background="#D3D3D3", foreground="black")
        except Exception as e:
            print(f"Error applying theme: {e}")
            traceback.print_exc()

    def toggle_dark_mode(self):
        """Toggle the dark mode setting and reapply theme."""
        try:
            self.dark_mode = not self.dark_mode
            self.session["dark_mode"] = self.dark_mode
            save_session(self.session)
            self.apply_theme()
        except Exception as e:
            print(f"Error toggling dark mode: {e}")
            traceback.print_exc()

    # ------------------ WIDGET CREATION ------------------ #

    def create_widgets(self):
        try:
            # Top frame for search & dark mode button
            top_frame = ttk.Frame(self)
            top_frame.pack(fill=tk.X, padx=10, pady=10)

            # Search label & entry
            search_label = tk.Label(top_frame, text=get_localized_text("search_label"), font=("Helvetica", 12))
            search_label.pack(side=tk.LEFT, padx=(0, 5))

            self.search_var = tk.StringVar()
            self.search_var.trace("w", self.update_filter)
            search_entry = ttk.Entry(top_frame, textvariable=self.search_var)
            search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Dark mode toggle button
            dark_mode_btn = ttk.Button(top_frame, text=get_localized_text("show_hide_dark_mode"), command=self.toggle_dark_mode)
            dark_mode_btn.pack(side=tk.LEFT, padx=(10, 0))

            # Middle frame for Treeview & actions
            main_frame = ttk.Frame(self)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Treeview for timezones
            tree_frame = ttk.Frame(main_frame)
            tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            tree_scrollbar = ttk.Scrollbar(tree_frame)
            tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.tree = ttk.Treeview(
                tree_frame, 
                columns=("Countries",), 
                show="tree headings", 
                yscrollcommand=tree_scrollbar.set
            )
            self.tree.heading("#0", text=get_localized_text("region_timezone"), anchor="w")
            self.tree.heading("Countries", text=get_localized_text("countries_column"), anchor="w")
            self.tree.column("Countries", anchor="w", width=200)
            self.tree.pack(fill=tk.BOTH, expand=True)

            tree_scrollbar.config(command=self.tree.yview)

            # Insert grouped timezones into the Treeview
            self.populate_treeview()

            # Right-side frame for buttons & favorite management
            btn_frame = ttk.Frame(main_frame)
            btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

            # Favorites label
            fav_label = tk.Label(btn_frame, text=get_localized_text("favorites_label"), font=("Helvetica", 12, "bold"))
            fav_label.pack(pady=5)

            # Buttons
            load_fav_btn = ttk.Button(btn_frame, text=get_localized_text("load_favorite"), command=self.load_favorite_timezone)
            load_fav_btn.pack(pady=5, fill=tk.X)

            save_fav_btn = ttk.Button(btn_frame, text=get_localized_text("save_favorite"), command=self.save_favorite_timezone)
            save_fav_btn.pack(pady=5, fill=tk.X)

            # Create Multi-Clock button
            multi_clock_btn = ttk.Button(btn_frame, text="Open Clocks", command=self.open_multi_clock)
            multi_clock_btn.pack(pady=30, fill=tk.X)
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Failed to create widgets: {e}")
            print(f"Error creating widgets: {e}")
            traceback.print_exc()

    def populate_treeview(self, filter_text=""):
        """Populates the Treeview with regions/timezones."""
        try:
            # Clear existing entries
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Iterate through regions
            for region, tz_dict in sorted(self.grouped_timezones.items()):
                # Filter timezones that match search
                matching_timezones = {
                    tz: countries 
                    for tz, countries in tz_dict.items() 
                    if filter_text.lower() in tz.lower()
                }
                if matching_timezones:
                    region_id = self.tree.insert("", "end", text=region, open=False)
                    for tz, countries in sorted(matching_timezones.items()):
                        country_list = ", ".join(sorted(set(countries)))
                        self.tree.insert(region_id, "end", iid=tz, text=tz, values=(country_list,))
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Failed to populate Treeview: {e}")
            print(f"Error populating Treeview: {e}")
            traceback.print_exc()

    def update_filter(self, *args):
        """Update the Treeview based on search input."""
        try:
            text = self.search_var.get()
            self.populate_treeview(text)
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Failed to update filter: {e}")
            print(f"Error updating filter: {e}")
            traceback.print_exc()

    # ------------------ FAVORITES & SESSION ------------------ #

    def get_selected_timezone(self) -> str:
        """Return the selected timezone or None if invalid."""
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning(get_localized_text("warning_title"), get_localized_text("no_selection_warning"))
                return None
            selected_item = selected[0]
            parent = self.tree.parent(selected_item)
            if not parent:
                # It's a region, not a timezone
                messagebox.showwarning(get_localized_text("warning_title"), get_localized_text("invalid_selection_warning"))
                return None
            return selected_item
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Failed to get selected timezone: {e}")
            print(f"Error getting selected timezone: {e}")
            traceback.print_exc()
            return None

    def save_favorite_timezone(self):
        """Save current selection as favorite in session."""
        try:
            tz = self.get_selected_timezone()
            if tz:
                self.session["favorite_timezone"] = tz
                save_session(self.session)
                messagebox.showinfo(get_localized_text("info_title"), get_localized_text("save_favorite_success"))
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Failed to save favorite timezone: {e}")
            print(f"Error saving favorite timezone: {e}")
            traceback.print_exc()

    def load_favorite_timezone(self):
        """Load favorite timezone from session."""
        try:
            fav = self.session.get("favorite_timezone", None)
            if fav:
                # Try to select it in the tree
                if self.tree.exists(fav):
                    self.tree.selection_set(fav)
                    self.tree.see(fav)
                    messagebox.showinfo(get_localized_text("info_title"), get_localized_text("load_favorite_success"))
                else:
                    messagebox.showwarning(get_localized_text("warning_title"), get_localized_text("load_favorite_fail"))
            else:
                messagebox.showwarning(get_localized_text("warning_title"), get_localized_text("load_favorite_fail"))
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Failed to load favorite timezone: {e}")
            print(f"Error loading favorite timezone: {e}")
            traceback.print_exc()

    # ------------------ OPEN MULTI-CLOCK ------------------ #

    def open_multi_clock(self):
        """Open a MultiClockWindow for the selected timezone."""
        try:
            tz = self.get_selected_timezone()
            if tz:
                MultiClockWindow(self, tz, dark_mode=self.dark_mode)
        except Exception as e:
            messagebox.showerror(get_localized_text("error_title"), f"Failed to open MultiClockWindow: {e}")
            print(f"Error opening MultiClockWindow: {e}")
            traceback.print_exc()

# ------------------ ENTRY POINT ------------------ #

if __name__ == "__main__":
    try:
        app = TimezoneApp()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        traceback.print_exc()
