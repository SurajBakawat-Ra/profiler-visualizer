import os
import sys
import subprocess

def get_resource_path(filename):
    # For PyInstaller, to access files added with --add-data
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return filename

# Absolute path to bundled analyzer.py
analyzer_path = get_resource_path("visualizer.py")

# Use relative streamlit in virtual env (bundled manually)
streamlit_path = get_resource_path("streamlit")

# Run the streamlit app
subprocess.run([streamlit_path, "run", analyzer_path])
