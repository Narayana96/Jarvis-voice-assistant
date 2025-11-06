import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import threading
import math
import requests
from bs4 import BeautifulSoup
import subprocess
import platform
import urllib.parse
import webbrowser
import time
import queue

# API Keys - Replace with your own keys
NEWS_API_KEY = "41a7a41c979b47738401dbd433ea14f9"  
WEATHER_API_KEY = "c11900c45a6b4552fbf09a771d18cb5a"  

class EnhancedVoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS Voice Assistant")
        self.root.geometry("800x900")
        self.root.configure(bg="#0a0e27")
        self.root.resizable(False, False)
        
        # Initialize text-to-speech on main thread
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)
        
        # Speech queue for thread-safe speaking
        self.speech_queue = queue.Queue()
        self.is_engine_busy = False
        
        # Animation variables
        self.is_speaking = False
        self.is_listening = False
        self.animation_offset = 0
        self.particles = []
        
        # Continuous listening control
        self.continuous_mode = True
        self.should_stop = False
        
        # Assistant name
        self.assistant_name = self.load_name()
        
        # Detect OS for app opening
        self.os_type = platform.system()
        
        # Create UI
        self.create_widgets()
        
        # Start speech processor
        self.process_speech_queue()
        
        # Welcome message and start continuous listening
        self.root.after(500, self.start_assistant)
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#0a0e27")
        header_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text=f"⚡ {self.assistant_name.upper()} ⚡",
            font=("Orbitron", 28, "bold"),
            bg="#0a0e27",
            fg="#00ffff"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="AI Voice Assistant - Continuous Mode",
            font=("Arial", 12),
            bg="#0a0e27",
            fg="#8892b0"
        )
        subtitle_label.pack()
        
        # Main Canvas for Animation
        self.canvas = tk.Canvas(
            self.root,
            width=400,
            height=400,
            bg="#0a0e27",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Create animated elements
        self.create_animation_elements()
        
        # Subtitle Label (for live speech display)
        self.subtitle_frame = tk.Frame(self.root, bg="#1a1f3a", relief=tk.RIDGE, bd=2)
        self.subtitle_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.subtitle_label = tk.Label(
            self.subtitle_frame,
            text="...",
            font=("Arial", 14, "italic"),
            bg="#1a1f3a",
            fg="#00ffff",
            wraplength=700,
            justify=tk.CENTER,
            height=3
        )
        self.subtitle_label.pack(pady=10)
        
        # Status Label
        self.status_label = tk.Label(
            self.root,
            text="● Status: Initializing...",
            font=("Arial", 11, "bold"),
            bg="#0a0e27",
            fg="#fbbf24"
        )
        self.status_label.pack(pady=5)
        
        # Conversation Display
        conv_frame = tk.Frame(self.root, bg="#0a0e27")
        conv_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(
            conv_frame,
            text="Conversation History",
            font=("Arial", 11, "bold"),
            bg="#0a0e27",
            fg="#8892b0"
        ).pack(anchor=tk.W)
        
        self.text_area = scrolledtext.ScrolledText(
            conv_frame,
            height=10,
            width=80,
            font=("Consolas", 10),
            bg="#1a1f3a",
            fg="#e0e0e0",
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            insertbackground="#00ffff"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags
        self.text_area.tag_config("user", foreground="#00ffff", font=("Consolas", 10, "bold"))
        self.text_area.tag_config("assistant", foreground="#4ade80", font=("Consolas", 10))
        self.text_area.tag_config("system", foreground="#fbbf24", font=("Consolas", 9, "italic"))
        self.text_area.tag_config("command", foreground="#ff6b6b", font=("Consolas", 10, "bold"))
        
        # Control Buttons
        button_frame = tk.Frame(self.root, bg="#0a0e27")
        button_frame.pack(pady=20)
        
        # Mode indicator
        self.mode_label = tk.Label(
            self.root,
            text="🔄 CONTINUOUS LISTENING MODE - Say 'go offline' or 'exit' to stop",
            font=("Arial", 10, "bold"),
            bg="#0a0e27",
            fg="#00ff00"
        )
        self.mode_label.pack(pady=5)
        
        # Command list button
        self.commands_button = tk.Button(
            button_frame,
            text="📋 COMMANDS LIST",
            font=("Arial", 11, "bold"),
            bg="#8b5cf6",
            fg="#ffffff",
            activebackground="#7c3aed",
            width=15,
            height=1,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_commands_list
        )
        self.commands_button.pack(pady=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ STOP & EXIT",
            font=("Arial", 13, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            width=20,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.stop_assistant
        )
        self.stop_button.pack()
        
        # Start idle animation
        self.animate_idle()
    
    def create_animation_elements(self):
        """Create circles and particles for animation."""
        center_x, center_y = 200, 200
        
        # Create concentric circles
        self.circles = []
        for i in range(6):
            radius = 40 + i * 20
            circle = self.canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline="#00ffff",
                width=2,
                fill=""
            )
            self.circles.append(circle)
        
        # Create center core
        self.core = self.canvas.create_oval(
            center_x - 25, center_y - 25,
            center_x + 25, center_y + 25,
            fill="#00ffff",
            outline="#00cccc",
            width=3
        )
        
        # Create particles
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(80, 180)
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            size = random.uniform(2, 4)
            
            particle = self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill="#00ffff",
                outline=""
            )
            self.particles.append({
                'id': particle,
                'angle': angle,
                'distance': distance,
                'speed': random.uniform(0.01, 0.03)
            })
    
    def animate_idle(self):
        """Idle animation."""
        if not self.is_speaking and not self.is_listening:
            self.animation_offset += 0.05
            center_x, center_y = 200, 200
            
            # Animate circles
            for i, circle in enumerate(self.circles):
                base_radius = 40 + i * 20
                pulse = math.sin(self.animation_offset + i * 0.4) * 3
                new_radius = base_radius + pulse
                
                self.canvas.coords(
                    circle,
                    center_x - new_radius, center_y - new_radius,
                    center_x + new_radius, center_y + new_radius
                )
                
                # Subtle color fade
                intensity = int(200 + 55 * math.sin(self.animation_offset + i * 0.3))
                color = f"#{intensity:02x}ffff" if intensity < 255 else "#00ffff"
                self.canvas.itemconfig(circle, outline=color)
            
            # Animate particles
            for particle in self.particles:
                particle['angle'] += particle['speed']
                x = center_x + particle['distance'] * math.cos(particle['angle'])
                y = center_y + particle['distance'] * math.sin(particle['angle'])
                size = 2
                self.canvas.coords(particle['id'], x - size, y - size, x + size, y + size)
        
        self.root.after(30, self.animate_idle)
    
    def animate_speaking(self):
        """Speaking animation with wave effect."""
        if self.is_speaking:
            self.animation_offset += 0.15
            center_x, center_y = 200, 200
            
            for i, circle in enumerate(self.circles):
                base_radius = 40 + i * 20
                pulse = math.sin(self.animation_offset * 2 + i * 0.6) * 10
                new_radius = base_radius + pulse
                
                self.canvas.coords(
                    circle,
                    center_x - new_radius, center_y - new_radius,
                    center_x + new_radius, center_y + new_radius
                )
                
                # Vibrant colors when speaking
                intensity = int(150 + 105 * abs(math.sin(self.animation_offset + i * 0.5)))
                color = f"#00{intensity:02x}ff"
                self.canvas.itemconfig(circle, outline=color, width=3)
            
            # Core pulsing
            core_pulse = 25 + math.sin(self.animation_offset * 3) * 5
            self.canvas.coords(
                self.core,
                center_x - core_pulse, center_y - core_pulse,
                center_x + core_pulse, center_y + core_pulse
            )
            
            self.root.after(30, self.animate_speaking)
    
    def animate_listening(self):
        """Listening animation with ripple effect."""
        if self.is_listening:
            self.animation_offset += 0.1
            center_x, center_y = 200, 200
            
            for i, circle in enumerate(self.circles):
                base_radius = 40 + i * 20
                ripple = abs(math.sin(self.animation_offset - i * 0.3)) * 8
                new_radius = base_radius + ripple
                
                self.canvas.coords(
                    circle,
                    center_x - new_radius, center_y - new_radius,
                    center_x + new_radius, center_y + new_radius
                )
                
                # Orange/yellow listening color
                intensity_g = int(200 + 55 * math.sin(self.animation_offset + i * 0.4))
                color = f"#ff{intensity_g:02x}00"
                self.canvas.itemconfig(circle, outline=color, width=2)
            
            self.root.after(30, self.animate_listening)
    
    def speak(self, audio):
        """Queue speech to be processed on main thread - FIXED VERSION."""
        self.speech_queue.put(audio)
    
    def process_speech_queue(self):
        """Process speech queue on main thread - CRITICAL FIX."""
        try:
            if not self.is_engine_busy and not self.speech_queue.empty():
                audio = self.speech_queue.get_nowait()
                
                # Set speaking state
                self.is_speaking = True
                self.is_engine_busy = True
                self.animate_speaking()
                
                # Display in subtitle
                self.subtitle_label.config(text=f'"{audio}"')
                
                # Add to conversation
                self.text_area.insert(tk.END, f"{self.assistant_name}: ", "assistant")
                self.text_area.insert(tk.END, f"{audio}\n\n")
                self.text_area.see(tk.END)
                
                # Force GUI update BEFORE speaking
                self.root.update_idletasks()
                
                try:
                    # Speak using pyttsx3 on main thread
                    self.engine.say(audio)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"Speech error: {e}")
                    # Reinitialize engine if needed
                    try:
                        self.engine = pyttsx3.init()
                    except:
                        pass
                
                # Reset speaking state
                self.is_speaking = False
                self.is_engine_busy = False
                self.subtitle_label.config(text="...")
                
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Queue processing error: {e}")
            self.is_speaking = False
            self.is_engine_busy = False
        
        # Schedule next check (faster polling for responsiveness)
        self.root.after(50, self.process_speech_queue)
    
    def update_status(self, status, color="#4ade80"):
        """Update status with color."""
        self.status_label.config(text=f"● Status: {status}", fg=color)
    
    def load_name(self):
        """Load assistant name."""
        try:
            with open("assistant_name.txt", "r") as f:
                return f.read().strip()
        except:
            return "Jarvis"
    
    def open_application(self, app_name):
        """Open applications based on OS - runs in thread."""
        def _open_app():
            app_name_lower = app_name.lower().strip()
            success = False
            
            try:
                if self.os_type == "Windows":
                    apps = {
                        "notepad": "notepad.exe",
                        "calculator": "calc.exe",
                        "paint": "mspaint.exe",
                        "cmd": "cmd.exe",
                        "command prompt": "cmd.exe",
                        "task manager": "taskmgr.exe",
                        "chrome": "chrome.exe",
                        "google chrome": "chrome.exe",
                        "edge": "msedge.exe",
                        "microsoft edge": "msedge.exe",
                        "firefox": "firefox.exe",
                        "vscode": "code.exe",
                        "visual studio code": "code.exe",
                        "excel": "excel.exe",
                        "word": "winword.exe",
                        "powerpoint": "powerpnt.exe",
                        "outlook": "outlook.exe",
                        "explorer": "explorer.exe",
                        "file explorer": "explorer.exe"
                    }
                    
                    if app_name_lower in apps:
                        subprocess.Popen([apps[app_name_lower]], shell=True)
                        success = True
                    else:
                        subprocess.Popen([app_name_lower], shell=True)
                        success = True
                        
                elif self.os_type == "Darwin":  # macOS
                    apps = {
                        "safari": "Safari",
                        "chrome": "Google Chrome",
                        "google chrome": "Google Chrome",
                        "firefox": "Firefox",
                        "notes": "Notes",
                        "calculator": "Calculator",
                        "mail": "Mail",
                        "calendar": "Calendar",
                        "finder": "Finder",
                        "terminal": "Terminal"
                    }
                    
                    if app_name_lower in apps:
                        subprocess.Popen(["open", "-a", apps[app_name_lower]])
                        success = True
                    else:
                        subprocess.Popen(["open", "-a", app_name.title()])
                        success = True
                        
                elif self.os_type == "Linux":
                    apps = {
                        "firefox": "firefox",
                        "chrome": "google-chrome",
                        "google chrome": "google-chrome",
                        "terminal": "gnome-terminal",
                        "calculator": "gnome-calculator",
                        "files": "nautilus",
                        "text editor": "gedit"
                    }
                    
                    if app_name_lower in apps:
                        subprocess.Popen([apps[app_name_lower]])
                        success = True
                    else:
                        subprocess.Popen([app_name_lower])
                        success = True
                
                if success:
                    self.root.after(0, lambda: self.text_area.insert(tk.END, f"✓ Opened {app_name}\n", "system"))
                
            except FileNotFoundError:
                self.speak(f"Sorry, I couldn't find {app_name}. Please make sure it's installed.")
                self.root.after(0, lambda: self.text_area.insert(tk.END, f"✗ Application not found: {app_name}\n", "system"))
            except Exception as e:
                self.speak(f"Unable to open {app_name}")
                self.root.after(0, lambda: self.text_area.insert(tk.END, f"✗ Error: {str(e)}\n", "system"))
        
        # Speak first, then open in thread
        self.speak(f"Opening {app_name}")
        threading.Thread(target=_open_app, daemon=True).start()
    
    def get_news(self):
        """Fetch latest news headlines - runs in thread."""
        def _fetch_news():
            try:
                if NEWS_API_KEY == "YOUR_NEWS_API_KEY":
                    self.speak("News API key not configured")
                    return
                
                url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
                response = requests.get(url, timeout=10)
                news_data = response.json()
                
                if news_data.get('status') == 'ok':
                    articles = news_data.get('articles', [])[:5]
                    self.speak("Here are today's top 5 headlines")
                    
                    for i, article in enumerate(articles, 1):
                        title = article.get('title', 'No title')
                        source = article.get('source', {}).get('name', 'Unknown')
                        
                        self.root.after(0, lambda t=title, s=source, n=i: [
                            self.text_area.insert(tk.END, f"📰 News {n}: ", "system"),
                            self.text_area.insert(tk.END, f"{t} (Source: {s})\n"),
                            self.text_area.see(tk.END)
                        ])
                        
                        self.speak(f"News {i}. {title}")
                        
                else:
                    self.speak("Unable to fetch news")
                    
            except Exception as e:
                self.speak("Sorry, I couldn't fetch the news right now")
        
        self.speak("Fetching latest news headlines")
        threading.Thread(target=_fetch_news, daemon=True).start()
    
    def get_weather(self, city=None):
        """Get weather information - runs in thread."""
        def _fetch_weather(city_name):
            try:
                if WEATHER_API_KEY == "YOUR_WEATHER_API_KEY":
                    self.speak("Weather API key not configured")
                    return
                
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                complete_url = f"{base_url}q={city_name}&appid={WEATHER_API_KEY}&units=metric"
                
                response = requests.get(complete_url, timeout=10)
                weather_data = response.json()
                
                if weather_data.get("cod") != 404:
                    main = weather_data.get("main", {})
                    weather = weather_data.get("weather", [{}])[0]
                    
                    temperature = main.get("temp", "N/A")
                    feels_like = main.get("feels_like", "N/A")
                    humidity = main.get("humidity", "N/A")
                    weather_desc = weather.get("description", "N/A")
                    
                    # Display in text area
                    self.root.after(0, lambda: [
                        self.text_area.insert(tk.END, f"\n🌤️ Weather in {city_name.title()}:\n", "system"),
                        self.text_area.insert(tk.END, f"Temperature: {temperature}°C\n"),
                        self.text_area.insert(tk.END, f"Feels Like: {feels_like}°C\n"),
                        self.text_area.insert(tk.END, f"Humidity: {humidity}%\n"),
                        self.text_area.insert(tk.END, f"Description: {weather_desc.title()}\n\n"),
                        self.text_area.see(tk.END)
                    ])
                    
                    # Speak weather info
                    self.speak(f"Weather in {city_name}")
                    self.speak(f"Temperature is {temperature} degrees celsius")
                    self.speak(f"Humidity is {humidity} percent")
                    self.speak(f"Weather description: {weather_desc}")
                    
                else:
                    self.speak("City not found. Please try again with a valid city name")
                    
            except Exception as e:
                self.speak("Unable to fetch weather information")
        
        if not city:
            self.speak("Which city's weather would you like to know?")
            # The continuous loop will pick up the next command
        else:
            self.speak(f"Fetching weather for {city}")
            threading.Thread(target=_fetch_weather, args=(city,), daemon=True).start()
    
    def play_youtube_video(self, query):
        """NEW FEATURE: Play YouTube video directly - opens first result."""
        def _play_video():
            try:
                from urllib.parse import quote_plus
                
                # Search YouTube and get first video
                search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
                
                # Fetch search results
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(search_url, headers=headers, timeout=10)
                
                # Parse for first video ID
                if 'watch?v=' in response.text:
                    start = response.text.find('watch?v=') + 8
                    video_id = response.text[start:start+11]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    # Open video
                    webbrowser.open(video_url)
                    
                    self.root.after(0, lambda: [
                        self.text_area.insert(tk.END, f"🎥 Playing Video: {query}\n", "system"),
                        self.text_area.insert(tk.END, f"🔗 {video_url}\n\n", "system"),
                        self.text_area.see(tk.END)
                    ])
                    
                    self.speak(f"Playing {query} on YouTube")
                else:
                    # Fallback to search results
                    webbrowser.open(search_url)
                    self.speak(f"Opened YouTube search for {query}")
                    
            except Exception as e:
                self.speak("Sorry, I couldn't play that video")
        
        self.speak(f"Searching for {query} on YouTube")
        threading.Thread(target=_play_video, daemon=True).start()
    
    def search_youtube(self, query):
        """Search YouTube - opens search results."""
        try:
            encoded_query = urllib.parse.quote_plus(query)
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            webbrowser.open(youtube_url)
            
            self.text_area.insert(tk.END, f"🎥 YouTube Search: {query}\n", "system")
            self.text_area.see(tk.END)
            
            self.speak(f"Opened YouTube search results for {query}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't search YouTube right now")
    
    def calculate(self, expression):
        """Perform calculations."""
        try:
            expression = expression.replace("calculate", "").replace("what is", "").replace("equals", "").strip()
            expression = expression.replace("plus", "+").replace("minus", "-")
            expression = expression.replace("times", "*").replace("multiplied by", "*")
            expression = expression.replace("divided by", "/").replace("divide", "/")
            
            result = eval(expression)
            self.speak(f"The answer is {result}")
            self.text_area.insert(tk.END, f"🔢 {expression} = {result}\n", "system")
        except:
            self.speak("I couldn't calculate that")
    
    def show_commands_list(self):
        """Display all available commands."""
        commands_text = """
🎯 AVAILABLE VOICE COMMANDS:

📅 TIME & DATE:
  • "what time is it" / "current time"
  • "what's the date" / "today's date"

🌤️ WEATHER:
  • "weather in [city]"

📰 NEWS:
  • "news" / "headlines"

🎥 YOUTUBE & MEDIA:
  • "play [video name]" - NEW! Plays video directly
  • "search youtube for [query]"
  • "play music"

🔍 SEARCH & INFORMATION:
  • "wikipedia [topic]"
  • "search [query]"
  • "open google/gmail/youtube"

💻 APPLICATIONS:
  • "open notepad/calculator/chrome/etc"

🎯 PRODUCTIVITY:
  • "screenshot"
  • "tell me a joke"
  • "calculate [expression]"

🛠️ SYSTEM:
  • "help" - Show commands
  • "exit" - Stop assistant
"""
        self.text_area.insert(tk.END, "\n" + "="*60 + "\n", "system")
        self.text_area.insert(tk.END, "📋 COMMANDS LIST\n", "command")
        self.text_area.insert(tk.END, "="*60 + "\n", "system")
        self.text_area.insert(tk.END, commands_text + "\n", "system")
        self.text_area.see(tk.END)
        
        self.speak("I've displayed all available commands")
    
    def wishme(self):
        """Greet user."""
        hour = datetime.datetime.now().hour
        if 4 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 16:
            greeting = "Good afternoon"
        elif 16 <= hour < 24:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.text_area.insert(tk.END, f"[System Initialized - OS: {self.os_type}]\n\n", "system")
        self.speak(f"Welcome back! {greeting}!")
        self.speak(f"{self.assistant_name} at your service. I'm listening continuously.")
        self.speak("Say 'help' to see what I can do, or 'exit' to stop me.")
    
    def takecommand(self):
        """Voice recognition - runs in listening thread."""
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.is_listening = True
                self.root.after(0, lambda: self.animate_listening())
                self.root.after(0, lambda: self.update_status("Listening...", "#fbbf24"))
                self.root.after(0, lambda: self.subtitle_label.config(text="🎤 Listening...", fg="#fbbf24"))
                
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = r.listen(source, timeout=5)
                self.root.after(0, lambda: self.update_status("Recognizing...", "#3b82f6"))
                self.root.after(0, lambda: self.subtitle_label.config(text="⚙️ Recognizing...", fg="#3b82f6"))
                
                query = r.recognize_google(audio, language="en-in")
                
                self.root.after(0, lambda: self.text_area.insert(tk.END, "You: ", "user"))
                self.root.after(0, lambda: self.text_area.insert(tk.END, f"{query}\n"))
                self.root.after(0, lambda: self.text_area.see(tk.END))
                
                self.is_listening = False
                return query.lower()
                
        except sr.WaitTimeoutError:
            self.is_listening = False
            self.root.after(0, lambda: self.update_status("Ready - Listening...", "#4ade80"))
            return None
        except sr.UnknownValueError:
            self.is_listening = False
            self.root.after(0, lambda: self.update_status("Ready - Listening...", "#4ade80"))
            return None
        except Exception as e:
            self.is_listening = False
            self.root.after(0, lambda: self.update_status("Ready - Listening...", "#4ade80"))
            return None

    def process_command(self, query):
        """Process commands - runs in background thread."""
        if not query:
            return False
        
        try:
            # Exit commands
            if any(word in query for word in ["exit", "offline", "quit", "goodbye", "bye", "go offline"]):
                self.speak("Going offline. Have a good day!")
                return True
            
            # Time
            elif "time" in query or "current time" in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                self.speak(f"The current time is {current_time}")
                self.root.after(0, lambda: self.text_area.insert(tk.END, f"🕒 {current_time}\n", "system"))
            
            # Date
            elif "date" in query or "today's date" in query:
                now = datetime.datetime.now()
                date_str = now.strftime("%A, %B %d, %Y")
                self.speak(f"The current date is {date_str}")
                self.root.after(0, lambda: self.text_area.insert(tk.END, f"📅 {date_str}\n", "system"))
            
            # News
            elif "news" in query or "headlines" in query:
                self.get_news()
            
            # Weather
            elif "weather" in query:
                city = query.replace("weather", "").replace("in", "").replace("at", "").strip()
                city = city.replace("what's the", "").replace("how's the", "").strip()
                self.get_weather(city if city else None)
            
            # Play YouTube Video - NEW FEATURE
            elif "play" in query and ("video" in query or "youtube" not in query):
                # Extract what to play
                play_query = query.replace("play", "").replace("video", "").replace("on youtube", "").strip()
                if play_query and play_query != "music":
                    self.play_youtube_video(play_query)
                elif "music" in query:
                    # Handle play music separately
                    pass
                else:
                    self.speak("What would you like me to play?")
            
            # YouTube Search
            elif "youtube" in query or ("search" in query and "youtube" in query):
                if "search youtube for" in query:
                    search_query = query.replace("search youtube for", "").strip()
                else:
                    search_query = query.replace("youtube", "").replace("search", "").replace("open", "").strip()
                
                if search_query:
                    self.search_youtube(search_query)
                else:
                    wb.open("https://youtube.com")
                    self.speak("Opening YouTube")
            
            # Wikipedia
            elif "wikipedia" in query:
                def _wiki_search():
                    search_query = query.replace("wikipedia", "").replace("search", "").replace("for", "").strip()
                    self.speak("Searching Wikipedia")
                    try:
                        result = wikipedia.summary(search_query, sentences=3)
                        self.speak("According to Wikipedia")
                        self.speak(result)
                        self.root.after(0, lambda: self.text_area.insert(tk.END, f"📚 {result}\n", "system"))
                    except:
                        self.speak("I couldn't find anything on Wikipedia for that topic")
                
                threading.Thread(target=_wiki_search, daemon=True).start()
            
            # Open website shortcuts
            elif "open youtube" in query and "search" not in query:
                self.speak("Opening YouTube")
                wb.open("https://youtube.com")
                self.root.after(0, lambda: self.text_area.insert(tk.END, "🔗 Opened YouTube\n", "system"))
            
            elif "open google" in query:
                self.speak("Opening Google")
                wb.open("https://google.com")
                self.root.after(0, lambda: self.text_area.insert(tk.END, "🔗 Opened Google\n", "system"))
            
            elif "open gmail" in query or "open mail" in query:
                self.speak("Opening Gmail")
                wb.open("https://gmail.com")
                self.root.after(0, lambda: self.text_area.insert(tk.END, "🔗 Opened Gmail\n", "system"))
            
            elif "open facebook" in query:
                self.speak("Opening Facebook")
                wb.open("https://facebook.com")
                self.root.after(0, lambda: self.text_area.insert(tk.END, "🔗 Opened Facebook\n", "system"))
            
            elif "open twitter" in query:
                self.speak("Opening Twitter")
                wb.open("https://twitter.com")
                self.root.after(0, lambda: self.text_area.insert(tk.END, "🔗 Opened Twitter\n", "system"))
            
            # Open applications
            elif "open" in query:
                app_name = query.replace("open", "").strip()
                if app_name and app_name not in ["youtube", "google", "gmail", "facebook", "twitter"]:
                    self.open_application(app_name)
            
            # Play music
            elif "play music" in query:
                def _play_music():
                    song_dir = os.path.expanduser("~\\Music")
                    try:
                        songs = os.listdir(song_dir)
                        if songs:
                            song = random.choice(songs)
                            os.startfile(os.path.join(song_dir, song))
                            self.speak(f"Playing {song}")
                            self.root.after(0, lambda: self.text_area.insert(tk.END, f"🎵 {song}\n", "system"))
                        else:
                            self.speak("No songs found in your Music folder")
                    except:
                        self.speak("Unable to access Music folder")
                
                threading.Thread(target=_play_music, daemon=True).start()
            
            # Screenshot
            elif "screenshot" in query or "screen shot" in query:
                def _take_screenshot():
                    self.speak("Taking screenshot")
                    img = pyautogui.screenshot()
                    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
                    img.save(img_path)
                    self.speak("Screenshot saved")
                    self.root.after(0, lambda: self.text_area.insert(tk.END, f"📸 Saved to {img_path}\n", "system"))
                
                threading.Thread(target=_take_screenshot, daemon=True).start()
            
            # Joke
            elif "joke" in query:
                joke = pyjokes.get_joke()
                self.speak(joke)
                self.root.after(0, lambda: self.text_area.insert(tk.END, f"😂 {joke}\n", "system"))
            
            # Calculator
            elif "calculate" in query or ("what is" in query and any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided'])):
                self.calculate(query)
            
            # Search
            elif "search" in query or ("google" in query and "open" not in query):
                search_query = query.replace("search", "").replace("google", "").replace("for", "").strip()
                if search_query:
                    self.speak(f"Searching for {search_query}")
                    wb.open(f"https://www.google.com/search?q={urllib.parse.quote_plus(search_query)}")
                    self.root.after(0, lambda: self.text_area.insert(tk.END, f"🔍 Searched: {search_query}\n", "system"))
                else:
                    self.speak("What would you like me to search for?")
            
            # Help command
            elif "help" in query or "what can you do" in query:
                self.show_commands_list()
            
            else:
                self.speak("I'm not sure how to help with that. Say 'help' to see what I can do.")
                
        except Exception as e:
            self.speak("An error occurred while processing your request")
            self.root.after(0, lambda: self.text_area.insert(tk.END, f"❌ Error: {e}\n", "system"))
        
        self.root.after(0, lambda: self.update_status("Ready - Listening...", "#4ade80"))
        return False

    def continuous_listening_loop(self):
        """Main continuous listening loop - runs in background thread."""
        while not self.should_stop:
            query = self.takecommand()
            if query:
                should_exit = self.process_command(query)
                if should_exit:
                    break
        
        # Exit after loop ends
        self.root.after(2000, self.cleanup_and_exit)

    def start_assistant(self):
        """Start the assistant with greeting and continuous listening."""
        self.wishme()
        
        # Start continuous listening in a separate thread
        self.continuous_thread = threading.Thread(target=self.continuous_listening_loop, daemon=True)
        self.continuous_thread.start()

    def stop_assistant(self):
        """Exit assistant."""
        self.should_stop = True
        self.speak("Shutting down. Goodbye!")
        self.root.after(2000, self.cleanup_and_exit)

    def cleanup_and_exit(self):
        """Clean up resources before exit."""
        try:
            self.engine.stop()
        except:
            pass
        self.root.quit()
        self.root.destroy()


# MAIN EXECUTION
def main():
    root = tk.Tk()
    app = EnhancedVoiceAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()