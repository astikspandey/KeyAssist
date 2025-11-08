# KeyAssist

A macOS keyboard assistant that automatically improves your text using AI. Press `Control+Option+X` to fix spelling, grammar, expand slang/shortforms, and make your text more professional.

## Features

- **One time Config**: Only needs 20 seconds to initialize the first time, smooth sailing onwards
- **Smart Text Improvement**: Uses Ollama's Gemma model to fix text
- **Works Everywhere**: Works in any text field across all applications
- **Keyboard Shortcut**: Simple `Control+Option+X` trigger
- **Expands Slang**: Converts shortforms like "u" → "you", "gonna" → "going to"
- **Grammar & Spelling**: Fixes common mistakes automatically

## Requirements

- macOS
- Python 3.7+
- Ollama installed and running

## Installation

1. **Install Ollama** (if not already installed):
   ```bash
   brew install ollama
   ```

2. **Start Ollama service**:
   ```bash
   ollama serve
   ```

3. **Pull the Gemma model** (in a new terminal):
   ```bash
   ollama pull gemma3:1b
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Grant Accessibility Permissions**:
   - Go to System Preferences → Security & Privacy → Privacy → Accessibility
   - Add Terminal (or your Python app) to the allowed list
   - You may need to run the script first to trigger the permission request

## Usage

1. **Start KeyAssist**:
   ```bash
   python keyassist.py
   ```

2. **Use it**:

   **Option A - Improve selected text (recommended):**
   - Type some text in any application (TextEdit, Notes, WhatsApp, browser, etc.)
   - Select the specific text you want to improve
   - Press `Control+Option+X`
   - Your selected text will be automatically improved and replaced!

   **Option B - Improve all text in field:**
   - Type some text without selecting anything
   - Press `Control+Option+X`
   - ALL text in the current field will be improved and replaced

   💡 **Tip**: For best results when improving multiple times, manually select only the new text you want to improve. This prevents re-processing already-improved text.

3. **Stop KeyAssist**:
   - Press `Control+C` in the terminal where it's running

## Examples

### Social Media Slang
**Before**: "ngl this app slaps fr fr, lowkey the goat no cap"
**After**: "This application is exceptionally well-executed and impressive. It presents a genuinely authentic and compelling experience."

### Gen Z Chat
**Before**: "omg idk what 2 do rn, hmu asap thx"
**After**: "I am currently uncertain about the next steps. Please contact me as soon as possible, thank you."

### Professional Context
**Before**: "tbh ur work is bussin, imo u deserve a raise fr"
**After**: "Considering your work is exceptionally strong, I believe you deserve a salary increase."

### Casual Text
**Before**: "wya? lmk when ur free bc we need 2 talk"
**After**: "Where are you? I need to connect with you soon; we require a conversation."

### All Slang Types Supported
- **Texting**: u, ur, y, bc, tmrw, rn, thx, pls, msg, 2day, 2nite, b4, l8r
- **Social**: idk, idc, tbh, ngl, imo, fyi, btw, lmk, hmu, wya
- **Reactions**: omg, lol, lmao, smh, gg, np
- **Gen Z**: fr, ong, lowkey, highkey, slaps, bussin, sus, mid, no cap, bet, goat, slay, vibe
- **Apps**: dm, rt, ily, fomo, yolo, tbt, icymi

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if the service is accessible: `curl http://localhost:11434/api/tags`

### "Model not found"
- Pull the Gemma model: `ollama pull gemma3:1b`

### "Nothing happens when I press the shortcut"
- Check Accessibility permissions in System Preferences
- Make sure KeyAssist is running in the terminal
- Try selecting text manually before pressing the shortcut

### Want to use a different model?
Edit `keyassist.py` and change the `self.model` line:
```python
self.model = "gemma3:1b"  # Change to your preferred model (e.g., gemma3:270m for faster/smaller)
```

## How it Works

1. When you press `Control+Option+X`, KeyAssist:
   - Selects all text in the current field (`Cmd+A`)
   - Copies it to clipboard (`Cmd+C`)
   - Sends it to Ollama's Gemma model with improvement instructions
   - Pastes the improved text back (`Cmd+V`)

## Notes

- The first improvement may take a few seconds as the model loads
- Subsequent improvements are much faster
- Your original clipboard content is preserved
- Works best with text fields that support standard keyboard shortcuts
# KeyAssist
