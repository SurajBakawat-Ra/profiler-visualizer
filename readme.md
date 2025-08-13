python3 -m venv profiler-visualize

source profiler-visualize/bin/activate

pip install streamlit pandas matplotlib pyinstaller

which streamlit     

cp /Users/surajbakawat/Documents/Python/ProfilerDataVisualizer/profiler-visualize/bin/streamlit .

pyinstaller \
  --onefile \
  --add-data "visualizer.py:." \
  --add-data "streamlit:." \
  launch.py


./dist/launch

