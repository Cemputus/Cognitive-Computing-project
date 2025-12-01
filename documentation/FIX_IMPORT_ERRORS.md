# 🔧 Fix Import Errors in Jupyter Notebooks

## Quick Fix for Missing Packages

If you get `ModuleNotFoundError` in your Jupyter notebook:

### Solution 1: Install in Notebook (Fastest)

Add this at the **beginning** of Cell 1 (before other imports):

```python
!pip install vaderSentiment textblob gensim wordcloud
```

Then **restart the kernel** and run again.

### Solution 2: Install in Terminal

```bash
pip install vaderSentiment textblob gensim wordcloud
```

Then restart your Jupyter kernel.

### Solution 3: Check Python Environment

Your notebook kernel might be using a different Python than your terminal.

1. **In Jupyter Notebook:**
   - Check Python path: `import sys; print(sys.executable)`
   - Install using that path: `!{sys.executable} -m pip install vaderSentiment`

2. **Or restart kernel:**
   - Kernel → Restart & Clear Output
   - Then install: `!pip install vaderSentiment`

---

## Common Missing Packages

Based on the project, you may need:

```bash
pip install vaderSentiment textblob gensim wordcloud networkx scikit-learn
```

Or install all at once:

```bash
pip install -r requirements.txt
```

---

## Verify Installation

After installing, verify in a new cell:

```python
import vaderSentiment
from textblob import TextBlob
import gensim
import wordcloud
print("✅ All packages available!")
```

---

## If Still Having Issues

1. **Restart kernel** - This is often the solution!
2. **Check Python version** - Notebook might need Python 3.8+
3. **Use conda** if you have it: `conda install -c conda-forge vadersentiment`

**Most common fix: Restart the kernel after installing! 🔄**

