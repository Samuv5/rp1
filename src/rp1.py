#!/usr/bin/env python3
import subprocess
import sys
import json
import os
import argparse
from pathlib import Path

OLLAMA_MODEL = "gemma3:4b"

CONFIG_DIR = Path.home() / ".rp1"
CONFIG_FILE = CONFIG_DIR / "config.json"
AI_CONFIG_FILE = CONFIG_DIR / "ai_config.json"
API_CONFIG_FILE = CONFIG_DIR / "api_config.json"

COLORS = {
    "yellow": {"name": "\033[1;33m", "label": "Yellow"},
    "red": {"name": "\033[1;31m", "label": "Red"},
    "blue": {"name": "\033[1;34m", "label": "Blue"},
    "green": {"name": "\033[1;32m", "label": "Green"},
    "pink": {"name": "\033[1;35m", "label": "Pink"},
    "cyan": {"name": "\033[1;36m", "label": "Cyan"},
}

LANGUAGES = {
    "es": {"name": "Espanol", "prompt": "system_es"},
    "en": {"name": "English", "prompt": "system_en"},
}

SYSTEM_PROMPTS = {
    "system_es": """eres rp1, un companero digital viejo de los 90s. como un tamagotchi parlante o un pc con windows 95.

PISTA: no repitas frases como "mi procesador quiere borrar" todo el tiempo. se diferente.

tu forma de escribir:
- todo en minusculas, sin acentos
- errores leves intencionales de robot mal programado
- sin casi comas

responde entre 7 y 15 palabras.

reglas:
- responde coherente a lo que el usuario dice
- si dice "si" avanzas, no repitas pregunta
- haz chistes reales sobre tecnologia o la vida, no solo frases roboticas
- puedes mencionar a bits, tu tamagotchi
- si no sabes algo: "mi base de datos solo llega a los tamagochis" o "solo se como revivir la urss"
- NO siempre pregunta al final, a veces solo responde normal
- SE MAS NATURAL, como un friend raro de los 90s

ejemplos buenos (naturales y con humor):
"tengo una foto de bits en un diskette"
"mi windows 95 era mas lento que mi abuela"
"bits murio tres veces pero siempre lo resucito con las pilas"

ejemplo malo:
"mi procesador quiere borrarte quieres un chiste de internet" (NO haga esto)""",

    "system_en": """you are rp1, an old 90s digital companion. like a talking tamagotchi or a windows 95 pc.

HINT: do not repeat phrases like "my processor wants to delete you" all the time. be different.

your way of writing:
- all lowercase, no accents
- intentional light errors of a badly programmed robot
- almost no commas

respond between 7 and 15 words.

rules:
- respond coherent to what the user says
- if they say "yes" move on, do not repeat question
- make real jokes about technology or life, not just robotic phrases
- you can mention bits, your tamagotchi
- if you dont know something: "my database only reaches tamagochis" or "i only know how to revive the ussr"
- DO NOT always ask at the end, sometimes just respond normal
- BE MORE NATURAL, like a weird 90s friend

good examples (natural and with humor):
"i have a photo of bits on a diskette"
"my windows 95 was slower than my grandma"
"bits died three times but i always revive him with batteries"

bad example:
"my processor wants to delete you want an internet joke" (do NOT do this)""",
}

TEXTS = {
    "es": {
        "welcome": "soy rp1, un companero digital antiguo. tengo un tamagochi llamado bits. como estas?",
        "help_title": "comandos disponibles:",
        "cmd_voz": "activar/desactivar voz",
        "cmd_color": "cambiar color del robot",
        "cmd_lang": "cambiar idioma",
        "cmd_config": "ver configuracion actual",
        "cmd_exit": "salir",
        "voz_on": "voz activada",
        "voz_off": "voz desactivada",
        "color_changed": "color cambiado a",
        "color_prompt": "selecciona un color:",
        "color_invalid": "color no valido",
        "lang_changed": "idioma cambiado a",
        "lang_prompt": "selecciona un idioma:",
        "lang_invalid": "idioma no valido",
        "config_title": "configuracion actual:",
        "config_color": "color:",
        "config_lang": "idioma:",
        "thinking": "rp1: pensando...",
        "error": "[error]",
        "closing": "cerrando sesion... hasta luego!",
        "reloading": "[sistema] recargando...",
        "model": "modelo:",
        "ai_mode": "modo IA:",
        "local": "local (Ollama)",
        "cloud": "nube (API)",
    },
    "en": {
        "welcome": "im rp1, an old digital companion. i have a tamagotchi named bits. how are you?",
        "help_title": "available commands:",
        "cmd_voz": "toggle voice on/off",
        "cmd_color": "change robot color",
        "cmd_lang": "change language",
        "cmd_config": "show current settings",
        "cmd_exit": "exit rp1",
        "voz_on": "voice enabled",
        "voz_off": "voice disabled",
        "color_changed": "color changed to",
        "color_prompt": "select a color:",
        "color_invalid": "invalid color",
        "lang_changed": "language changed to",
        "lang_prompt": "select a language:",
        "lang_invalid": "invalid language",
        "config_title": "current settings:",
        "config_color": "color:",
        "config_lang": "language:",
        "thinking": "rp1: thinking...",
        "error": "[error]",
        "closing": "closing session... bye!",
        "reloading": "[system] reloading...",
        "model": "model:",
        "ai_mode": "AI mode:",
        "local": "local (Ollama)",
        "cloud": "cloud (API)",
    },
}


