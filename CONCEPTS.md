# Key Programming Concepts in KeyAssist

## 🎓 Lesson: Event-Driven Programming & Keyboard Handling

### What We Just Fixed

**The Problem:**
```python
AttributeError: 'HotKey' object has no attribute 'canonical'
```

**Why It Happened:**
The pynput library's `HotKey` class API changed, and the old `canonical()` method approach doesn't work in newer versions.

---

## Core Concept 1: Event-Driven Programming

### What is Event-Driven Programming?

Think of a doorbell:
- You don't constantly check if someone's at the door
- Instead, when someone presses the button, it TRIGGERS an event
- Your doorbell RESPONDS to that event by ringing

KeyAssist works the same way:
```
User presses key → Event triggered → Our code responds
```

### How It Works in Our Code

**Old Approach (Broken):**
```python
# Used pynput's HotKey helper with canonical()
hotkey = HotKey(HotKey.parse('<ctrl>+<alt>+x'), callback)
# This abstracted away the complexity but broke with new versions
```

**New Approach (Robust):**
```python
# We manually track which keys are pressed
current_keys = set()  # A collection of currently pressed keys

def on_press(key):
    current_keys.add(key)  # Add key when pressed
    if current_keys == {Ctrl, Alt, X}:  # Check if combo matches
        trigger_action()

def on_release(key):
    current_keys.remove(key)  # Remove key when released
```

---

## Core Concept 2: Sets and Set Operations

### What is a Set?

A **set** is a collection with NO duplicates and NO order:

```python
my_set = {1, 2, 3}
my_set.add(2)  # Still {1, 2, 3} - no duplicates!
my_set.add(4)  # Now {1, 2, 3, 4}
```

### Why We Use Sets for Key Tracking

**Perfect for tracking keys because:**
1. Each key can only be pressed once at a time
2. Order doesn't matter (Ctrl→Alt→X same as Alt→Ctrl→X)
3. Fast checking if combo is pressed

### Set Operations We Use

```python
# Define what keys we want
hotkey_combo = {Key.ctrl_l, Key.alt_l, KeyCode.from_char('x')}

# Current keys pressed
current_keys = {Key.ctrl_l, Key.alt_l, KeyCode.from_char('x'), Key.shift}

# Check if ALL hotkey keys are in current_keys
current_keys.issuperset(hotkey_combo)  # True!
# This means: "current_keys contains all of hotkey_combo"
```

**Visual Example:**
```
hotkey_combo     = {Ctrl, Alt, X}
current_keys     = {Ctrl, Alt, X, Shift}
                    ✓     ✓    ✓   (extra)

issuperset() → True (all required keys present)
```

---

## Core Concept 3: Filtering Unwanted Events

### The Problem: Too Many Events!

When you type, macOS sends events for EVERYTHING:
- Regular keys (a, b, c, x)
- Modifier keys (Ctrl, Alt, Cmd, Shift)
- Function keys (F1, F2, brightness, volume)
- Media keys (play, pause)
- Special keys (Caps Lock, Fn)

### Our Solution: Event Filtering

```python
def on_press(self, key):
    # FILTER 1: Ignore Command keys
    if key == Key.cmd or key == Key.cmd_l or key == Key.cmd_r:
        return  # Exit early - don't process this key

    # FILTER 2: Ignore Function keys (macOS-specific)
    if hasattr(key, 'vk') and 0xF700 <= key.vk <= 0xF8FF:
        return  # Virtual key codes in this range are function keys

    # Only process keys that passed filters
    self.current_keys.add(key)
```

### Key Concepts Here:

**1. Early Return Pattern:**
```python
if unwanted_condition:
    return  # Stop processing now
# Rest of code only runs if condition false
```

**2. Virtual Key Codes (vk):**
- Each key has a numeric code
- macOS function keys: 0xF700 to 0xF8FF (hexadecimal numbers)
- Example: F1 = 0xF704, Brightness Up = 0xF706

**3. hasattr() - Safe Attribute Checking:**
```python
hasattr(object, 'attribute_name')  # Returns True/False
# Safe way to check if object has an attribute
# Prevents errors if attribute doesn't exist
```

---

## Core Concept 4: Supporting Multiple Key Combinations

### Why Multiple Combos?

Keyboards have LEFT and RIGHT versions of keys:
- Left Ctrl vs Right Ctrl
- Left Alt vs Right Alt

Users might press any combination!

### Our Solution:

```python
# All possible valid combinations
self.hotkey_combo = {Key.ctrl_l, Key.alt_l, KeyCode.from_char('x')}
self.hotkey_combo_alt = {Key.ctrl_r, Key.alt_r, KeyCode.from_char('x')}
self.hotkey_combo_mixed1 = {Key.ctrl_l, Key.alt_r, KeyCode.from_char('x')}
self.hotkey_combo_mixed2 = {Key.ctrl_r, Key.alt_l, KeyCode.from_char('x')}

# Check if ANY combination matches
if (current_keys.issuperset(self.hotkey_combo) or
    current_keys.issuperset(self.hotkey_combo_alt) or
    current_keys.issuperset(self.hotkey_combo_mixed1) or
    current_keys.issuperset(self.hotkey_combo_mixed2)):
    trigger()
```

**Concept: OR Logic**
```
Combo1 OR Combo2 OR Combo3 OR Combo4
  ↓
If ANY is true → Execute
```

---

## Core Concept 5: Exception Handling (try/except)

### Why We Need It

Sometimes keys behave unexpectedly:
- Special keys might not have expected attributes
- Events might come in weird orders
- System might send malformed events

### The Pattern:

```python
try:
    # Try to do something that might fail
    if key == Key.cmd:
        return
except:
    # If ANY error happens, just continue
    pass
```

**What `pass` means:**
```python
pass  # Do nothing - empty placeholder
```

It's like saying "if this fails, that's okay, just keep going."

---

## Core Concept 6: State Management

### What is State?

**State** = data that changes over time

In KeyAssist:
```python
self.current_keys = set()  # This is our STATE
# It tracks: "what keys are currently pressed right now"
```

### State Changes:

```
Time 0: current_keys = {}              # Nothing pressed
Time 1: current_keys = {Ctrl}          # User presses Ctrl
Time 2: current_keys = {Ctrl, Alt}     # User presses Alt
Time 3: current_keys = {Ctrl, Alt, X}  # User presses X → TRIGGER!
Time 4: current_keys = {Ctrl, Alt}     # User releases X
Time 5: current_keys = {}              # User releases all
```

### Why Track State?

- Keyboard events come one at a time
- We need to REMEMBER what's pressed
- Check combinations across multiple events

---

## Visual Flow: From Key Press to Action

```
┌─────────────────────────────────────────────────┐
│ 1. User presses Ctrl                            │
│    on_press(Key.ctrl_l)                         │
│    current_keys = {Ctrl}                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. User presses Alt                             │
│    on_press(Key.alt_l)                          │
│    current_keys = {Ctrl, Alt}                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. User presses X                               │
│    on_press(KeyCode.from_char('x'))             │
│    current_keys = {Ctrl, Alt, X}                │
│                                                 │
│    CHECK: Does current_keys match hotkey?       │
│    {Ctrl, Alt, X} == {Ctrl, Alt, X} ✓           │
│                                                 │
│    → TRIGGER on_activate()                      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. on_activate() runs                           │
│    - Select all text (Cmd+A)                    │
│    - Copy (Cmd+C)                               │
│    - Send to Ollama                             │
│    - Get improved text                          │
│    - Paste (Cmd+V)                              │
└─────────────────────────────────────────────────┘
```

---

## Comparing Approaches

### Old Approach (Abstract but Fragile):
```python
hotkey = HotKey(HotKey.parse('<ctrl>+<alt>+x'), callback)
listener = Listener(
    on_press=lambda k: hotkey.press(hotkey.canonical(k)),
    on_release=lambda k: hotkey.release(hotkey.canonical(k))
)
```
**Pros:** Simple, clean
**Cons:** Breaks when library internals change

### New Approach (Manual but Robust):
```python
current_keys = set()
def on_press(key):
    current_keys.add(key)
    if current_keys.issuperset(hotkey_combo):
        trigger()
def on_release(key):
    current_keys.discard(key)
```
**Pros:** Full control, works across versions
**Cons:** More code to write

---

## Key Takeaways

1. **Event-Driven Programming**: Respond to events instead of constantly checking
2. **Sets**: Perfect for tracking unique items with no order
3. **Filtering**: Ignore unwanted events early (Command, Function keys)
4. **State Management**: Remember what's happening between events
5. **Exception Handling**: Gracefully handle unexpected situations
6. **Robustness vs Simplicity**: Sometimes manual control is better than clever abstractions

---

## Try It Yourself!

Want to change the hotkey? Edit these lines in `keyassist.py`:

```python
# Change 'x' to 'z' for Ctrl+Alt+Z
self.hotkey_combo = {Key.ctrl_l, Key.alt_l, keyboard.KeyCode.from_char('z')}
```

Want to add Shift to the combo? (Ctrl+Shift+Alt+X)
```python
self.hotkey_combo = {Key.ctrl_l, Key.alt_l, Key.shift, keyboard.KeyCode.from_char('x')}
```

Experiment and learn! 🚀
