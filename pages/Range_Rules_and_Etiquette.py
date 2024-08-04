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
image_names = []
images = []

for name in image_names:
    image = Image.open(ASSETS / "img" / "archery-sample-scoring" / name)
    images.append(image)

if st.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

col1, col2, col3 = st.columns([0.2,0.6,0.2])

col2.header("Range Rules/Etiquette", anchor=False)

col2.markdown("Note: Please follow your range's specific rules, these are just good practices.")

col2.markdown("#### Safety First")
col2.markdown("1. __Always follow range commands.__ If you are waiting for a command there is probably good reason. If you don't think so, there is no harm in asking.")
col2.markdown("2. __A loaded bow should only ever be pointing down range towards the targets__.")
col2.markdown("3. __If you're not on line ALL of your arrows should either be in your quiver or in the target down range__.")
col2.markdown("4. Similarly, do not walk around with arrows in your hand. Keep the arrows on you in your quiver.")
col2.markdown("5. __No running!__ Seriously don't.")
col2.markdown("6. __No dry firing!__ A 'dry fire' is when you load and release a bow without an arrow. All of the energy released goes straight into the limbs of the bow and can seriously injure you and damage your equipment making it unsafe until it is thouroughly inspected.")

col2.divider()

col2.markdown("#### Keeping Each Other Safe")
col2.markdown("On the topic of safety, if you see anything unsafe, you should address it. It is not just the responsibilty of range staff to keep people safe, but is the responsibility of everyone. __You are allowed to yell the safety command (HOLD) as appropriate.__")

col2.divider()

col2.markdown("#### Open Range Rules vs Official Scoring")
col2.markdown("Please take note of the differences.")
col2.markdown("""
              | Command | Open Range | Official Scoring |
              | ------- | ---------- | ---------------- |
              | On Line | Grab your bow, straddle the line, __and wait.__ | Grab your bow, straddle the line, __you may load an arrow.__ |
              | Begin | You may load your arrow and begin shooting. When you're done, step off the line and put your bow away. | You may begin shooting. __You must finish shooting before the timer ends.__ When you're done, step off the line and put your bow away. |
              | Clear | It is safe to retrieve your arrows. | It is safe to retrieve you arrows. |
              | Hold | Emergency command. Immediately let down your bow and wait for further instructions. | Emergency command. Immediately let down your bow and wait for further instructions. |
              """)

col2.divider()

col2.markdown("#### Stay In Your Lane")
col2.markdown("Be weary of your surroundings when you're on line. Keep what you do (i.e loading an arrow, drawing your bow, just standing there collecting yourself) within your lane.")

col2.divider()

col2.markdown("#### Walking Behind Other Archers")
col2.markdown("Generally there will be a safety/waiting line you must wait behind if you're not shooting, but it's good practice to allow someone to complete their shot before moving behind them. If you can't wait, just maintain a larger distance between them or walk slower.")

col2.divider()

col2.markdown("#### No Yelling")
col2.markdown("Keep your volume to a reasonable level. You should be able to hear range commands at all times. The only time it is okay to yell is for safety commands (i.e. HOLD).")

col2.divider()