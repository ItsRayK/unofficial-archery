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
if 'spt_setup_time' not in st.session_state:
    st.session_state['spt_setup_time'] = 10

if 'spt_work_time' not in st.session_state:
    st.session_state['spt_work_time'] = 30

if 'spt_rest_time' not in st.session_state:
    st.session_state['spt_rest_time'] = 60

if 'spt_num_reps' not in st.session_state:
    st.session_state['spt_num_reps'] = 6

if 'spt_timer_ended' not in st.session_state:
    st.session_state['spt_timer_ended'] = False

if 'spt_end_text' not in st.session_state:
    st.session_state['spt_end_text'] = '00:00'

if 'spt_title_text' not in st.session_state:
    st.session_state['spt_title_text'] = 'SPT 1: Endurance'

## Previous State Trackers
if 'spt_timer_active' not in st.session_state:
    st.session_state['spt_timer_active'] = False

if 'last_spt_time' not in st.session_state:
    st.session_state['last_spt_time'] = st.session_state['spt_setup_time']

if 'last_spt_phase' not in st.session_state:
    st.session_state['last_spt_phase'] = 'SETUP'

if 'curr_rep' not in st.session_state:
    st.session_state['curr_rep'] = 1

if 'is_spt_audio_enabled' not in st.session_state:
    st.session_state['is_spt_audio_enabled'] = True

#-------------------#
#   Page Elements   #
#-------------------#

## Styles/Colors
style_small_default = "<center style='text-align: center; font-size: 4vmax;'>"

timer_style_default = "<center style='text-align: center; font-size: 17vmax;'>"
timer_style_green = "<center style='text-align: center; font-size: 17vmax; color: #0cc93f'>"
timer_style_amber = "<center style='text-align: center; font-size: 17vmax; color: #c9b30c'>"

end_center_style = "</center>"

home_button_placeholder = st.empty()

## Setup Column Layout
col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])

spt_title_placeholder = col1_2.empty()
spt_phase_placeholder = col1_3.empty()
spt_rep_placeholder = col1_4.empty()

## Outside Of Columns
spt_time_placeholder = st.empty()

## Setup Next Set of Columns
col2_1, col2_2, col2_3 = st.columns([0.2, 0.6, 0.2])

spt_audio_placeholder = col2_1.empty()
spt_controls_placeholder = col2_2.empty()
settings_popover = col2_3.empty()

### End General Layout

#-------------------#
#    Setup Assets   #
#-------------------#

spt_num = int(st.session_state['spt_title_text'].split(':')[0].split(' ')[1])
spt_description = st.session_state['spt_title_text'].split(':')[1]

def clear_buzzer(element):
    element.empty()

