# 🤖 RP1 - Digital Companion

<p align="center">
  <img src="assets/banner.png" alt="RP1 Banner" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-GPL--3.0-green.svg" alt="License">
  <img src="https://img.shields.io/badge/AI-Local%20%7C%20Cloud-blue.svg" alt="AI">
</p>

> **RP1** is an old-school 90s digital companion. Like a talking Tamagotchi or a Windows 95 PC with personality!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **Customizable Colors** | Yellow, Red, Blue, Green, Pink, Cyan |
| 🌐 **Bilingual** | Spanish and English |
| 🔊 **TTS Voice** | Text-to-speech with pyttsx3 |
| 🤖 **AI Modes** | Local (Ollama) or Cloud (API Keys) |
| 💾 **Persistent Config** | Saved in `~/.rp1/config.json` |
| 🖥️ **Cross-Platform** | Linux, Mac, Windows |

---

## 📋 System Requirements

### Minimum Requirements

| Component | Local AI | Cloud AI |
|-----------|----------|----------|
| **OS** | Linux / macOS / Windows | Linux / macOS / Windows |
| **Python** | 3.8+ | 3.8+ |
| **RAM** | 4 GB | 2 GB |
| **Disk** | 5 GB free (for ai model) | 500 MB |
| **GPU** | Optional (recommended for local) | Not required |

### For Local AI (Ollama)

- **RAM**: 4GB minimum (8GB recommended)
- **GPU**: NVIDIA GPU with CUDA (optional, but recommended)
- **Disk**: 5GB for models

### For Cloud AI (API)

- **OpenAI API Key** or **Anthropic API Key**
- Internet connection

---

## 🚀 Installation

### Linux / macOS

```bash
git clone https://github.com/Samuv5/rp1.git
cd rp1
chmod +x install.sh
./install.sh
```

### Windows

```batch
git clone https://github.com/Samuv5/rp1.git
cd rp1
install.bat
```

### 📦 Direct Download

Download the AppImage from [Releases](https://github.com/Samuv5/rp1/releases):

```bash
chmod +x RP1.AppImage
./RP1.AppImage
```

---

## 🤖 AI Setup Options

During installation, choose your AI mode:

### 1. Local (Ollama) - FREE
- Uses local models (gemma3:4b)
- No internet required
- Private (all data stays on your machine)
- Requires more RAM

### 2. Cloud (API Key) - Pay per use
- **OpenAI** - GPT-4o Mini
- **Anthropic** - Claude 3.5 Sonnet
- Requires internet
- Lower resource usage

---

## 📖 Usage

```bash
rp1
```

### Startup Options

| Command | Description |
|---------|-------------|
| `rp1 --voice` | Start with voice enabled |
| `rp1 --setup` | Download Ollama models (local mode only) |

### In-App Commands

| Command | Description |
|---------|-------------|
| `help` 📋 | Show available commands |
| `voice` 🔊 | Toggle voice on/off |
| `color` 🎨 | Change robot color |
| `lang` 🌐 | Change language (es/en) |
| `config` ⚙️ | Show current settings |
| `reload` 🔄 | Reload with new settings |
| `exit` 🚪 | Exit RP1 |

---

## 🎮 Available Colors

```
┌─────────────────────────────────────┐
│  🟡 Yellow   🔴 Red    🔵 Blue     │
│  🟢 Green    🩷 Pink   🔵 Cyan     │
└─────────────────────────────────────┘
```

---

## 🌐 Languages

| Code | Language |
|------|----------|
| `es` | Spanish 🇲🇽 🇪🇸 |
| `en` | English 🇺🇸 🇬🇧 |

---

## 📁 Project Structure

```
RP1/
├── src/
│   └── rp1.py          # Source code
├── install.sh           # Linux/Mac installer
├── install.bat          # Windows installer
├── RP1.AppImage        # Portable AppImage
├── README.md           # Documentation
├── LICENSE             # GPL-3.0
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Configuration

Config files are saved in `~/.rp1/`:

```bash
~/.rp1/config.json     # UI settings (color, language)
~/.rp1/ai_config.json # AI mode (local/cloud)
~/.rp1/api_config.json # API keys (if cloud mode)
```

---

## 📋 Requirements

### For All Modes

- 🐍 Python 3.8+
- 🔊 pyttsx3 (for voice)
- 🌐 Internet (for cloud mode)

### For Local AI Mode

- 🤖 Ollama
- 📦 gemma3:4b model
- 💾 4GB+ RAM

### For Cloud AI Mode

- 🔑 OpenAI API Key OR
- 🔑 Anthropic API Key

---

## 📸 Screenshots

<details>
<summary>Click to see screenshots</summary>

### Startup Banner
```
╭─────────────────────────────────────────────╮
│          🤖 RP1 - Digital Companion          │
╰─────────────────────────────────────────────╯

┌─ INFO ────────────────────────────────┐
│  📦 Model: gemma3:4b
│  🔇 Voice: disabled
│  🎨 Color: Yellow
│  🌐 Lang: English
│  🤖 AI: local (Ollama)
│  💡 type 'help' for commands
└──────────────────────────────────────┘

rp1: im rp1, an old digital companion...
```

### Help Menu
```
╭─────────────────────────────────────────────╮
│              📋 COMMANDS                   │
╰─────────────────────────────────────────────╯

┌─ COMMANDS ────────────────────────────┐
│  🔊 voice  - toggle voice on/off
│  🎨 color  - change robot color
│  🌐 lang   - change language
│  ⚙️  config - show current settings
│  🔄 reload - reload with new settings
│  🚪 exit   - exit rp1
└──────────────────────────────────────┘
```

</details>

---

## 📜 License

This project is under the **GNU General Public License v3.0**

See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Samuv5** - [GitHub](https://github.com/Samuv5)

---

<p align="center">
  🤖 Made with ❤️ and Python
</p>
