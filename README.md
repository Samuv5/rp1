# RP1 - Digital Companion

RP1 is an old-school 90s style digital companion chatbot. Think of it as a talking Tamagotchi or a Windows 95 PC with personality.

## Features

- Retro 90s chatbot personality
- Text-to-speech voice support
- Customizable colors (Yellow, Red, Blue, Green, Pink, Cyan)
- Bilingual support (English/Spanish)
- Uses Ollama with gemma3:4b model
- Persistent configuration

## Installation

### Linux / Mac

```bash
chmod +x install.sh
./install.sh
```

### Windows

```batch
install.bat
```

## Usage

```bash
rp1
```

### Options

| Command | Description |
|---------|-------------|
| `rp1 --voice` | Start with voice enabled |
| `rp1 --setup` | Download gemma3:4b model manually |

### In-App Commands

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `voice` | Toggle voice on/off |
| `color` | Change robot color |
| `lang` | Change language |
| `config` | Show current settings |
| `exit` | Exit RP1 |

## Requirements

- Python 3.8+
- Ollama
- gemma3:4b model
- pyttsx3 (for voice)

## Configuration

Config is stored in `~/.rp1/config.json`:

```json
{
  "color": "yellow",
  "language": "es"
}
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

Samuv5
