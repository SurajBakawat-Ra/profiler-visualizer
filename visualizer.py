import streamlit as st
import pandas as pd
import json

def render_analysis_summary(analysis: dict):
    st.header("📊 Performance Summary")

    st.markdown(f"**Grade**: {analysis.get('grade', '-')}")
    st.markdown(f"**Bottleneck**: {analysis.get('bottleneck', '-')}")

    # FPS
    st.subheader("🎮 FPS")
    st.markdown(f"- **Average FPS**: {analysis.get('averageFPS', 0):.2f}")
    st.markdown(f"- **Min FPS**: {analysis.get('minFPS', 0):.2f}")
    st.markdown(f"- **Max FPS**: {analysis.get('maxFPS', 0):.2f}")
    st.markdown(f"- **FPS Std. Dev**: {analysis.get('fpsStandardDeviation', 0):.2f}")

    # CPU/GPU
    st.subheader("🧠 CPU / GPU")
    st.markdown(f"- **Avg CPU Main Thread Time**: {analysis.get('averageMainThreadTimeMs', 0):.3f} ms")
    st.markdown(f"- **Avg CPU Render Thread Time**: {analysis.get('averageRenderThreadTimeMs', 0):.3f} ms")
    st.markdown(f"- **Avg GPU Time**: {analysis.get('averageGpuFrameTimeMs', 0):.3f} ms")
    st.markdown(f"- **Max GPU Time**: {analysis.get('maxGpuFrameTimeMs', 0):.3f} ms")

    # Memory
    st.subheader("💾 Memory")
    st.markdown(f"- **Max Memory Usage**: {analysis.get('maxMemoryUsageKB', 0) / 1024:.2f} MB")
    st.markdown(f"- **Avg GC Allocated / Frame**: {analysis.get('averageGcAllocatedInFrameKB', 0):.2f} KB")
    st.markdown(f"- **Avg GC Reserved**: {analysis.get('averageGcReservedMB', 0):.2f} MB")
    st.markdown(f"- **Avg System Used**: {analysis.get('averageSystemUsedMB', 0):.2f} MB")

    # Rendering
    st.subheader("🖼️ Rendering")
    st.markdown(f"- **Avg Draw Calls**: {analysis.get('averageDrawCalls', 0):.2f}")
    st.markdown(f"- **Avg Batches**: {analysis.get('averageBatchCount', 0):.2f}")
    st.markdown(f"- **Avg Triangles**: {analysis.get('averageTriangleCount', 0):.2f}")
    st.markdown(f"- **Avg Vertices**: {analysis.get('averageVertexCount', 0):.2f}")
    st.markdown(f"- **Avg Shadow Casters**: {analysis.get('averageShadowCasterCount', 0):.2f}")

    # Audio
    st.subheader("🔊 Audio")
    st.markdown(f"- **Avg Audio Used Memory**: {analysis.get('averageAudioUsedMemoryMB', 0):.2f} MB")
    st.markdown(f"- **Avg Audio Reserved Memory**: {analysis.get('averageAudioReservedMemoryMB', 0):.2f} MB")
    st.markdown(f"- **Avg Audio Clip Memory**: {analysis.get('averageAudioClipMemoryMB', 0):.2f} MB")
    st.markdown(f"- **Avg Audio Clip Count**: {analysis.get('averageAudioClipCount', 0):.2f}")
    st.markdown(f"- **Avg Audio Reads**: {analysis.get('averageAudioReads', 0)}")

    # UI
    st.subheader("🧩 UI")
    st.markdown(f"- **Avg UI Layout Time**: {analysis.get('averageUILayoutMs', 0):.3f} ms")
    st.markdown(f"- **Avg UI Render Time**: {analysis.get('averageUIRenderMs', 0):.3f} ms")

    # Physics
    st.subheader("⚙️ Physics")
    st.markdown(f"- **Avg Physics Queries**: {analysis.get('averagePhysicsQueries', 0):.2f}")
    st.markdown(f"- **Avg 2D Physics Queries**: {analysis.get('averagePhysics2DQueries', 0):.2f}")
    st.markdown(f"- **Avg Physics Memory (3D)**: {analysis.get('averagePhysicsUsedMemoryMB', 0):.3f} MB")
    st.markdown(f"- **Avg Physics Memory (2D)**: {analysis.get('averagePhysics2DUsedMemoryMB', 0):.3f} MB")

    # Animation
    st.subheader("🎞️ Animation")
    st.markdown(f"- **Avg Animation Clip Memory**: {analysis.get('averageAnimationClipMemoryMB', 0):.3f} MB")
    st.markdown(f"- **Avg Animation Clip Count**: {analysis.get('averageAnimationClipCount', 0)}")
    st.markdown(f"- **Avg Animation Update Time**: {analysis.get('averageAnimationUpdateMs', 0):.3f} ms")

    # Recommendations
    st.subheader("⚠️ Recommendations")
    for r in analysis.get("recommendations", []):
        st.markdown(f"- {r}")


