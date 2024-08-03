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

# Load Images
image_names = ["01.JPG", "02.JPG", "03.JPG", "04.JPG", "05.JPG", "06.JPG"]
images = []

for name in image_names:
    image = Image.open(ASSETS / "img" / "archery-sample-scoring" / name)
    images.append(image)

if st.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

col1, col2, col3 = st.columns([0.2,0.6,0.2])

col2.header("How To Score", anchor=False)

col2.markdown("Note: Not all scoring sheets are the same, but here is generally how you'd fill one out.")

col2.markdown("#### First End: Basic Scoring")
col2.markdown("Score from highest to lowest. Remember that breaking the line means you get the higher score.")
col2.image(images[0], caption="First End: Score from highest to lowest. Remember that breaking the line means you get the higher score.", use_column_width=None)

col2.divider()

col2.markdown("#### Second End: How to mark a 'Miss'")
col2.markdown("If you miss, mark it with an 'M'.")
col2.image(images[1], caption="Second End: If you miss, mark it with an 'M'.", use_column_width=None)

col2.divider()

col2.markdown("#### Third End: 'I wrote down the wrong score!'")
col2.markdown("If you make a mistake, don't erase! Instead strike it out and write the correct score.")
col2.image(images[2], caption="Third End: If you make a mistake, don't erase! Instead strike it out and write the correct score.", use_column_width=None)

col2.divider()

col2.markdown("#### Fourth End: It's just one of those days.")
col2.markdown("Everyone has a 'not so great end'.")
col2.image(images[3], caption="Fourth End: Everyone has a 'not so great end'.", use_column_width=None)

col2.divider()

col2.markdown("#### Fifth End: Last end. Best end!")
col2.markdown("Last end, best end! Hopefully you understand the basics of scoring now.")
col2.image(images[4], caption="Fifth End: Last end, best end! Hopefully you understand the basics of scoring now.", use_column_width=None)

col2.divider()

col2.markdown("#### Finalizing: Tallying up and Signing")
col2.markdown("Fill in the remainder of the boxes. Verify with your group that the final scores are correct and sign each other's card [not shown].")
col2.image(images[5], caption="Finalizing: Fill in the remainder of the boxes. Verify with your group that the final scores are correct and sign each other's card [not shown].", use_column_width=None)

col2.divider()