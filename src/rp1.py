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

COLORS = {
    "yellow": {"name": "\033[1;33m", "label": "Yellow"},
    "red": {"name": "\033[1;31m", "label": "Red"},
    "blue": {"name": "\033[1;34m", "label": "Blue"},
    "green": {"name": "\033[1;32m", "label": "Green"},
    "pink": {"name": "\033[1;35m", "label": "Pink"},
    "cyan": {"name": "\033[1;36m", "label": "Cyan"},
}

LANGUAGES = {
    "es": {"name": "Español", "prompt": "system_es"},
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
        "cmd_voz": "voz   - activar/desactivar voz",
        "cmd_color": "color - cambiar color del robot",
        "cmd_lang": "lang   - cambiar idioma",
        "cmd_config": "config - ver configuracion actual",
        "cmd_exit": "exit  - salir",
        "cmd_ayuda": "ayuda - mostrar comandos",
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
        "closing": "rp1: cerrando sesion... hasta luego!",
        "sistema": "[sistema]",
        "model": "modelo:",
        "voice_status": "voz:",
        "not_found": "modelo no encontrado. ejecuta 'rp1 --setup' primero.",
        "tu": "tu > ",
        "rp1_prefix": "rp1: ",
    },
    "en": {
        "welcome": "im rp1, an old digital companion. i have a tamagotchi named bits. how are you?",
        "help_title": "available commands:",
        "cmd_voz": "voice - toggle voice on/off",
        "cmd_color": "color - change robot color",
        "cmd_lang": "lang   - change language",
        "cmd_config": "config - show current settings",
        "cmd_exit": "exit  - exit rp1",
        "cmd_ayuda": "help  - show commands",
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
        "closing": "rp1: closing session... bye!",
        "sistema": "[system]",
        "model": "model:",
        "voice_status": "voice:",
        "not_found": "model not found. run 'rp1 --setup' first.",
        "tu": "you > ",
        "rp1_prefix": "rp1: ",
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
    def __init__(self, config):
        self.config = config
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
        print(f"{C}========================================={R}")
        print(f"{C}  RP1 - Digital Companion{R}")
        print(f"{C}========================================={R}")
        print(f"{C}{self.get_text('sistema')}{R} {self.get_text('model')} {OLLAMA_MODEL}")
        voice_status = self.get_text('voz_on') if self.tts.enabled else self.get_text('voz_off')
        print(f"{C}{self.get_text('sistema')}{R} {self.get_text('voice_status')} {voice_status}")
        print(f"{C}{self.get_text('sistema')}{R} {self.get_text('config_color')} {COLORS[self.config.color]['label']}")
        print(f"{C}{self.get_text('sistema')}{R} {self.get_text('config_lang')} {LANGUAGES[self.config.language]['name']}")
        print(f"{C}{self.get_text('sistema')}{R} type 'help' for commands")
        print()
        print(f"{C}rp1: {R}{self.get_text('welcome')}")

    def show_help(self):
        C = self.get_color()
        R = "\033[0m"
        print(f"{C}{self.get_text('help_title')}{R}")
        print(f"  {self.get_text('cmd_voz')}")
        print(f"  {self.get_text('cmd_color')}")
        print(f"  {self.get_text('cmd_lang')}")
        print(f"  {self.get_text('cmd_config')}")
        print(f"  reload - reload with new settings")
        print(f"  {self.get_text('cmd_exit')}")

    def cmd_color(self):
        C = self.get_color()
        R = "\033[0m"
        print(f"{C}{self.get_text('color_prompt')}{R}")
        for key, val in COLORS.items():
            print(f"  {key}: {val['label']}")
        new_color = input(f"{C}color > {R}").strip().lower()
        if self.config.set_color(new_color):
            print(f"{C}rp1: {R}{self.get_text('color_changed')} {COLORS[new_color]['label']}")
        else:
            print(f"{C}rp1: {R}{self.get_text('color_invalid')}")

    def cmd_lang(self):
        C = self.get_color()
        R = "\033[0m"
        print(f"{C}{self.get_text('lang_prompt')}{R}")
        for key, val in LANGUAGES.items():
            print(f"  {key}: {val['name']}")
        new_lang = input(f"{C}lang > {R}").strip().lower()
        if self.config.set_language(new_lang):
            self.tts.init_engine(new_lang)
            print(f"{C}rp1: {R}{self.get_text('lang_changed')} {LANGUAGES[new_lang]['name']}")
        else:
            print(f"{C}rp1: {R}{self.get_text('lang_invalid')}")

    def cmd_config(self):
        C = self.get_color()
        R = "\033[0m"
        print(f"{C}{self.get_text('config_title')}{R}")
        print(f"  {self.get_text('config_color')} {COLORS[self.config.color]['label']}")
        print(f"  {self.get_text('config_lang')} {LANGUAGES[self.config.language]['name']}")

    def chat(self):
        C = self.get_color()
        R = "\033[0m"
        self.show_banner()

        while True:
            try:
                user_input = input(f"{C}{self.get_text('tu')}{R}")
            except EOFError:
                break

            cmd = user_input.strip().lower()

            if cmd in ["exit", "salir", "quit"]:
                print(f"{C}rp1: {R}{self.get_text('closing')}")
                break

            if cmd in ["voz", "voice"]:
                enabled = self.tts.toggle()
                msg = self.get_text('voz_on') if enabled else self.get_text('voz_off')
                print(f"{C}{self.get_text('sistema')}{R} {msg}")
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
                print(f"{C}[system]{R} reloading...")
                os.execv(sys.executable, [sys.executable, __file__])

            if not user_input.strip():
                continue

            self.conversation_history.append(f"user: {user_input}")
            print(f"{C}{self.get_text('thinking')}{R}", end=" ", flush=True)

            try:
                history = "\n".join(self.conversation_history[-5:])
                full_prompt = f"{self.get_system_prompt()}\n\n{history}\nrp1:"

                result = subprocess.run(
                    ["curl", "-s", "http://localhost:11434/api/generate",
                     "-d", json.dumps({"model": OLLAMA_MODEL, "prompt": full_prompt, "stream": False})],
                    capture_output=True, text=True, timeout=120
                )
                data = json.loads(result.stdout)
                response = data.get("response", "sin respuesta")

                self.conversation_history.append(f"rp1: {response}")

                print("\r" + " " * 25 + "\r", end="")
                print(f"{C}{self.get_text('rp1_prefix')}{R}{response}")

                if self.tts.enabled:
                    self.tts.speak(response)

            except subprocess.TimeoutExpired:
                print("\r" + " " * 25 + "\r", end="")
                print(f"{C}{self.get_text('error')}{R} timeout")
            except Exception as e:
                print("\r" + " " * 25 + "\r", end="")
                print(f"{C}{self.get_text('error')}{R} {e}")


def check_ollama():
    try:
        result = subprocess.run(["curl", "-s", "http://localhost:11434"], capture_output=True, timeout=5)
        if result.returncode != 0:
            print("[error] Ollama is not running. Start it with: ollama serve")
            return False
    except:
        print("[error] Ollama is not running. Start it with: ollama serve")
        return False
    return True


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

    if not check_ollama():
        sys.exit(1)

    config = Config()
    rp1 = RP1(config)
    rp1.tts.enabled = args.voice
    rp1.chat()


if __name__ == "__main__":
    main()