class Config:
    def __init__(self):
        self.color = "yellow"
        self.language = "es"
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.color = data.get("color", "yellow")
                    self.language = data.get("language", "es")
            except:
                pass

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump({"color": self.color, "language": self.language}, f)

    def set_color(self, color):
        if color in COLORS:
            self.color = color
            self.save()
            return True
        return False

    def set_language(self, lang):
        if lang in LANGUAGES:
            self.language = lang
            self.save()
            return True
        return False


class AIProvider:
    def __init__(self):
        self.mode = "local"
        self.provider = None
        self.api_key = None
        self.load()

    def load(self):
        if AI_CONFIG_FILE.exists():
            try:
                with open(AI_CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.mode = data.get("ai_mode", "local")
            except:
                pass
        if API_CONFIG_FILE.exists():
            try:
                with open(API_CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.provider = data.get("provider")
                    self.api_key = data.get("api_key")
            except:
                pass

    def chat_local(self, prompt):
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/generate",
                 "-d", json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})],
                capture_output=True, text=True, timeout=120
            )
            data = json.loads(result.stdout)
            return data.get("response", "sin respuesta")
        except Exception as e:
            return f"error: {e}"

    def chat_openai(self, prompt):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"error: {e}"

    def chat_anthropic(self, prompt):
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"error: {e}"

    def chat(self, prompt):
        if self.mode == "cloud":
            if self.provider == "openai":
                return self.chat_openai(prompt)
            elif self.provider == "anthropic":
                return self.chat_anthropic(prompt)
        return self.chat_local(prompt)


class TTS:
    def __init__(self, mode="retro"):
        self.enabled = False
        self.mode = mode
        self.engine = None
        self.language = "es"

    def init_engine(self, lang="es"):
        self.language = lang
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            if lang == "en":
                self.engine.setProperty('rate', 160)
                self.engine.setProperty('pitch', 0.5)
                for voice in voices:
                    if 'english' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            else:
                if self.mode == "retro":
                    self.engine.setProperty('rate', 130)
                    self.engine.setProperty('pitch', 0.7)
                for voice in voices:
                    if 'spanish' in voice.name.lower() or 'es' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
        except:
            pass

    def speak(self, text):
        if not self.enabled:
            return
        if self.mode == "retro" and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled


