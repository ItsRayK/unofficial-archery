#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st
import base64

#-------------------#
#       Setup       #
#-------------------#

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / "style" / "style.css"
ASSETS = THIS_DIR / "assets"

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64(ASSETS / "img" / "bg.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
}}
</style>
"""
### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯", initial_sidebar_state="collapsed")

### Apply Custom CSS
with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(page_bg_img, unsafe_allow_html=True)

#-------------------#
#   Page Elements   #
#-------------------#

# Display Header
RANGE_NAME = "Unofficial Archery"
st.markdown(f"<center style='text-align: center; font-size: 3.1vmax; font-weight: 600;'>{RANGE_NAME} 🎯</center>", unsafe_allow_html=True)

st.markdown(f"#")

col1_1, col1_2, col1_3 = st.columns(3, gap="medium")

###### Column 1

col1_1.markdown(f"<center style='text-align: center; font-size: 1.5em; padding-bottom: 1em;'>Scoring Timer</center>", unsafe_allow_html=True)

if col1_1.button("Timer", use_container_width=True):
    st.switch_page("./pages/Timer.py")

if col1_1.button("Timer Settings", use_container_width=True):
    st.switch_page("./pages/Timer_Settings.py")

col1_1.divider()

###### Column 2

col1_2.markdown(f"<center style='text-align: center; font-size: 1.5em; padding-bottom: 1em;'>Range Tools</center>", unsafe_allow_html=True)

if col1_2.button("Range Commands", use_container_width=True):
    st.switch_page("./pages/Range_Commands.py")

if col1_2.button("Countdown", use_container_width=True):
    st.switch_page("./pages/Countdown.py")

col1_2.divider()

###### Column 3

col1_3.markdown(f"<center style='text-align: center; font-size: 1.5em; padding-bottom: 1em;'>Info</center>", unsafe_allow_html=True)

if col1_3.button("About", use_container_width=True):
    st.switch_page("./pages/About.py")

if col1_3.button("Useful Tips", use_container_width=True):
    st.switch_page("./pages/Useful_Tips.py")

col1_3.divider()

st.markdown(f"""
            Important: Don't use the browsers navigation buttons (forward/back/refresh) while using this tool.
            Doing so will reset any settings you may have configured.
            Navigate with the on screen buttons or open the navigation menu in the top left.
            """)