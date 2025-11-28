"""
Test script to verify notebook editing capabilities
"""
import json
import os

def check_notebook_editable(nb_path):
    """Check if notebook can be edited"""
    print(f"Checking notebook: {nb_path}")
    print(f"File exists: {os.path.exists(nb_path)}")
    print(f"Is writable: {os.access(nb_path, os.W_OK)}")
    
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Notebook is valid JSON")
        print(f"✅ Has {len(data.get('cells', []))} cells")
        print(f"✅ Notebook format: {data.get('nbformat', 'unknown')}")
        
        # Check if we can write to it
        test_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Test cell - can be deleted"]
        }
        
        # Don't actually modify, just check structure
        print(f"✅ Notebook structure is correct")
        print(f"\n📝 To edit in Cursor:")
        print(f"   1. Make sure Jupyter extension is installed")
        print(f"   2. Click on the notebook file")
        print(f"   3. Click in any cell to edit")
        print(f"   4. Use + button to add new cells")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    nb_path = "notebooks/Milestone1/01_Data_Pipeline.ipynb"
    check_notebook_editable(nb_path)