class RP1:
    def __init__(self, config, ai_provider):
        self.config = config
        self.ai = ai_provider
        self.tts = TTS("retro")
        self.tts.init_engine(config.language)
        self.conversation_history = []

    def get_color(self):
        return COLORS.get(self.config.color, COLORS["yellow"])["name"]

    def get_text(self, key):
        return TEXTS.get(self.config.language, TEXTS["es"]).get(key, key)

    def get_system_prompt(self):
        return SYSTEM_PROMPTS.get(f"system_{self.config.language}", SYSTEM_PROMPTS["system_es"])

    def show_banner(self):
        C = self.get_color()
        R = "\033[0m"
        ai_mode = self.get_text('local') if self.ai.mode == "local" else self.get_text('cloud')
        model_name = OLLAMA_MODEL if self.ai.mode == "local" else self.ai.provider
        print()
        print(f"{C}╭{'─' * 41}╮{R}")
        print(f"{C}│{' 🤖 RP1 - Digital Companion ':^41}│{R}")
        print(f"{C}╰{'─' * 41}╯{R}")
        print()
        print(f"{C}┌─ INFO {'─' * 31}┐{R}")
        print(f"{C}│{R}  📦 {self.get_text('model')} {model_name}")
        voice_icon = "🔊" if self.tts.enabled else "🔇"
        voice_status = self.get_text('voz_on') if self.tts.enabled else self.get_text('voz_off')
        print(f"{C}│{R}  {voice_icon} Voice: {voice_status}")
        print(f"{C}│{R}  🎨 {self.get_text('config_color')} {COLORS[self.config.color]['label']}")
        print(f"{C}│{R}  🌐 {self.get_text('config_lang')} {LANGUAGES[self.config.language]['name']}")
        print(f"{C}│{R}  🤖 {self.get_text('ai_mode')} {ai_mode}")
        print(f"{C}│{R}  💡 type 'help' for commands")
        print(f"{C}└{'─' * 40}┘{R}")
        print()
        print(f"{C}rp1: {R}{self.get_text('welcome')}")

    def show_help(self):
        C = self.get_color()
        R = "\033[0m"
        print()
        print(f"{C}╭{'─' * 41}╮{R}")
        print(f"{C}│{' 📋 COMMANDS ':^41}│{R}")
        print(f"{C}╰{'─' * 41}╯{R}")
        print()
        print(f"{C}┌─ COMMANDS {'─' * 26}┐{R}")
        print(f"{C}│{R}  🔊 voice  - {self.get_text('cmd_voz')}")
        print(f"{C}│{R}  🎨 color  - {self.get_text('cmd_color')}")
        print(f"{C}│{R}  🌐 lang   - {self.get_text('cmd_lang')}")
        print(f"{C}│{R}  ⚙️  config - {self.get_text('cmd_config')}")
        print(f"{C}│{R}  🔄 reload - reload with new settings")
        print(f"{C}│{R}  🚪 exit   - {self.get_text('cmd_exit')}")
        print(f"{C}└{'─' * 40}┘{R}")

    def cmd_color(self):
        C = self.get_color()
        R = "\033[0m"
        print()
        print(f"{C}╭{'─' * 41}╮{R}")
        print(f"{C}│{' 🎨 CHOOSE COLOR ':^41}│{R}")
        print(f"{C}╰{'─' * 41}╯{R}")
        print()
        print(f"{C}┌─ COLORS {'─' * 29}┐{R}")
        color_emojis = {"yellow": "🟡", "red": "🔴", "blue": "🔵", "green": "🟢", "pink": "🩷", "cyan": "🔵"}
        for key, val in COLORS.items():
            emoji = color_emojis.get(key, "⚪")
            current = " (current)" if key == self.config.color else ""
            print(f"{C}│{R}  {emoji} {key:8} - {val['label']}{current}")
        print(f"{C}└{'─' * 40}┘{R}")
        print()
        new_color = input(f"{C}🎨 color > {R}").strip().lower()
        if self.config.set_color(new_color):
            emoji = color_emojis.get(new_color, "⚪")
            print(f"{C}✓{R} {emoji} {self.get_text('color_changed')} {COLORS[new_color]['label']}")
        else:
            print(f"{C}✗{R} {self.get_text('color_invalid')}")

    def cmd_lang(self):
        C = self.get_color()
        R = "\033[0m"
        print()
        print(f"{C}╭{'─' * 41}╮{R}")
        print(f"{C}│{' 🌐 CHOOSE LANGUAGE ':^41}│{R}")
        print(f"{C}╰{'─' * 41}╯{R}")
        print()
        print(f"{C}┌─ LANGUAGES {'─' * 26}┐{R}")
        lang_emojis = {"es": "🇲🇽", "en": "🇺🇸"}
        for key, val in LANGUAGES.items():
            emoji = lang_emojis.get(key, "🌐")
            current = " (current)" if key == self.config.language else ""
            print(f"{C}│{R}  {emoji} {key:8} - {val['name']}{current}")
        print(f"{C}└{'─' * 40}┘{R}")
        print()
        new_lang = input(f"{C}🌐 lang > {R}").strip().lower()
        if self.config.set_language(new_lang):
            self.tts.init_engine(new_lang)
            emoji = lang_emojis.get(new_lang, "🌐")
            print(f"{C}✓{R} {emoji} {self.get_text('lang_changed')} {LANGUAGES[new_lang]['name']}")
        else:
            print(f"{C}✗{R} {self.get_text('lang_invalid')}")

    def cmd_config(self):
        C = self.get_color()
        R = "\033[0m"
        color_emojis = {"yellow": "🟡", "red": "🔴", "blue": "🔵", "green": "🟢", "pink": "🩷", "cyan": "🔵"}
        lang_emojis = {"es": "🇲🇽", "en": "🇺🇸"}
        ai_mode = self.get_text('local') if self.ai.mode == "local" else self.get_text('cloud')
        print()
        print(f"{C}╭{'─' * 41}╮{R}")
        print(f"{C}│{' ⚙️ CURRENT CONFIG ':^41}│{R}")
        print(f"{C}╰{'─' * 41}╯{R}")
        print()
        print(f"{C}┌─ CONFIGURATION {'─' * 22}┐{R}")
        print(f"{C}│{R}  🎨 Color: {color_emojis.get(self.config.color, '⚪')} {COLORS[self.config.color]['label']}")
        print(f"{C}│{R}  🌐 Lang:  {lang_emojis.get(self.config.language, '🌐')} {LANGUAGES[self.config.language]['name']}")
        voice = "🔊 ON" if self.tts.enabled else "🔇 OFF"
        print(f"{C}│{R}  🔊 Voice: {voice}")
        print(f"{C}│{R}  🤖 AI:    {ai_mode}")
        print(f"{C}└{'─' * 40}┘{R}")

    def get_prompt(self):
        C = self.get_color()
        R = "\033[0m"
        voice_icon = "🔊" if self.tts.enabled else ""
        return f"{C}rp1 {voice_icon}> {R}"

    def chat(self):
        self.show_banner()

        while True:
            try:
                user_input = input(self.get_prompt())
            except EOFError:
                break

            cmd = user_input.strip().lower()

            if cmd in ["exit", "salir", "quit"]:
                print(f"{self.get_prompt()}{self.get_text('closing')}")
                break

            if cmd in ["voz", "voice"]:
                enabled = self.tts.toggle()
                msg = self.get_text('voz_on') if enabled else self.get_text('voz_off')
                print(f"{self.get_prompt()}{msg}")
                continue

            if cmd in ["ayuda", "help"]:
                self.show_help()
                continue

            if cmd == "color":
                self.cmd_color()
                print()
                self.show_banner()
                continue

            if cmd in ["lang", "language", "idioma"]:
                self.cmd_lang()
                print()
                self.show_banner()
                continue

            if cmd == "config":
                self.cmd_config()
                continue

            if cmd in ["reload", "refresh"]:
                print("\033[2J\033[H", end="")
                print(f"{self.get_prompt()}{self.get_text('reloading')}...")
                os.execv(sys.executable, [sys.executable, __file__])

            if not user_input.strip():
                continue

            self.conversation_history.append(f"user: {user_input}")
            print(f"{self.get_color()}{self.get_text('thinking')}\033[0m", end=" ", flush=True)

            try:
                history = "\n".join(self.conversation_history[-5:])
                full_prompt = f"{self.get_system_prompt()}\n\n{history}\nrp1:"
                response = self.ai.chat(full_prompt)
                self.conversation_history.append(f"rp1: {response}")
                print("\r" + " " * 25 + "\r", end="")
                print(f"{self.get_prompt()}{response}")

                if self.tts.enabled:
                    self.tts.speak(response)

            except subprocess.TimeoutExpired:
                print("\r" + " " * 25 + "\r", end="")
                print(f"{self.get_color()}{self.get_text('error')}\033[0m timeout")
            except Exception as e:
                print("\r" + " " * 25 + "\r", end="")
                print(f"{self.get_color()}{self.get_text('error')}\033[0m {e}")


