# Troubleshooting Guide

## Understanding Common Errors

### ✅ FIXED: Threading Error with Python 3.13

**Error Message:**
```
TypeError: '_thread._ThreadHandle' object is not callable
```

**What Happened:**
- **Root Cause**: Python 3.13 changed internal threading implementation
- **Why It Failed**: pynput 1.7.6 was written for older Python versions
- **The Fix**: Upgraded to pynput 1.8.1 which supports Python 3.13

**Key Concepts Learned:**

1. **Version Compatibility**: Libraries must be compatible with your Python version
2. **Threading**: Python uses threads to run multiple tasks simultaneously (like listening for keyboard events)
3. **Breaking Changes**: Sometimes Python updates change how things work internally
4. **Semantic Versioning**:
   - `1.7.6` = Major.Minor.Patch
   - `1.8.1` = Minor version bump usually means "new features + bug fixes"

**How to Fix Similar Issues:**
```bash
# Check what version you have
pip list | grep library_name

# Upgrade to latest
pip install --upgrade library_name

# Or specify a version
pip install library_name==2.0.0
```

---

## Other Common Issues

### 1. "Cannot connect to Ollama"

**Symptom:**
```
Error: Cannot connect to Ollama
```

**Diagnosis:**
Ollama service isn't running

**Fix:**
```bash
# Start Ollama in a separate terminal
ollama serve
```

**Concept:** Ollama is a **server** that runs in the background. KeyAssist is a **client** that sends requests to it.

---

### 2. "Model not found"

**Symptom:**
```
Warning: gemma3:1b not found
```

**Diagnosis:**
Model hasn't been downloaded

**Fix:**
```bash
# Download the model (one-time setup)
ollama pull gemma3:1b

# Check what models you have
ollama list
```

**Concept:** AI models are large files (hundreds of MB to GB). You must download them before use.

---

### 3. "Nothing happens when I press Control+Option+X"

**Possible Causes:**

**A. No Accessibility Permissions**

**Fix:**
1. System Preferences → Security & Privacy → Privacy → Accessibility
2. Add Terminal (or Python.app) to the allowed list
3. Restart KeyAssist

**Concept:** macOS requires explicit permission for apps to monitor keyboard/mouse events (security feature)

**B. KeyAssist Not Running**

Check if you see:
```
KeyAssist is running...
Press Control+Option+X to improve text
```

If not, run: `./start.sh`

**C. Wrong Application Context**

Some apps (like system apps or protected apps) may block keyboard automation.

---

### 4. "Text Gets Mangled or Weird"

**Symptom:**
Text is replaced but looks wrong or incomplete

**Causes:**
- Timing issues (text changed too fast)
- Clipboard conflicts (another app using clipboard)
- Model giving poor output

**Fix:**
```python
# In keyassist.py, increase sleep times:
time.sleep(0.2)  # Change to 0.3 or 0.5
```

**Concept:** Keyboard automation needs small delays between actions to ensure the OS processes each command.

---

## Debugging Tips

### 1. Check the Terminal Output

KeyAssist prints what it's doing:
```
=== KeyAssist Triggered ===
Original: hey whats up
Sending to Ollama: hey whats up...
Improved text: Hello, what's up?
✓ Text improved and replaced!
```

### 2. Test Ollama Separately

```bash
# Test if Ollama is responding
curl http://localhost:11434/api/tags

# Test generation
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:1b",
  "prompt": "Fix this text: hey whats up",
  "stream": false
}'
```

### 3. Test Keyboard Events

```python
# Simple test script
from pynput import keyboard

def on_press(key):
    print(f"Key pressed: {key}")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
```

---

## Performance Tuning

### Speed vs Quality Trade-offs

**Use gemma3:270m for:**
- ✓ Faster responses (smaller model)
- ✓ Lower memory usage
- ✗ Less accurate with complex slang

**Use gemma3:1b for:**
- ✓ Better accuracy
- ✓ More natural output
- ✗ Slightly slower (1-2 seconds first time)

**Change model in keyassist.py:**
```python
self.model = "gemma3:270m"  # Fast
# or
self.model = "gemma3:1b"    # Accurate
```

### Adjust Temperature

Temperature controls randomness (in keyassist.py):
```python
"temperature": 0.3  # More consistent (current)
"temperature": 0.7  # More creative
"temperature": 0.1  # Very consistent
```

---

## Learning Resources

### Understanding the Code Flow

```
User presses Ctrl+Option+X
         ↓
HotKey.parse() detects the combination
         ↓
on_activate() function is called
         ↓
Select all text (Cmd+A)
         ↓
Copy text (Cmd+C)
         ↓
Get text from clipboard
         ↓
Send to Ollama API
         ↓
Get improved text
         ↓
Put in clipboard
         ↓
Paste (Cmd+V)
```

### Key Python Concepts Used

1. **Classes**: `KeyAssist` is a class that bundles data + functions
2. **Threading**: Background listener for keyboard events
3. **HTTP Requests**: Talking to Ollama API
4. **Event Handlers**: Functions that run when events happen
5. **Context Managers**: `with` statements for resource management

---

## Still Stuck?

1. Check Python version: `python3 --version`
2. Check if venv is activated: Look for `(venv)` in prompt
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Try running the test script: `python3 -c "import pynput; print('OK')"`

Need more help? Check the code comments in `keyassist.py`!
