# 🤖 JARVIS Voice Assistant

A powerful AI-powered voice assistant built with Python that can perform various tasks through voice commands. Features a beautiful animated GUI with continuous listening mode.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## ✨ Features

- 🎤 **Continuous Voice Recognition** - Always listening for your commands
- 🗣️ **Text-to-Speech** - Natural voice responses
- 🌐 **Web Integration** - Search Google, YouTube, Wikipedia
- 🎥 **YouTube Video Player** - Direct video playback
- 🌤️ **Weather Updates** - Real-time weather information
- 📰 **News Headlines** - Latest news from around the world
- 💻 **Application Launcher** - Open any installed application
- 📸 **Screenshot Capture** - Take and save screenshots
- 🧮 **Calculator** - Perform mathematical calculations
- 😂 **Entertainment** - Tell jokes and play music
- 🎨 **Animated GUI** - Beautiful visual feedback with animations

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Voice Commands](#-voice-commands)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Microphone access
- Internet connection (for most features)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/jarvis-voice-assistant.git
cd jarvis-voice-assistant
```

### Step 2: Platform-Specific Setup

#### 🪟 **Windows**

```bash
# Install dependencies
pip install -r requirements.txt

# If PyAudio fails, use pipwin
pip install pipwin
pipwin install pyaudio
```

#### 🐧 **Linux (Ubuntu/Debian)**

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio espeak python3-tk

# Install Python packages
pip install -r requirements.txt
```

#### 🍎 **macOS**

```bash
# Install system dependencies
brew install portaudio espeak

# Install Python packages
pip install -r requirements.txt
```

### Step 3: Configuration

Create an `assistant_name.txt` file in the project directory:

```bash
echo "Jarvis" > assistant_name.txt
```

---

## ⚙️ Configuration

### API Keys Setup

The assistant requires API keys for weather and news features. Replace these in the code:

1. **News API** (Free)
   - Sign up at [newsapi.org](https://newsapi.org)
   - Replace `NEWS_API_KEY` in the code with your key

2. **Weather API** (Free)
   - Sign up at [openweathermap.org](https://openweathermap.org/api)
   - Replace `WEATHER_API_KEY` in the code with your key

**Example:**
```python
NEWS_API_KEY = "your_news_api_key_here"
WEATHER_API_KEY = "your_weather_api_key_here"
```

---

## 🎯 Usage

### Starting the Assistant

```bash
python jarvis_assistant.py
```

Or on some systems:

```bash
python3 jarvis_assistant.py
```

### How It Works

1. **Launch** - Run the script to open the GUI
2. **Wait** - The assistant will greet you and start listening
3. **Speak** - Say your command clearly when you see "Listening..."
4. **Listen** - JARVIS will respond and execute your command
5. **Continue** - The assistant continues listening automatically

### Stopping the Assistant

Say any of these commands:
- "exit"
- "go offline"
- "goodbye"
- "quit"

Or click the **"STOP & EXIT"** button in the GUI.

---

## 🎤 Voice Commands

### 📅 Time & Date

| Command | Action |
|---------|--------|
| `"what time is it"` | Speaks current time |
| `"current time"` | Shows current time |
| `"what's the date"` | Speaks today's date |
| `"today's date"` | Shows current date |

### 🌤️ Weather

| Command | Action |
|---------|--------|
| `"weather in London"` | Gets weather for London |
| `"what's the weather in Paris"` | Gets weather for Paris |
| `"how's the weather"` | Asks for city, then shows weather |

### 📰 News

| Command | Action |
|---------|--------|
| `"news"` | Reads top 5 headlines |
| `"headlines"` | Shows latest news |
| `"latest news"` | Gets current news |

### 🎥 YouTube & Media

| Command | Action |
|---------|--------|
| `"play Despacito"` | **🆕 Plays video directly** |
| `"play Python tutorial"` | **🆕 Plays first matching video** |
| `"search youtube for cats"` | Opens YouTube search results |
| `"open youtube"` | Opens YouTube homepage |
| `"play music"` | Plays random song from Music folder |

### 🔍 Search & Information

| Command | Action |
|---------|--------|
| `"wikipedia artificial intelligence"` | Searches and reads Wikipedia |
| `"search wikipedia for Python"` | Gets Wikipedia summary |
| `"search quantum computing"` | Google search |
| `"google machine learning"` | Opens Google search |
| `"open google"` | Opens Google homepage |
| `"open gmail"` | Opens Gmail |
| `"open facebook"` | Opens Facebook |
| `"open twitter"` | Opens Twitter |

### 💻 Applications

| Command | Action |
|---------|--------|
| `"open notepad"` | Opens Notepad (Windows) |
| `"open calculator"` | Opens Calculator |
| `"open chrome"` | Opens Google Chrome |
| `"open firefox"` | Opens Firefox |
| `"open vscode"` | Opens Visual Studio Code |
| `"open terminal"` | Opens Terminal/CMD |
| `"open paint"` | Opens Paint (Windows) |

**Supported Applications by OS:**

**Windows:** Notepad, Calculator, Paint, CMD, Task Manager, Chrome, Edge, Firefox, VSCode, Excel, Word, PowerPoint, Outlook, File Explorer

**macOS:** Safari, Chrome, Firefox, Notes, Calculator, Mail, Calendar, Finder, Terminal

**Linux:** Firefox, Chrome, Terminal, Calculator, Files, Text Editor

### 🎯 Productivity

| Command | Action |
|---------|--------|
| `"take screenshot"` | Captures and saves screenshot |
| `"screenshot"` | Takes screenshot |
| `"tell me a joke"` | Tells a random joke |
| `"calculate 15 plus 27"` | Performs calculation |
| `"what is 100 divided by 5"` | Mathematical operation |

**Calculator Operations:**
- Addition: "plus" or "+"
- Subtraction: "minus" or "-"
- Multiplication: "times" or "multiplied by"
- Division: "divided by"

### 🛠️ System

| Command | Action |
|---------|--------|
| `"help"` | Shows all available commands |
| `"what can you do"` | Displays command list |
| `"exit"` | Stops the assistant |
| `"go offline"` | Shuts down |
| `"goodbye"` | Exits program |

---

## 💡 Tips for Best Results

1. **Speak Clearly** - Enunciate your words clearly
2. **Wait for "Listening..."** - Speak when you see the listening indicator
3. **Reduce Background Noise** - Use in a quiet environment
4. **Use Specific Commands** - Be precise with your requests
5. **Check Microphone** - Ensure your mic is working and permitted
6. **Internet Connection** - Required for most online features

---

## 🐛 Troubleshooting

### Issue: PyAudio Installation Fails

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

Or download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### Issue: No Microphone Detected

1. Check system microphone permissions
2. Ensure microphone is not being used by another application
3. Test microphone in system settings
4. Restart the application

### Issue: Text-to-Speech Not Working

**Windows:** Check Windows Speech settings

**Linux:** Install espeak
```bash
sudo apt-get install espeak
```

**macOS:** Check System Preferences > Accessibility > Speech

### Issue: "Listening..." but Not Recognizing

1. Speak closer to the microphone
2. Reduce background noise
3. Check internet connection (Google Speech Recognition requires internet)
4. Adjust `r.pause_threshold` in code (currently 1 second)

### Issue: GUI Not Appearing

**Linux:**
```bash
sudo apt-get install python3-tk
```

### Issue: Application Won't Open

1. Verify application is installed
2. Check if application name matches supported list
3. Try using the full application name
4. Check OS compatibility

### Issue: API Features Not Working (Weather/News)

1. Verify API keys are correctly set
2. Check internet connection
3. Ensure API quota is not exceeded
4. Verify API key is active

---

## 📁 Project Structure

```
jarvis-voice-assistant/
│
├── jarvis_assistant.py          # Main application file
├── requirements.txt             # Python dependencies
├── assistant_name.txt          # Assistant name configuration
├── README.md                   # This file
│
└── (Optional directories)
    ├── Pictures/               # Screenshots saved here
    └── Music/                  # Music folder for playback
```

---

## 🔧 Customization

### Change Assistant Name

Edit `assistant_name.txt`:
```
Friday
```

### Change Voice

Edit in code:
```python
# Change voice (0 = male, 1 = female, usually)
self.engine.setProperty('voice', voices[0].id)

# Change speech rate (default 150)
self.engine.setProperty('rate', 180)

# Change volume (0.0 to 1.0)
self.engine.setProperty('volume', 0.9)
```

### Add Custom Commands

Add to `process_command()` method:
```python
elif "custom command" in query:
    self.speak("Executing custom command")
    # Your custom code here
```

---

## 🌟 Features Overview

| Feature | Status | Description |
|---------|--------|-------------|
| Voice Recognition | ✅ | Google Speech Recognition |
| Text-to-Speech | ✅ | pyttsx3 engine |
| Continuous Listening | ✅ | Always listening mode |
| Animated GUI | ✅ | Tkinter with animations |
| YouTube Player | ✅ | Direct video playback |
| Weather API | ✅ | OpenWeatherMap integration |
| News API | ✅ | NewsAPI integration |
| Wikipedia | ✅ | Wikipedia search & summary |
| Calculator | ✅ | Mathematical operations |
| App Launcher | ✅ | Cross-platform support |
| Screenshot | ✅ | PyAutoGUI capture |
| Web Search | ✅ | Google search integration |

---

## 📝 Requirements

```
Python 3.8+
pyttsx3==2.90
SpeechRecognition==3.10.0
PyAudio==0.2.14
wikipedia==1.4.0
beautifulsoup4==4.12.2
requests==2.31.0
pyautogui==0.9.54
pyjokes==0.6.0
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Google Speech Recognition API
- OpenWeatherMap API
- NewsAPI
- Wikipedia API
- Python Community

---

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an issue on GitHub
3. Contact: your.email@example.com

---

## 🚀 Quick Start Guide

```bash
# 1. Clone repository
git clone https://github.com/yourusername/jarvis-voice-assistant.git
cd jarvis-voice-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure assistant name
echo "Jarvis" > assistant_name.txt

# 4. Run the assistant
python jarvis_assistant.py

# 5. Say "help" to see all commands
```

---

**Made with ❤️ by [Your Name]**

**⭐ Star this repository if you find it helpful!**