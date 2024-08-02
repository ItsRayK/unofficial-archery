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
if 'setup_time' not in st.session_state:
    st.session_state['setup_time'] = 10

if 'shooting_time' not in st.session_state:
    st.session_state['shooting_time'] = 90

if 'low_time_warning' not in st.session_state:
    st.session_state['low_time_warning'] = 30

if 'low_time_urgent' not in st.session_state:
    st.session_state['low_time_urgent'] = 15

if 'use_warning_color' not in st.session_state:
    st.session_state['use_warning_color'] = True

if 'use_urgent_color' not in st.session_state:
    st.session_state['use_urgent_color'] = True
    
if 'num_practice_ends' not in st.session_state:
    st.session_state['num_practice_ends'] = 2

if 'num_scoring_ends' not in st.session_state:
    st.session_state['num_scoring_ends'] = 10

if 'is_double_line' not in st.session_state:
    st.session_state['is_double_line'] = False

if 'alternate_line' not in st.session_state:
    st.session_state['alternate_line'] = False

if 'current_line' not in st.session_state:
    st.session_state['current_line'] = 'A'

if 'current_end' not in st.session_state:
    st.session_state['current_end'] = 1

if 'is_buzzer_enabled' not in st.session_state:
    st.session_state['is_buzzer_enabled'] = True

if 'skip_buzzer' not in st.session_state:
    st.session_state['skip_buzzer'] = False

## Previous State Trackers
if 'timer_active' not in st.session_state:
    st.session_state['timer_active'] = False

if 'last_setup_time' not in st.session_state:
    st.session_state['last_setup_time'] = st.session_state['setup_time']

if 'last_shooting_time' not in st.session_state:
    st.session_state['last_shooting_time'] = st.session_state['shooting_time']

if 'last_phase' not in st.session_state:
    st.session_state['last_phase'] = 'SETUP'

#-------------------#
#   Page Elements   #
#-------------------#

## Styles/Colors
style_small_default = "<center style='text-align: center; font-size: 2.5vmax;'>"

timer_style_default = "<center style='text-align: center; font-size: 15vmax;'>"
timer_style_green = "<center style='text-align: center; font-size: 15vmax; color: #0cc93f'>"
timer_style_warning = "<center style='text-align: center; font-size: 15vmax; color: #c9b30c'>"
timer_style_urgent = "<center style='text-align: center; font-size: 15vmax; color: #c94b0c'>"

end_center_style = "</center>"

## Setup Three Column Layout
col1_1, col1_2, col1_3= st.columns(3)

line_placeholder = col1_1.empty()
end_number_placeholder = col1_3.empty()

line_placeholder.markdown(f"{style_small_default}Line: {st.session_state['current_line']}{end_center_style}", unsafe_allow_html=True)
end_number_placeholder.markdown(f"{style_small_default}End: {st.session_state['current_end']}/{st.session_state['num_scoring_ends']}{end_center_style}", unsafe_allow_html=True)

## Outside Of Columns
time_placeholder = st.empty()
phase_placeholder = st.empty()

st.markdown('##') # Spacer

## Setup Next Set of Columns
col2_1, col2_2, col2_3= st.columns(3)

## Nested Columns

timer_controls_placeholder = col2_2.empty()

col2_2_1, col2_2_2= col2_2.columns(2)

timer_settings_placeholder = col2_2_1.empty()
advance_phase_button_placeholder = col2_2_2.empty()

buzzer_audio_placeholder = col2_2.empty()
### End General Layout

#-------------------#
#    Setup Assets   #
#-------------------#

def clear_buzzer(element):
    element.empty()

def play_buzzer(element, num_times = 1):
    clear_buzzer(element)

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
            element.markdown(md, unsafe_allow_html=True)

#-------------------#
#     Core Logic    #
#-------------------#
if st.session_state['last_phase'] == 'SETUP':
    time_placeholder.markdown(f"{timer_style_default}{time.strftime('%M:%S', time.gmtime(st.session_state['last_setup_time']))}{end_center_style}", unsafe_allow_html=True)
