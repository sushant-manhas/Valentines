import streamlit as st
import turtle
import base64
from PIL import ImageGrab
import time
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Page setup
st.set_page_config(
    page_title="My Valentine 💖",
    page_icon="❤️",
    layout="centered"
)

# Custom CSS injection
def inject_css():
    with open("styles/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_css()

# Turtle rose drawing function
# Rose drawing function using Matplotlib
def draw_rose_matplotlib():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-2, 1])
    ax.axis('off')
    
    def heart_x(t):
        return 16 * (np.sin(t)**3)
    
    def heart_y(t):
        return 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    t = np.linspace(-np.pi, np.pi, 200)
    x = heart_x(t) / 15  # Scaling down
    y = heart_y(t) / 15 + 0.5  # Scaling down and shifting up
    
    ax.plot(x, y, color='red')
    return fig

# Main app logic
def main():
    st.markdown("""
    <div class="floating-hearts">
        <div class="heart"></div>
        <div class="heart"></div>
        <div class="heart"></div>
    </div>
    """, unsafe_allow_html=True)

    if 'accepted' not in st.session_state:
        st.session_state.accepted = False

    if not st.session_state.accepted:
        # Proposal Section
        st.markdown("<h1 class='proposal-text'>Will you be my Valentine? 💘</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("YES 💖", type="primary", use_container_width=True):
                with st.spinner("Growing our love..."):
                    # Use matplotlib to draw rose
                    fig = draw_rose_matplotlib()
                    st.pyplot(fig)
                    time.sleep(2)
                    st.session_state.accepted = True
                    st.experimental_rerun()
        
        with col2:
            if st.button("NO 😢", use_container_width=True):
                st.error("Please reconsider! 💔 Our love deserves a chance...")

    else:
        # Surprise Page
        st.balloons()
        
        # Photo Gallery
        st.page_link("streamlit_app.py", label="Go Back to Home", icon="🏠")
        st.markdown("<h2 class='memory-title'>Our Beautiful Memories 📸</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        image_files = [f for f in os.listdir("images") if f.endswith(('.png', '.jpg'))]
        
        for i, col in enumerate(cols):
            if i < len(image_files):
                with col:
                    img_path = os.path.join("images/couple_photos", image_files[i])
                    st.image(img_path, use_column_width=True, caption=f"Memory #{i+1}")

        # Love Letter
        st.markdown("<h2 class='letter-title'>From My Heart 💌</h2>", unsafe_allow_html=True)
        with open("documents/love_letter.txt") as f:
            love_letter = f.read()
        
        b64_letter = base64.b64encode(love_letter.encode()).decode()
        href = f'<a class="download-link" href="data:file/txt;base64,{b64_letter}" download="My_Love_Letter.txt">📥 Download Love Letter</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Background Music
        audio_path = "audio/romantic_music.mp3"
        if os.path.exists(audio_path):
            audio_str = open(audio_path, "rb").read()
            st.markdown(f"""
            <audio autoplay loop style="display:none;">
                <source src="data:audio/mp3;base64,{base64.b64encode(audio_str).decode()}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)
        

if __name__ == "__main__":
    main()
