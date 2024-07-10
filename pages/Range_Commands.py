#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st
import base64
import time

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
#with open(CSS_FILE) as f:
#    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
            col3_1.markdown(md, unsafe_allow_html=True)
            time.sleep(num_times)

#-------------------#
#   Page Elements   #
#-------------------#

online_text = "<center style='text-align: center; font-size: 12em; color: #cf7c11'>ON LINE</center>"
begin_text = "<center style='text-align: center; font-size: 12em; color: #0cc93f'>BEGIN</center>"
clear_text = "<center style='text-align: center; font-size: 12em; color: #2695d1'>CLEAR</center>"
hold_text = "<center style='text-align: center; font-size: 12em; color: #c94b0c'>HOLD</center>"

st.header("Range Commands")

st.text("")
st.text("")

if st.session_state['last_command'] == "ON LINE":
    command_text_placeholder = st.markdown(f"{online_text}", unsafe_allow_html=True)

elif st.session_state['last_command'] == "BEGIN":
    command_text_placeholder = st.markdown(f"{begin_text}", unsafe_allow_html=True)

elif st.session_state['last_command'] == "CLEAR":
    command_text_placeholder = st.markdown(f"{clear_text}", unsafe_allow_html=True)

else:
    command_text_placeholder = st.markdown(f"{hold_text}", unsafe_allow_html=True)

st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")

## Setup Two Column Layout
col2_1, col2_2, col2_3, col2_4 = st.columns(4)
col3_1, col3_2, col3_3, col3_4 = st.columns(4)

#-------------------#
#     Core Logic    #
#-------------------#

if col2_1.button("ON LINE", use_container_width=True):
    command_text_placeholder.markdown(f"{online_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'ON LINE'
    play_buzzer(2)
    st.rerun()

if col2_2.button("BEGIN", use_container_width=True):
    command_text_placeholder.markdown(f"{begin_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'BEGIN'
    play_buzzer(1)
    st.rerun()

if col2_3.button("CLEAR", use_container_width=True):
    command_text_placeholder.markdown(f"{clear_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'CLEAR'
    play_buzzer(3)
    st.rerun()

if col2_4.button("HOLD", use_container_width=True, type="primary"):
    command_text_placeholder.markdown(f"{hold_text}", unsafe_allow_html=True)
    st.session_state['last_command'] = 'HOLD'

col3_3.text("")
col3_4.text("")
buzzer_enable_placeholder = col3_4.empty()
buzzer_text_placeholder = col3_4.empty()

if st.session_state['is_range_buzzer_enabled']:
    buzzer_text_placeholder.write(f"Buzzer: Enabled")
else:
    buzzer_text_placeholder.write(f"Buzzer: Disabled")

if buzzer_enable_placeholder.button("Toggle Buzzer", use_container_width=True):
    if st.session_state['is_range_buzzer_enabled']:
        st.session_state['is_range_buzzer_enabled'] = False
    else:
        st.session_state['is_range_buzzer_enabled'] = True
    st.rerun()

css = '''
<style>
section.main > div:has(~ footer ) {
    padding-bottom: 5px;
}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

###################### DEBUG ################
# st.session_state