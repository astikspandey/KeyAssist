#!/usr/bin/env python3
"""
KeyAssist - A keyboard assistant that fixes text using Ollama's Gemma3 model
Trigger with Control+Option+X to improve selected or recently typed text
"""

import json
import time
import pyperclip
import requests
from pynput import keyboard
from pynput.keyboard import Key, Controller, HotKey
from AppKit import NSWorkspace


class KeyAssist:
    def __init__(self):
        self.controller = Controller()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:3b"  # Better instruction-following than gemma

        # Track which keys are currently pressed
        self.current_keys = set()

        # Debouncing - prevent multiple triggers
        self.last_trigger_time = 0
        self.debounce_seconds = 1  # Wait 1 second between triggers
        self.is_processing = False  # Flag to prevent re-triggering while processing

        # Define the hotkey combination: Ctrl + Alt + X
        self.hotkey_combo = {Key.ctrl_l, Key.alt_l, keyboard.KeyCode.from_char('x')}
        # Also support right ctrl/alt
        self.hotkey_combo_alt = {Key.ctrl_r, Key.alt_r, keyboard.KeyCode.from_char('x')}
        self.hotkey_combo_mixed1 = {Key.ctrl_l, Key.alt_r, keyboard.KeyCode.from_char('x')}
        self.hotkey_combo_mixed2 = {Key.ctrl_r, Key.alt_l, keyboard.KeyCode.from_char('x')}

    def improve_text(self, text):
        """Send text to Ollama Gemma3 model for improvement"""
        if not text.strip():
            return text

        # Simple completion prompt for qwen2.5
        prompt = f"""Rewrite in proper English with all slang expanded:

{text}

Rewritten:"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.3
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            improved_text = result.get('response', '').strip()
            return improved_text

        except:
            # Silently fail and return original text
            return text

    def on_activate(self):
        """Called when Control+Option+X is pressed"""
        # Prevent re-triggering while already processing
        if self.is_processing:
            return

        self.is_processing = True

        # Check active application
        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        app_name = active_app['NSApplicationName']

        if app_name in ['Terminal', 'iTerm2', 'iTerm']:
            # Silently ignore if Terminal is active
            self.is_processing = False
            return

        # Debounce - ignore if triggered too recently
        current_time = time.time()
        if current_time - self.last_trigger_time < self.debounce_seconds:
            self.is_processing = False
            return
        self.last_trigger_time = current_time

        # Wait longer to ensure we stay in the target app
        time.sleep(0.5)

        # Double-check we're still in the right app
        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        app_name = active_app['NSApplicationName']

        if app_name in ['Terminal', 'iTerm2', 'iTerm']:
            # Focus shifted to terminal, abort
            return

        # Save current clipboard
        original_clipboard = pyperclip.paste() or ""

        # Select all text in the current field
        with self.controller.pressed(Key.cmd):
            self.controller.tap('a')

        time.sleep(0.5)

        with self.controller.pressed(Key.cmd):
            self.controller.tap('c')

        time.sleep(0.6)

        # Get the copied text
        text = pyperclip.paste()

        if text and text.strip():
            # Improve the text
            improved_text = self.improve_text(text)

            if improved_text and improved_text != text:
                # Put improved text in clipboard
                pyperclip.copy(improved_text)

                # Paste it back
                time.sleep(0.2)
                with self.controller.pressed(Key.cmd):
                    self.controller.tap('v')

                # Click to deselect and position cursor at end
                time.sleep(0.2)
                self.controller.tap(Key.right)

                # Restore original clipboard after a delay
                time.sleep(0.2)
                pyperclip.copy(original_clipboard)
            else:
                # Restore original clipboard
                pyperclip.copy(original_clipboard)
        else:
            # Restore original clipboard
            pyperclip.copy(original_clipboard)

        # Reset processing flag
        self.is_processing = False

    def on_press(self, key):
        """Called when any key is pressed"""
        # Ignore Cmd and Function keys
        try:
            if key == Key.cmd or key == Key.cmd_l or key == Key.cmd_r:
                return  # Ignore Command keys
            if hasattr(key, 'vk') and 0xF700 <= key.vk <= 0xF8FF:
                return  # Ignore function keys (macOS specific)
        except:
            pass

        # Add key to currently pressed set
        self.current_keys.add(key)

        # Check if hotkey combination is pressed
        if (self.current_keys.issuperset(self.hotkey_combo) or
            self.current_keys.issuperset(self.hotkey_combo_alt) or
            self.current_keys.issuperset(self.hotkey_combo_mixed1) or
            self.current_keys.issuperset(self.hotkey_combo_mixed2)):
            self.on_activate()

    def on_release(self, key):
        """Called when any key is released"""
        # Remove key from currently pressed set
        try:
            self.current_keys.discard(key)
        except:
            pass

    def start(self):
        """Start listening for the keyboard shortcut"""
        print("KeyAssist is running...")
        print("Press Control+Option+X to improve text")
        print("Press Control+C to exit\n")

        # Test Ollama connection
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            print(f"Connected to Ollama. Available models: {model_names}")

            if not any(self.model in name for name in model_names):
                print(f"\nWarning: {self.model} not found. Available models: {model_names}")
                print(f"Run: ollama pull {self.model}")
        except Exception as e:
            print(f"Warning: Could not connect to Ollama: {e}")
            print("Make sure Ollama is running with: ollama serve")

        # Listen for keyboard events
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                print("\nKeyAssist stopped")


def main():
    assistant = KeyAssist()
    assistant.start()


if __name__ == "__main__":
    main()