elif st.session_state['last_phase'] == 'SHOOT':
    time_placeholder.markdown(f"{timer_style_default}{time.strftime('%M:%S', time.gmtime(st.session_state['last_shooting_time']))}{end_center_style}", unsafe_allow_html=True)
else:
    time_placeholder.markdown(f"{timer_style_default}00:00{end_center_style}", unsafe_allow_html=True)

phase_placeholder.markdown(f"{style_small_default}HOLD{end_center_style}", unsafe_allow_html=True)

def run_timer(last_setup_time_sec, last_shot_time_sec, current_phase, current_line):
    phase = current_phase

    # Reinitialize values on Start/Stop based on last known state
    if phase == 'SETUP':
        if not st.session_state['skip_buzzer']:
            play_buzzer(buzzer_audio_placeholder, 2)
        st.session_state['skip_buzzer'] = False
        phase_placeholder.markdown(f"{style_small_default}{phase}{end_center_style}", unsafe_allow_html=True)
        display_timer = last_setup_time_sec
    elif phase == 'SHOOT':
        if not st.session_state['skip_buzzer']:
            play_buzzer(buzzer_audio_placeholder, 1)
        st.session_state['skip_buzzer'] = False
        phase_placeholder.markdown(f"{style_small_default}{phase}{end_center_style}", unsafe_allow_html=True)
        display_timer = last_shot_time_sec
    else:
        display_timer = 0

    # Non-blocking timer loop
    while( True ):
        phase_placeholder.markdown(f"{style_small_default}{phase}{end_center_style}", unsafe_allow_html=True)
        
        if st.session_state['alternate_line']:
            if st.session_state['current_end'] % 2 == 1:
                starting_line = 'A'
                next_line = 'B'
            else:
                starting_line = 'B'
                next_line = 'A'
        else:
            starting_line = 'A'
            next_line = 'B'

        # Logic if in SETUP PHASE
        if phase == 'SETUP':

            st.session_state['last_phase'] = phase # Save/Update the last known phase (SETUP)

            time_placeholder.markdown(f"{timer_style_warning}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)

            # When the phase is complete (time == 0)
            if display_timer <= 0:
                phase = 'SHOOT'
                display_timer = st.session_state['shooting_time']
                play_buzzer(buzzer_audio_placeholder, 1)
            else:
                st.session_state['last_setup_time'] = display_timer - 1
                #display_timer -= 1

        # Logic if in SHOOT PHASE
        elif phase == 'SHOOT':

            st.session_state['last_phase'] = phase # Save/Update the last known phase (SHOOT)

            ## Timer Colors

            # If both URGENT and WARNING colors are enabled
            if st.session_state['use_urgent_color'] and st.session_state['use_warning_color']:
                if display_timer <= st.session_state['low_time_urgent']:
                    time_placeholder.markdown(f"{timer_style_urgent}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)
                elif display_timer <= st.session_state['low_time_warning']:
                    time_placeholder.markdown(f"{timer_style_warning}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)
                else:
                    time_placeholder.markdown(f"{timer_style_green}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)

            # If only URGENT color is enabled
            elif st.session_state['use_urgent_color'] and not st.session_state['use_warning_color']:
                if display_timer <= st.session_state['low_time_urgent']:
                    time_placeholder.markdown(f"{timer_style_urgent}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)
                else:
                    time_placeholder.markdown(f"{timer_style_green}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)
            
            # If only WARNING color is enabled
            elif not st.session_state['use_urgent_color'] and st.session_state['use_warning_color']:
                if display_timer <= st.session_state['low_time_warning']:
                    time_placeholder.markdown(f"{timer_style_warning}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)
                else:
                    time_placeholder.markdown(f"{timer_style_green}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)
            
            # If no colors are enabled
            else:
                    time_placeholder.markdown(f"{timer_style_green}{time.strftime('%M:%S', time.gmtime(display_timer))}{end_center_style}", unsafe_allow_html=True)

            # When the phase is complete (time == 0)
            if display_timer <= 0:
                phase = 'HOLD'
                st.session_state['last_phase'] = phase

                if st.session_state['is_double_line']:

                    if current_line == starting_line:
                        current_line = next_line

                        play_buzzer(buzzer_audio_placeholder, 2)
                    
                        st.session_state['current_line'] = current_line
                        line_placeholder.markdown(f"{style_small_default}Line: {current_line}{end_center_style}", unsafe_allow_html=True)

                        phase = 'SETUP'
                        st.session_state['last_phase'] = phase
                        display_timer = st.session_state['setup_time']

                    else:
                        play_buzzer(buzzer_audio_placeholder, 3)

                        phase_placeholder.markdown(f"{style_small_default}{phase}{end_center_style}", unsafe_allow_html=True)
                        if st.session_state['alternate_line']:
                            current_line = next_line
                        else:
                            current_line = 'A'
                        st.session_state['current_line'] = current_line
                        
                        st.session_state['current_end'] += 1

                        st.session_state['last_phase'] = 'SETUP'

                        st.session_state['last_setup_time'] = st.session_state['setup_time']
                        st.session_state['last_shooting_time'] = st.session_state['shooting_time']
                                               
                        time.sleep(5)
                        line_placeholder.markdown(f"{style_small_default}Line: {current_line}{end_center_style}", unsafe_allow_html=True)
                        end_number_placeholder.markdown(f"{style_small_default}End: {st.session_state['current_end']}/{st.session_state['num_scoring_ends']}{end_center_style}", unsafe_allow_html=True)
                        
                        st.session_state['timer_active'] = False
                        st.rerun()
                        #break
                else:
                        play_buzzer(buzzer_audio_placeholder, 3)

                        phase_placeholder.markdown(f"{style_small_default}{phase}{end_center_style}", unsafe_allow_html=True)
                        current_line = 'A'
                        st.session_state['current_line'] = current_line
                        
                        st.session_state['current_end'] += 1
                        
                        st.session_state['last_phase'] = 'SETUP'

                        st.session_state['last_setup_time'] = st.session_state['setup_time']
                        st.session_state['last_shooting_time'] = st.session_state['shooting_time']
                     
                        time.sleep(5)
                        line_placeholder.markdown(f"{style_small_default}Line: {current_line}{end_center_style}", unsafe_allow_html=True)
                        end_number_placeholder.markdown(f"{style_small_default}End: {st.session_state['current_end']}/{st.session_state['num_scoring_ends']}{end_center_style}", unsafe_allow_html=True)

                        st.session_state['timer_active'] = False
                        st.rerun()
                        #break
            else:
                st.session_state['last_shooting_time'] = display_timer - 1
        
        display_timer -= 1
        time.sleep(1)
        

if advance_phase_button_placeholder.button("Next Phase", use_container_width=True):
    st.session_state['last_setup_time'] = 2
    st.session_state['last_shooting_time'] = 2
    st.session_state['timer_active'] = False
    st.session_state['skip_buzzer'] = True
    st.rerun()

if timer_controls_placeholder.button("Start/Stop", use_container_width=True):
    if st.session_state['timer_active'] == False:
        st.session_state['timer_active'] = True
        run_timer(st.session_state['last_setup_time'], st.session_state['last_shooting_time'], st.session_state['last_phase'], st.session_state['current_line'])
    else:
        st.session_state['timer_active'] = False

if timer_settings_placeholder.button("Settings", use_container_width=True):
    st.session_state['timer_active'] = False
    st.switch_page("./pages/Timer_Settings.py")

add_keyboard_shortcuts({
    's': 'Start/Stop',
    'n': 'Next Phase >>'
})

###################### DEBUG ################
#st.session_state