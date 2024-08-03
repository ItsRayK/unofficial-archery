#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st
from PIL import Image

#-------------------#
#       Setup       #
#-------------------#

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / ".." / "style" / "style.css"
ASSETS = THIS_DIR / ".." / "assets"

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯", initial_sidebar_state="collapsed", layout="wide")

### Apply Custom CSS
# with open(CSS_FILE) as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if st.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

col1, col2, col3 = st.columns([0.2,0.6,0.2])

col2.header("Useful Tips", anchor=False)

image = Image.open(ASSETS / "img" / "tips" / "close_sidebar_example.png")

col2.markdown("#### Go Full Screen")
col2.markdown("Press 'F11' on your keyboard to go full screen. Press it again to go back.")

col2.markdown("#### Close the Navigation Menu")
col2.image(image, caption="You can close the navigation menu by clicking the 'X' as shown in the image. Click the '>' to reopen it at any time.", width=480)