# 📝 How to Edit Jupyter Notebooks - Complete Guide

## ⚠️ Important: Don't Edit JSON Directly!

Jupyter Notebooks (`.ipynb` files) are JSON files, but **you should NEVER edit them directly as text/JSON**. Always use a proper notebook editor.

---

## ✅ Proper Ways to Edit Notebooks

### Method 1: Jupyter Notebook (Recommended)

**Step 1: Launch Jupyter**
```bash
jupyter notebook
```
This opens in your browser automatically (usually `http://localhost:8888`)

**Step 2: Navigate to your notebook**
- Click through folders: `notebooks` → `Milestone1`
- Click on `01_Data_Pipeline.ipynb` to open it

**Step 3: Edit cells**
- **Click on any cell** to select it
- **Double-click** to enter edit mode (or press `Enter`)
- **Type your changes**
- **Press `Shift + Enter`** to run and exit edit mode
- **Press `Esc`** to exit edit mode without running

**Step 4: Add new cells**
- Click `+` button in toolbar (or press `B` for below, `A` for above)
- Choose cell type: `Code` or `Markdown`

---

### Method 2: JupyterLab (Better Interface)

```bash
jupyter lab
```

**Advantages:**
- Better file browser
- Tabbed interface
- Split view for multiple files
- Integrated terminal

**Editing is the same as Jupyter Notebook**

---

### Method 3: VS Code (Best for Development)

**Step 1: Install Jupyter Extension**
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Jupyter"
4. Install "Jupyter" extension by Microsoft

**Step 2: Open Notebook**
1. File → Open Folder → Select your project folder
2. Navigate to `notebooks/Milestone1/`
3. Click on `01_Data_Pipeline.ipynb`

**Step 3: Edit**
- Click in any cell to edit
- Use toolbar buttons to run cells
- Much better for code editing!

---

### Method 4: Cursor IDE (If You're Using It)

If you're using Cursor IDE:

1. **Install Jupyter Extension:**
   - Open Extensions (Ctrl+Shift+X)
   - Search for "Jupyter"
   - Install it

2. **Open Notebook:**
   - Click on any `.ipynb` file
   - Cursor should recognize it as a notebook

3. **Edit Cells:**
   - Click in a cell to edit
   - Use the play buttons to run

---

## 🎯 Common Editing Tasks

### Adding a New Code Cell
1. Click on a cell
2. Press `B` (add cell below) or `A` (add cell above)
3. Or click the `+` button in toolbar
4. Type your code

### Adding a New Markdown Cell
1. Click on a cell
2. Press `M` to convert to Markdown
3. Or use dropdown to change cell type
4. Type your markdown text

### Editing Existing Cell
1. **Click on the cell** (single click)
2. **Double-click** or press `Enter` to enter edit mode
3. **Make your changes**
4. **Press `Shift + Enter`** to save and run

### Deleting a Cell
- Select cell
- Press `D` twice (DD) or click trash icon

### Moving Cells
- Select cell
- Use up/down arrow buttons in toolbar
- Or drag the cell

---

## ❌ What NOT to Do

### ❌ Don't Edit the JSON File Directly
**BAD:**
```json
// Opening 01_Data_Pipeline.ipynb in a text editor and editing the JSON
{
  "cells": [
    {
      "cell_type": "code",
      "source": ["print('hello')"]
    }
  ]
}
```

**This will:**
- Break the notebook format
- Lose cell outputs
- Cause errors
- Make the notebook unopenable

### ✅ Always Use a Notebook Editor
- Jupyter Notebook
- JupyterLab
- VS Code with Jupyter extension
- Cursor with Jupyter extension

---

## 🔧 Troubleshooting

### Problem: Notebook Won't Open
**Solution:**
1. Check if Jupyter is running: `jupyter notebook list`
2. Try opening in browser: `http://localhost:8888`
3. Check if file is corrupted (you'll need to restore from backup)

### Problem: Changes Not Saving
**Solution:**
1. Check if you're in edit mode (cell border should be blue/green)
2. Press `Ctrl+S` to save manually
3. Check file permissions (should be writable)

### Problem: Can't Run Cells
**Solution:**
1. Make sure kernel is selected (top right dropdown)
2. Try restarting kernel: `Kernel → Restart`
3. Check if Python environment is correct

### Problem: VS Code Shows JSON Instead of Notebook
**Solution:**
1. Install Jupyter extension
2. Right-click file → "Open With" → "Jupyter Notebook"
3. Or change default editor for `.ipynb` files

---

## 📋 Quick Reference

| Action | Shortcut |
|--------|----------|
| Run cell | `Shift + Enter` |
| Run cell and stay | `Ctrl + Enter` |
| Enter edit mode | `Enter` |
| Exit edit mode | `Esc` |
| Add cell below | `B` |
| Add cell above | `A` |
| Delete cell | `D` + `D` |
| Change to Markdown | `M` |
| Change to Code | `Y` |
| Save | `Ctrl + S` |
| Cut cell | `X` |
| Copy cell | `C` |
| Paste cell | `V` |

---

## ✅ Verification

To verify you're editing correctly:

1. **Open notebook in Jupyter:**
   ```bash
   jupyter notebook notebooks/Milestone1/01_Data_Pipeline.ipynb
   ```

2. **Make a small test edit:**
   - Click on Cell 1
   - Add a comment: `# Test edit`
   - Press `Shift + Enter`

3. **Save and check:**
   - The notebook should save automatically
   - Or press `Ctrl+S`
   - Refresh the file browser to see updated timestamp

---

## 🎓 Best Practices

1. **Always edit in Jupyter/VS Code** - Never edit JSON directly
2. **Save frequently** - Notebooks auto-save, but manual saves help
3. **Use markdown cells** - For documentation and explanations
4. **Organize your code** - Use clear section headers
5. **Run cells in order** - Don't skip around unless you know dependencies
6. **Clear outputs before committing** - Use "Clear All Outputs" in Jupyter

---

## 🚀 Quick Start

**To start editing right now:**

```bash
# Option 1: Jupyter Notebook
jupyter notebook

# Option 2: JupyterLab
jupyter lab

# Option 3: VS Code
code notebooks/Milestone1/01_Data_Pipeline.ipynb
```

Then click on any cell and start editing!

---

**Remember: If you can't edit, it's probably because you're viewing the notebook as a text file. Open it in Jupyter or VS Code instead! 🎯**

