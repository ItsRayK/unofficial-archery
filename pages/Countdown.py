#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st
from streamlit_shortcuts import add_keyboard_shortcuts
import time
import base64

#-------------------#
#       Setup       #
#-------------------#

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / ".." / "style" / "style.css"
ASSETS = THIS_DIR / ".." / "assets"

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯", layout='wide', initial_sidebar_state="collapsed")

### Apply Custom CSS
#with open(CSS_FILE) as f:
#    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#-------------------#
#   Session State   #
#-------------------#
if 'countdown_time' not in st.session_state:
    st.session_state['countdown_time'] = 300

if 'countdown_ended' not in st.session_state:
    st.session_state['countdown_ended'] = False

if 'countdown_end_text' not in st.session_state:
    st.session_state['countdown_end_text'] = '00:00'

if 'countdown_title_text' not in st.session_state:
    st.session_state['countdown_title_text'] = 'Countdown'

if 'is_buzzer_enabled' not in st.session_state:
    st.session_state['is_buzzer_enabled'] = True

## Previous State Trackers
if 'countdown_active' not in st.session_state:
    st.session_state['countdown_active'] = False

if 'last_countdown_time' not in st.session_state:
    st.session_state['last_countdown_time'] = st.session_state['countdown_time']

#-------------------#
#   Page Elements   #
#-------------------#

## Styles/Colors
style_small_default = "<center style='text-align: center; font-size: 4.5vmax;'>"

timer_style_default = "<center style='text-align: center; font-size: 18vmax;'>"

end_center_style = "</center>"

home_button_placeholder = st.empty()

## Setup Three Column Layout
countdown_title_placeholder = st.empty()

## Outside Of Columns
time_placeholder = st.empty()

## Setup Next Set of Columns
col2_1, col2_2, col2_3= st.columns([0.2, 0.6, 0.2])

countdown_controls_placeholder = col2_2.empty()
settings_popover = col2_3.empty()

### End General Layout

#-------------------#
#    Setup Assets   #
#-------------------#

def play_buzzer(num_times = 1):
    if st.session_state['is_buzzer_enabled']:
        if num_times == 2:
            buzzer_audio_file = ASSETS / "audio" / "buzzer2.mp3"
        elif num_times == 3:
            buzzer_audio_file = ASSETS / "audio" / "buzzer3.mp3"
        else:
            buzzer_audio_file = ASSETS / "audio" / "buzzer.mp3"

        with open(buzzer_audio_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            col2_1.markdown(md, unsafe_allow_html=True)


#-------------------#
#     Core Logic    #
#-------------------#

countdown_title_placeholder.markdown(f"{style_small_default}{st.session_state['countdown_title_text']}{end_center_style}", unsafe_allow_html=True)

if not st.session_state['countdown_ended']:
    if st.session_state['last_countdown_time'] >= 3600:
        time_placeholder.markdown(f"{timer_style_default}{time.strftime('%H:%M:%S', time.gmtime(st.session_state['last_countdown_time']))}{end_center_style}", unsafe_allow_html=True)
    else:
        time_placeholder.markdown(f"{timer_style_default}{time.strftime('%M:%S', time.gmtime(st.session_state['last_countdown_time']))}{end_center_style}", unsafe_allow_html=True)
else:
    time_placeholder.markdown(f"{timer_style_default}{st.session_state['countdown_end_text']}{end_center_style}", unsafe_allow_html=True)


def run_timer(last_countdown_time_sec):
    # Reinitialize values on Start/Stop based on last known state
    display_timer = last_countdown_time_sec

    # Non-blocking timer loop
    while( st.session_state['countdown_active'] ):

        if display_timer <= 0:
            st.session_state['countdown_ended'] = True
            st.session_state['last_countdown_time'] = st.session_state['countdown_time']
            st.session_state['countdown_active'] = False
            st.rerun()

        if st.session_state['last_countdown_time'] >= 3600:
            time_placeholder.markdown(f"{timer_style_default}{time.strftime('%H:%M:%S', time.gmtime(st.session_state['last_countdown_time']))}{end_center_style}", unsafe_allow_html=True)
        else:
            time_placeholder.markdown(f"{timer_style_default}{time.strftime('%M:%S', time.gmtime(st.session_state['last_countdown_time']))}{end_center_style}", unsafe_allow_html=True)

        st.session_state['last_countdown_time'] = display_timer - 1
        display_timer -= 1

        time.sleep(1)

if home_button_placeholder.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

with settings_popover.popover("Settings"):
    title_text = st.text_input("Event Text", value=st.session_state['countdown_title_text'])
    countdown_time = st.number_input("Time (seconds)", min_value=0, step=1, value=st.session_state['countdown_time'])
    end_text = st.text_input("End Display Text", value=st.session_state['countdown_end_text'])

    if st.button("Apply"):
        st.session_state['countdown_title_text'] = title_text
        st.session_state['countdown_time'] = countdown_time
        st.session_state['last_countdown_time'] = countdown_time
        if end_text.strip().lower() == '':
            end_text = '00:00'
        st.session_state['countdown_end_text'] = end_text

        st.session_state['countdown_ended'] = False
        st.session_state['countdown_active'] = False

        st.rerun()

if countdown_controls_placeholder.button("Start/Stop", use_container_width=True):
    if st.session_state['countdown_active'] == False:
        st.session_state['countdown_ended'] = False
        st.session_state['countdown_active'] = True
        run_timer(st.session_state['last_countdown_time'])
    else:
        st.session_state['countdown_active'] = False

add_keyboard_shortcuts({
    's': 'Start/Stop'
})

###################### DEBUG ################
#st.session_state