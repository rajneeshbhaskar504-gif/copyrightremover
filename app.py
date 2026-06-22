import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Copyright Shield", page_icon="🎬", layout="centered")

st.title("🎬 Copyright Shield & Video Modifier")
st.write("Alters video metadata, colors, and speed to bypass automated hash detection.")

uploaded_file = st.file_uploader("Upload your Video (MP4, MKV, MOV)", type=["mp4", "mkv", "mov"])

if uploaded_file is not None:
    # Input file ko temporary save karna
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input.mp4")
    
    st.subheader("Modifications Settings")
    speed = st.slider("Speed Factor (1.01x ya 1.02x best hai)", 0.95, 1.05, 1.01, step=0.01)
    flip = st.checkbox("Horizontal Mirror (Highly Recommended)", value=True)
    
    if st.button("🚀 Process & Remove Copyright Fingerprint"):
        with st.spinner("Processing... FFmpeg aapki video modify kar raha hai."):
            
            # Filters setup
            vf_filters = []
            if flip:
                vf_filters.append("hflip")
            # Pixels and dimensions subtle change to break hash
            vf_filters.append("eq=brightness=0.02:contrast=1.03:saturation=1.02")
            vf_filters.append("crop=in_w*0.99:in_h*0.99")
            
            vf_string = ",".join(vf_filters)
            
            # FFmpeg Command (Video edits + Audio sync + Metadata strip)
            cmd = f'ffmpeg -i input.mp4 -vf "{vf_string}" -af "atempo={speed},asetrate=44100*{1/speed}" -map_metadata -1 -y output.mp4'
            
            # Execute
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists("output.mp4"):
                st.success("🎉 Video Processed Successfully! Metadata aur original hash remove ho gaye hain.")
                
                with open("output.mp4", "rb") as file:
                    st.download_button(
                        label="📥 Download Clean Video",
                        data=file,
                        file_name="cleaned_video.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("Processing mein error aaya! Niche diye gaye logs check karein:")
                st.code(result.stderr)
