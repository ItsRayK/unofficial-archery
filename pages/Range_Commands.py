#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st
from streamlit_shortcuts import add_keyboard_shortcuts
import base64
import time

#-------------------#
#       Setup       #
#-------------------#

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / ".." / "style" / "style.css"
ASSETS = THIS_DIR / ".." / "assets"

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯", layout='wide', initial_sidebar_state="collapsed")

@st.cache_resource
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64(ASSETS / "img" / "range-bg.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

### Apply Custom CSS
# with open(CSS_FILE) as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#-------------------#
#   Session State   #
#-------------------#
if 'last_command' not in st.session_state:
    st.session_state['last_command'] = 'HOLD'

if 'is_range_buzzer_enabled' not in st.session_state:
    st.session_state['is_range_buzzer_enabled'] = False


#-------------------#
#    Setup Assets   #
#-------------------#

def play_buzzer(num_times = 1):
    if st.session_state['is_range_buzzer_enabled']:
        if num_times == 2:
            buzzer_audio_file = ASSETS / "audio" / "softbuzzer2.mp3"
        elif num_times == 3:
            buzzer_audio_file = ASSETS / "audio" / "softbuzzer3.mp3"
        else:
            buzzer_audio_file = ASSETS / "audio" / "softbuzzer.mp3"

        with open(buzzer_audio_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            col3_1.markdown(md, unsafe_allow_html=True)
            time.sleep(num_times)

#-------------------#
#   Page Elements   #
#-------------------#

online_text = "<center style='text-align: center; font-size: 12vmax; color: #cf7c11'>ON LINE</center>"
begin_text = "<center style='text-align: center; font-size: 12vmax; color: #0cc93f'>BEGIN</center>"
clear_text = "<center style='text-align: center; font-size: 12vmax; color: #2695d1'>CLEAR</center>"
hold_text = "<center style='text-align: center; font-size: 12vmax; color: #c94b0c'>HOLD</center>"

if st.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

st.header("Range Commands", anchor=False)

col1_1, col1_2 = st.columns([0.75,0.25])

if st.session_state['last_command'] == "ON LINE":
    command_text_placeholder = col1_1.markdown(f"{online_text}", unsafe_allow_html=True)

elif st.session_state['last_command'] == "BEGIN":
    command_text_placeholder = col1_1.markdown(f"{begin_text}", unsafe_allow_html=True)

elif st.session_state['last_command'] == "CLEAR":
    command_text_placeholder = col1_1.markdown(f"{clear_text}", unsafe_allow_html=True)

else:
    command_text_placeholder = col1_1.markdown(f"{hold_text}", unsafe_allow_html=True)

st.text("")
st.text("")
st.text("")

## Setup Multi Column Layout
col2_1, col2_2, col2_3, col2_4 = st.columns(4)
col3_1, col3_2, col3_3, col3_4 = st.columns(4)

#-------------------#
#     Core Logic    #
#-------------------#

col1_2.markdown("#")
col1_2.markdown("###")

if col1_2.button("ON LINE", use_container_width=True):
    command_text_placeholder.markdown(f"{online_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'ON LINE'
    play_buzzer(2)
    st.rerun()

if col1_2.button("BEGIN", use_container_width=True):
    command_text_placeholder.markdown(f"{begin_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'BEGIN'
    play_buzzer(1)
    st.rerun()

if col1_2.button("CLEAR", use_container_width=True):
    command_text_placeholder.markdown(f"{clear_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'CLEAR'
    play_buzzer(3)
    st.rerun()

if col1_2.button("HOLD", use_container_width=True, type="primary"):
    command_text_placeholder.markdown(f"{hold_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'HOLD'

add_keyboard_shortcuts({
    '1': 'ON LINE',
    '2': 'BEGIN',
    '3': 'CLEAR',
    '4': 'HOLD'
})

col3_3.text("")
col3_4.text("")
buzzer_text_placeholder = col1_2.empty()
settings_popover = col1_2.empty()

if st.session_state['is_range_buzzer_enabled']:
    buzzer_text_placeholder.write(f"Buzzer: Enabled")
else:
    buzzer_text_placeholder.write(f"Buzzer: Disabled")

with settings_popover.popover("Settings/Hotkeys", use_container_width=True):
    if st.button("Toggle Buzzer", use_container_width=True):
        if st.session_state['is_range_buzzer_enabled']:
            st.session_state['is_range_buzzer_enabled'] = False
        else:
            st.session_state['is_range_buzzer_enabled'] = True
        st.rerun()

    st.markdown('''
        #### Hotkeys
        | Key | Range Command |
        | --- | ------------- |
        | 1 | On Line |       
        | 2 | Begin |
        | 3 | Clear |
        | 4 | Hold |
    ''')
###################### DEBUG ################
# st.session_state