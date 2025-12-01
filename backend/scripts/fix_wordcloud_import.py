"""
Quick script to verify wordcloud installation and help fix import issues
"""
import sys

print("=" * 60)
print("WordCloud Installation Check")
print("=" * 60)

print(f"\nPython executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Try importing wordcloud
try:
    import wordcloud
    print(f"\n✅ WordCloud is installed!")
    print(f"   Version: {wordcloud.__version__}")
    print(f"   Location: {wordcloud.__file__}")
except ImportError as e:
    print(f"\n❌ WordCloud is NOT installed in this Python environment")
    print(f"   Error: {e}")
    print(f"\n💡 Solution:")
    print(f"   1. In your Jupyter notebook, run:")
    print(f"      !pip install wordcloud")
    print(f"   2. Or restart kernel and try again")
    print(f"   3. Or check if you're using a virtual environment")

# Check if it's in requirements
try:
    with open('requirements.txt', 'r') as f:
        if 'wordcloud' in f.read():
            print(f"\n✅ WordCloud is listed in requirements.txt")
        else:
            print(f"\n⚠️  WordCloud is NOT in requirements.txt (but should be)")
except:
    pass

print("\n" + "=" * 60)

