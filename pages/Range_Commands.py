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
CSS_FILE = THIS_DIR / ".." / "style" / "style.css"
ASSETS = THIS_DIR / ".." / "assets"

### Function to get query parameters
def get_range_name():
    query_params = st.experimental_get_query_params()
    return query_params.get("range", ["Unofficial Archery"])[0]

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯")

### Apply Custom CSS
with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#-------------------#
#   Session State   #
#-------------------#
if 'last_command' not in st.session_state:
    st.session_state['last_command'] = 'HOLD'

if 'is_range_buzzer_enabled' not in st.session_state:
    st.session_state['is_range_buzzer_enabled'] = False


#-------------------#
#   Page Elements   #
#-------------------#

st.markdown("#")
st.markdown("#")
st.markdown("#")

#col1_1, col1_2, col1_3, col1_4 = st.columns(4)

command_text_placeholder = st.empty()

st.markdown("#")
st.markdown("#")
st.markdown("#")

## Setup Two Column Layout
col2_1, col2_2, col2_3, col2_4 = st.columns(4)
col3_1, col3_2, col3_3, col3_4 = st.columns(4)

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

#-------------------#
#     Core Logic    #
#-------------------#

if st.session_state['last_command'] == 'ON LINE':
    play_buzzer(2)
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #cf7c11'>ON LINE</center>", unsafe_allow_html=True)

elif st.session_state['last_command'] == 'BEGIN':
    play_buzzer(1)
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #0cc93f'>BEGIN</center>", unsafe_allow_html=True)

elif st.session_state['last_command'] == 'CLEAR':
    play_buzzer(3)
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #2695d1'>CLEAR</center>", unsafe_allow_html=True)

else:
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #c94b0c'>HOLD</center>", unsafe_allow_html=True)


if col2_1.button("ON LINE", use_container_width=True):
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #cf7c11'>ON LINE</center>", unsafe_allow_html=True)
    st.session_state['last_command'] = 'ON LINE'

if col2_2.button("BEGIN", use_container_width=True):
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #0cc93f'>BEGIN</center>", unsafe_allow_html=True)
    st.session_state['last_command'] = 'BEGIN'

if col2_3.button("CLEAR", use_container_width=True):
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #2695d1'>CLEAR</center>", unsafe_allow_html=True)
    st.session_state['last_command'] = 'CLEAR'

if col2_4.button("HOLD", use_container_width=True, type="primary"):
    command_text_placeholder.markdown(f"<center style='text-align: center; font-size: 12em; color: #c94b0c'>HOLD</center>", unsafe_allow_html=True)
    st.session_state['last_command'] = 'HOLD'

buzzer_text_placeholder = col3_4.empty()
buzzer_enable_placeholder = col3_4.empty()

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

###################### DEBUG ################
#st.session_state