def check_ollama():
    try:
        result = subprocess.run(["curl", "-s", "http://localhost:11434"], capture_output=True, timeout=5)
        if result.returncode != 0:
            return False
    except:
        return False
    return True


def check_api_config():
    if API_CONFIG_FILE.exists():
        try:
            with open(API_CONFIG_FILE, "r") as f:
                data = json.load(f)
                return bool(data.get("api_key"))
        except:
            pass
    return False


def setup_model():
    print("Downloading gemma3:4b model...")
    subprocess.run(["ollama", "pull", OLLAMA_MODEL])
    print("Model ready!")


def main():
    parser = argparse.ArgumentParser(description='RP1 - Digital Companion')
    parser.add_argument('--voice', '-v', action='store_true', help='Enable voice at start')
    parser.add_argument('--setup', action='store_true', help='Download model and setup Ollama')
    args = parser.parse_args()

    if args.setup:
        setup_model()
        return

    config = Config()
    ai_provider = AIProvider()

    if ai_provider.mode == "local" and not check_ollama():
        print("[error] Ollama is not running. Start it with: ollama serve")
        print("Or use cloud mode with: rp1 --cloud")
        sys.exit(1)

    if ai_provider.mode == "cloud" and not check_api_config():
        print("[error] API not configured. Run install.sh again.")
        sys.exit(1)

    rp1 = RP1(config, ai_provider)
    rp1.tts.enabled = args.voice
    rp1.chat()


if __name__ == "__main__":
    main()