def play_buzzer(element, num_times = 1):
    clear_buzzer(element)
    time.sleep(0.05)
    if st.session_state['is_spt_audio_enabled']:

        buzzer1_file_str = "softbuzzer.mp3"
        buzzer2_file_str = "softbuzzer2.mp3"
        buzzer3_file_str = "softbuzzer3.mp3"

        if num_times == 2:
            buzzer_audio_file = ASSETS / "audio" / buzzer2_file_str
        elif num_times == 3:
            buzzer_audio_file = ASSETS / "audio" / buzzer3_file_str
        else:
            buzzer_audio_file = ASSETS / "audio" / buzzer1_file_str

        with open(buzzer_audio_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            element.markdown(md, unsafe_allow_html=True)


#-------------------#
#     Core Logic    #
#-------------------#

spt_title_placeholder.markdown(f"{style_small_default}SPT {spt_num}{end_center_style}", unsafe_allow_html=True)
spt_phase_placeholder.markdown(f"{style_small_default}{st.session_state['last_spt_phase']}{end_center_style}", unsafe_allow_html=True)
spt_rep_placeholder.markdown(f"{style_small_default}{st.session_state['curr_rep']}/{st.session_state['spt_num_reps']}{end_center_style}", unsafe_allow_html=True)

if not st.session_state['spt_timer_ended']:
    if st.session_state['last_spt_time'] >= 3600:
        spt_time_placeholder.markdown(f"{timer_style_default}{time.strftime('%H:%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)
    else:
        spt_time_placeholder.markdown(f"{timer_style_default}{time.strftime('%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)
else:
    spt_time_placeholder.markdown(f"{timer_style_default}{st.session_state['spt_end_text']}{end_center_style}", unsafe_allow_html=True)


def run_timer(last_phase, last_countdown_time_sec):
    # Reinitialize values on Start/Stop based on last known state
    display_timer = last_countdown_time_sec
    phase = last_phase

    # Non-blocking timer loop
    while( st.session_state['spt_timer_active'] ):

        if phase == 'SETUP':
            if display_timer < 0:
                play_buzzer(spt_audio_placeholder)
                phase = 'WORK'
                st.session_state['last_spt_phase'] = phase
                st.session_state['last_spt_time'] = st.session_state['spt_work_time']
                display_timer = st.session_state['last_spt_time']
                spt_phase_placeholder.markdown(f"{style_small_default}{st.session_state['last_spt_phase']}{end_center_style}", unsafe_allow_html=True)
                

        elif phase == "WORK":
            if display_timer < 0:
                play_buzzer(spt_audio_placeholder)
                phase = 'REST'
                st.session_state['last_spt_phase'] = phase
                st.session_state['last_spt_time'] = st.session_state['spt_rest_time']
                display_timer = st.session_state['last_spt_time']
                spt_phase_placeholder.markdown(f"{style_small_default}{st.session_state['last_spt_phase']}{end_center_style}", unsafe_allow_html=True)

        elif phase == "REST":
            if display_timer < 0:
                phase = 'WORK'
                st.session_state['last_spt_phase'] = phase
                st.session_state['last_spt_time'] = st.session_state['spt_work_time']
                st.session_state['curr_rep'] += 1
                display_timer = st.session_state['last_spt_time']

                if st.session_state['curr_rep'] > st.session_state['spt_num_reps']:
                    play_buzzer(spt_audio_placeholder, 3)
                    phase = 'END'
                    st.session_state['last_spt_phase'] = phase
                    st.session_state['curr_rep'] = st.session_state['spt_num_reps']
                    spt_rep_placeholder.markdown(f"{style_small_default}{st.session_state['curr_rep']}/{st.session_state['spt_num_reps']}{end_center_style}", unsafe_allow_html=True)

                else:
                    play_buzzer(spt_audio_placeholder)
                    spt_rep_placeholder.markdown(f"{style_small_default}{st.session_state['curr_rep']}/{st.session_state['spt_num_reps']}{end_center_style}", unsafe_allow_html=True)

                spt_phase_placeholder.markdown(f"{style_small_default}{st.session_state['last_spt_phase']}{end_center_style}", unsafe_allow_html=True)

        if phase == "END":
            play_buzzer(spt_audio_placeholder, 3)
            st.session_state['spt_timer_ended'] = True
            spt_phase_placeholder.markdown(f"{style_small_default}{st.session_state['last_spt_phase']}{end_center_style}", unsafe_allow_html=True)
            st.session_state['last_spt_time'] = st.session_state['spt_end_text']
            st.session_state['spt_timer_active'] = False

            time.sleep(3)
            st.rerun()

        if st.session_state['last_spt_time'] >= 3600:
            if phase == "WORK":
                spt_time_placeholder.markdown(f"{timer_style_green}{time.strftime('%H:%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)
            elif phase == "REST":
                spt_time_placeholder.markdown(f"{timer_style_amber}{time.strftime('%H:%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)
            else:
                spt_time_placeholder.markdown(f"{timer_style_default}{time.strftime('%H:%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)

        else:
            if phase == "WORK":
                spt_time_placeholder.markdown(f"{timer_style_green}{time.strftime('%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)
            elif phase == "REST":
                spt_time_placeholder.markdown(f"{timer_style_amber}{time.strftime('%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)
            else:
                spt_time_placeholder.markdown(f"{timer_style_default}{time.strftime('%M:%S', time.gmtime(st.session_state['last_spt_time']))}{end_center_style}", unsafe_allow_html=True)

        st.session_state['last_spt_time'] = display_timer - 1
        display_timer -= 1

        time.sleep(1)

if home_button_placeholder.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

if spt_controls_placeholder.button("Start/Stop", use_container_width=True):
    if st.session_state['spt_timer_active'] == False:
        st.session_state['spt_timer_ended'] = False
        st.session_state['spt_timer_active'] = True
        run_timer(st.session_state['last_spt_phase'], st.session_state['last_spt_time'])
    else:
        st.session_state['spt_timer_active'] = False

col4_1, col4_2, col4_3, col4_4= st.columns(4)

spt_text = col4_1.selectbox("SPT", ("SPT 1: Endurance", "SPT 2: Strength", "SPT 3: Flexibility", "SPT 4: Structure"), index=0)
spt_reps = col4_2.number_input("Number of Reps", min_value=0, step=1, value=st.session_state['spt_num_reps'])
spt_work_time = col4_3.number_input("Work Time (seconds)", min_value=0, step=1, value=st.session_state['spt_work_time'])
spt_rest_time = col4_4.number_input("Rest Time (seconds)", min_value=0, step=1, value=st.session_state['spt_rest_time'])
#end_text = st.text_input("End Display Text", value=st.session_state['spt_end_text'])

if st.button("Apply", use_container_width=True):
    st.session_state['spt_title_text'] = spt_text
    st.session_state['spt_work_time'] = spt_work_time
    st.session_state['spt_rest_time'] = spt_rest_time
    # if end_text.strip().lower() == '':
    #     end_text = '00:00'
    #st.session_state['spt_end_text'] = end_text
    st.session_state['last_spt_time'] = st.session_state['spt_setup_time']
    st.session_state['spt_num_reps'] = spt_reps
    st.session_state['curr_rep'] = 1
    st.session_state['spt_timer_ended'] = False
    st.session_state['spt_timer_active'] = False

    st.rerun()

add_keyboard_shortcuts({
    's': 'Start/Stop'
})

###################### DEBUG ################
#st.session_state