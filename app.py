import streamlit as st
import base64
from api_call import note_generator , audio_generator, quiz_generator

# 1. Set the initial state to auto so it doesn't break mobile layouts
st.set_page_config(
    page_title="Note Summary & Quiz Generator",
    layout="wide",
    initial_sidebar_state="auto" 
)
# 2. The Comprehensive CSS
st.markdown("""
    <style>
    /* --- GLOBAL RULES (Applies to all devices) --- */
    
    /* 1. Kill the entire header (Deletes Fork, GitHub, and Deploy buttons) */
    header[data-testid="stHeader"], 
    [data-testid="stStatusWidget"], 
    #MainMenu {
        display: none !important;
    }

    /* 2. Remove footer branding */
    footer {
        visibility: hidden;
    }

    /* 3. Adjust top padding for a clean look */
    .block-container {
        padding-top: 2rem !important;
    }


    /* --- RESPONSIVE RULES --- */

    /* DESKTOP: Screens wider than 992px */
    @media (min-width: 992px) {
        /* Lock the sidebar: hide the close buttons */
        button[aria-label="Close sidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    }

    /* MOBILE: Screens narrower than 991px */
    @media (max-width: 991px) {
        /* Keep Fork/GitHub hidden (done in global), but bring back the 
           Sidebar Arrow so mobile users can actually access the controls. */
        [data-testid="collapsedControl"] {
            display: flex !important;
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 999999;
            background-color: #f0f2f6;
            border-radius: 50%;
            padding: 5px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Note Summary and Quiz Generator")
st.markdown("Upload upto 3 file to generate Note summary and Quizzes")
st.divider()
with st.sidebar:
     st.header("Controls")
     uploaded_files = st.file_uploader("Upload the photos of your note",type =["jpg","jpeg","png","pdf"],accept_multiple_files=True)
     if uploaded_files:
          if len(uploaded_files) > 3:
               st.error("Please upload a maximum of 3 files.")
          else:
               st.subheader("Your uploaded Files")
               col = st.columns(len(uploaded_files))
               for i, file in enumerate(uploaded_files):
                    
                         if file.name.lower().endswith(('jpg', 'jpeg', 'png')):
                              with col[i]:
                                   st.image(file)
                         elif file.name.lower().endswith('pdf'):
                              file.seek(0) 
                              pdf_bytes = file.read()
                              base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                              pdf_display = f'''
                                   <iframe 
                                        src="data:application/pdf;base64,{base64_pdf}" 
                                        width="100%" 
                                        height="400" 
                                        type="application/pdf">
                                   </iframe>
                              '''
                              st.markdown(pdf_display, unsafe_allow_html=True)
                         else:
                              st.warning(f"Unsupported file type: {file.name}")    
     select_option= st.radio("Enter the difficulty of your quiz",["Easy","Medium","Hard"],index=None)
     if select_option:
          st.markdown(f"**{select_option}**")
     pressed =st.button("Click the button",type="primary")                   
               # Here you can add code to process the uploaded files and generate summaries and quizzes

if pressed:
     if not uploaded_files:
          st.error("Please upload at least 1 file to generate summary and quiz.")
     elif not select_option:
          st.error("Please select a difficulty level for the quiz.")
     else:
          # note
          with st.container(border = True):
               st.subheader("your note summary")
               with st.spinner("Generating summary..."):
                    summary = note_generator(uploaded_files)
                    st.markdown(summary)
               




          # audio
          # with st.container(border = True):
          #      st.subheader("Audio transcription")
          #      with st.spinner("Generating audio..."):
          #           audio = audio_generator(summary)
          #           st.audio(audio)


          # quiz
          with st.container(border = True):
               st.subheader(f"{select_option} Quiz Questions")
               with st.spinner("Generating quiz questions..."):
                    quiz = quiz_generator(uploaded_files,select_option)
                    st.markdown(quiz)
                    
