# 📝 Editing Notebooks in Cursor IDE

## Quick Fix for Cursor

If you're using **Cursor IDE** and can't edit notebooks:

### Step 1: Install Jupyter Extension

1. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac) to open Extensions
2. Search for **"Jupyter"**
3. Install **"Jupyter"** by Microsoft
4. **Restart Cursor** after installation

### Step 2: Open Notebook Properly

1. **Click** on `notebooks/Milestone1/01_Data_Pipeline.ipynb` in the file explorer
2. It should open as an **interactive notebook** (not JSON)
3. You should see:
   - Cells with borders
   - Code/Markdown dropdown
   - Run buttons (▶️)
   - Output areas

### Step 3: Edit Cells

**To edit existing cell:**
- Click inside the cell
- Start typing
- Changes save automatically

**To add new cell:**
- Click the **+ Code** or **+ Markdown** button at the top
- Or press `Ctrl+Shift+;` for new cell

**To change cell type:**
- Click the cell type dropdown (Code/Markdown)
- Select the type you want

---

## If Notebook Opens as JSON

If the notebook shows raw JSON instead of cells:

1. **Right-click** on the file
2. Select **"Open With..."**
3. Choose **"Jupyter Notebook"** or **"Notebook Editor"**

Or:

1. Go to **File → Preferences → Settings**
2. Search for **"jupyter"**
3. Set default editor for `.ipynb` files to **"Jupyter Notebook"**

---

## Alternative: Use Jupyter in Browser

If Cursor isn't working:

```bash
jupyter notebook
```

Then:
- Browser opens automatically
- Navigate to your notebook
- Edit normally
- Changes save automatically

---

## Verify It's Working

**You should see:**
- ✅ Cells with visible borders
- ✅ Code editor when clicking in a cell
- ✅ Run button (▶️) on each cell
- ✅ Output area below cells
- ✅ Cell type selector (Code/Markdown)

**You should NOT see:**
- ❌ Raw JSON text
- ❌ `{"cells": [...]}` code
- ❌ Just text editor

---

## Still Not Working?

1. **Check Jupyter extension is installed:**
   - Extensions → Search "Jupyter" → Should show "Installed"

2. **Try reloading window:**
   - `Ctrl+Shift+P` → "Reload Window"

3. **Check Python interpreter:**
   - Bottom right of Cursor → Click Python version
   - Select correct Python environment

4. **Use Jupyter in browser instead:**
   ```bash
   jupyter notebook notebooks/Milestone1/01_Data_Pipeline.ipynb
   ```

---

**The notebook IS editable - you just need the right editor interface! 🎯**

