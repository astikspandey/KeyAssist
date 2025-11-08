# Quick Start Guide

## 🚀 Start KeyAssist

```bash
./start.sh
```

Or manually:
```bash
source venv/bin/activate
python keyassist.py
```

## 📝 How to Use

1. **Open any text application** (Notes, TextEdit, browser, Slack, etc.)

2. **Type some text with slang/shortforms:**
   ```
   hey whats up gonna meet u tmrw at 5pm
   ```

3. **Press `Control+Option+X`**

4. **Watch your text transform:**
   ```
   Hey, how about we meet at 5 pm tomorrow?
   ```

## ✨ Examples

| Before | After |
|--------|-------|
| `u r awesome thx` | `You are awesome, thank you` |
| `gonna call u asap` | `Going to call you as soon as possible` |
| `cant wait 2 see u` | `Can't wait to see you` |
| `plz help me with this rly quick` | `Please help me with this really quickly` |

## ⚠️ First Time Setup

When you run KeyAssist for the first time, macOS will ask for **Accessibility permissions**:

1. Go to **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
2. Click the lock to make changes
3. Add **Terminal** (or **Python**) to the list
4. Restart KeyAssist

## 🛑 Stop KeyAssist

Press `Control+C` in the terminal where KeyAssist is running.

## 💡 Tips

- The shortcut works in **any application** that supports standard keyboard shortcuts
- The first request may take 1-2 seconds as the model loads
- Subsequent requests are much faster
- Your clipboard content is preserved
- If nothing happens, make sure you have text in the current field
