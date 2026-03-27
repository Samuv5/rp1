# 🤖 RP1 - Digital Companion

<p align="center">
  <img src="assets/banner.png" alt="RP1 Banner" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-GPL--3.0-green.svg" alt="License">
  <img src="https://img.shields.io/badge/AI-Model-gemma3:4b-orange.svg" alt="Model">
</p>

> **RP1** is an old-school 90s digital companion. Like a talking Tamagotchi or a Windows 95 PC with personality!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **Customizable Colors** | Yellow, Red, Blue, Green, Pink, Cyan |
| 🌐 **Bilingual** | Spanish and English |
| 🔊 **TTS Voice** | Text-to-speech with pyttsx3 |
| 💾 **Persistent Config** | Saved in `~/.rp1/config.json` |
| 🤖 **Local AI** | Uses Ollama with gemma3:4b |
| 🖥️ **Cross-Platform** | Linux, Mac, Windows |

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

## 📖 Usage

```bash
rp1
```

### Startup Options

| Command | Description |
|---------|-------------|
| `rp1 --voice` | Start with voice enabled |
| `rp1 --setup` | Download gemma3:4b model manually |

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

Config is saved in `~/.rp1/config.json`:

```json
{
  "color": "yellow",
  "language": "en"
}
```

---

## 📋 Requirements

- 🐍 Python 3.8+
- 🤖 Ollama
- 📦 gemma3:4b model
- 🔊 pyttsx3 (for voice)

---

## 📸 Screenshots

<details>
<summary>Click to see screenshots</summary>

### Startup Banner
```
=========================================
  🤖 RP1 - Digital Companion
=========================================
[system] model: gemma3:4b
[system] voice: disabled
[system] color: Yellow
[system] language: English

rp1: im rp1, an old digital companion...
```

### Changing Color
```
color > cyan

=========================================
  🤖 RP1 - Digital Companion
=========================================
[system] model: gemma3:4b
[system] voice: disabled
[system] color: Cyan
[system] language: English

rp1: color changed to Cyan
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
