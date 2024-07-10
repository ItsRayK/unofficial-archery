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

### Function to get query parameters
def get_range_name():
    query_params = st.experimental_get_query_params()
    return query_params.get("range", ["Unofficial Archery"])[0]

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯")

### Apply Custom CSS
# with open(CSS_FILE) as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("Useful Tips")

image = Image.open(ASSETS / "img" / "tips" / "close_sidebar_example.png")

st.markdown("#### Go Full Screen")
st.markdown("Press 'F11' on your keyboard to go full screen. Press it again to go back.")

st.markdown("#### Close the Navigation Menu")
st.image(image, caption="You can close the navigation menu by clicking the 'X' as shown in the image. Click the '>' to reopen it at any time.", width=480)