def render_graphs(frames: pd.DataFrame):
    st.header("📈 Graphs (Toggle On/Off)")
    col1, col2, col3 = st.columns(3)
    with col1:
        show_fps = st.checkbox("FPS")
        show_cpu = st.checkbox("CPU/Main/Render Threads")
        show_gpu = st.checkbox("GPU Frame Time")
    with col2:
        show_mem = st.checkbox("Memory Usage")
        show_gc = st.checkbox("GC Allocated")
        show_audio = st.checkbox("Audio Stats")
    with col3:
        show_draw = st.checkbox("Draw/Render Stats")
        show_phys = st.checkbox("Physics")
        show_ui = st.checkbox("UI Stats")
        show_anim = st.checkbox("Animation")

    if show_fps:
        st.subheader("FPS Over Time")
        frames["FPS"] = 1000 / frames["frameTime_ms"]
        st.line_chart(frames.set_index("frame")[["FPS"]])

    if show_cpu or show_gpu:
        st.subheader("Frame Times (ms)")
        plot_df = pd.DataFrame({"frame": frames["frame"]})
        if show_cpu:
            plot_df["Main Thread"] = frames["mainThreadTime_ms"]
            plot_df["Render Thread"] = frames["renderThreadTime_ms"]
        if show_gpu:
            plot_df["GPU"] = frames["gpuFrameTime_ms"]  
        st.line_chart(plot_df.set_index("frame"))

    if show_mem:
        st.subheader("Memory Usage (MB)")
        mem_df = pd.DataFrame({
            "frame": frames["frame"],
            "Allocated": frames["totalAllocatedMemory_kb"] / 1024,
            "Reserved": frames["totalReservedMemory_kb"] / 1024,
            "GC Reserved": frames["gcReservedMemory_kb"] / 1024,
            "System Used": frames["systemUsedMemory_kb"] / 1024
        })
        st.line_chart(mem_df.set_index("frame"))

    if show_gc:
        st.subheader("GC Allocated Memory (KB)")
        gc_df = pd.DataFrame({
            "frame": frames["frame"],
            "GC Allocated": frames["gcAllocatedMemory_kb"]
        })
        st.line_chart(gc_df.set_index("frame"))

    if show_draw:
        st.subheader("Rendering Stats")
        draw_df = frames[["frame", "drawCalls", "triangleCount", "vertexCount", "batchCount", "shadowCasterCount"]]
        st.line_chart(draw_df.set_index("frame"))

    if show_phys:
        st.subheader("Physics Queries & Memory (MB)")
        phys_df = pd.DataFrame({
            "frame": frames["frame"],
            "3D Queries": frames["physicsQueries"],
            "2D Queries": frames["physics2DQueries"],
            "3D Memory": frames["physicsUsedMemory_kb"] / 1024,
            "2D Memory": frames["physics2DUsedMemory_kb"] / 1024,
        })
        st.line_chart(phys_df.set_index("frame"))

    if show_audio:
        st.subheader("Audio Stats")
        audio_df = pd.DataFrame({
            "frame": frames["frame"],
            "Reserved": frames["audioReservedMemory_kb"] / 1024,
            "Used": frames["audioUsedMemory_kb"] / 1024,
            "Clip Memory": frames["audioClipMemory_kb"] / 1024,
            "Clip Count": frames["audioClipCount"],
            "Reads": frames["audioReads"],
        })
        st.line_chart(audio_df.set_index("frame"))

    if show_ui:
        st.subheader("UI Render & Layout Times (ms)")
        ui_df = pd.DataFrame({
            "frame": frames["frame"],
            "Layout Time": frames["uiLayout_ms"],
            "Render Time": frames["uiRender_ms"],
        })
        st.line_chart(ui_df.set_index("frame"))

    if show_anim:
        st.subheader("Animation Stats")
        anim_df = pd.DataFrame({
            "frame": frames["frame"],
            "Clip Memory (MB)": frames["animationClipMemory_kb"] / 1024,
            "Clip Count": frames["animationClipCount"],
            "Update Time (ms)": frames["animationUpdate_ms"]
        })
        st.line_chart(anim_df.set_index("frame"))


# Main App
st.title("Unity Performance JSON Analyzer")

uploaded_file = st.file_uploader("Upload JSON file", type="json")
if uploaded_file:
    data = json.load(uploaded_file)

    st.header("🧾 Session Info")
    st.markdown(f"- **Game**: {data.get('gameName', '-')}")
    st.markdown(f"- **Session ID**: {data.get('sessionId', '-')}")
    st.markdown(f"- **Start Time**: {data.get('startTime', '-')}")
    st.markdown(f"- **End Time**: {data.get('endTime', '-')}")

    st.subheader("📱 Device Info")
    device = data.get("deviceInfo", {})
    for key, value in device.items():
        st.write(f"**{key}**: {value}")

    if "analysis" in data:
        render_analysis_summary(data["analysis"])

    frames = pd.DataFrame(data["frames"])
    render_graphs(frames)

    st.header("🧮 Raw Frame Data")
    st.dataframe(frames)
