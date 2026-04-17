import streamlit as st
import base64
from api_call import note_generator , audio_generator, quiz_generator


# 1. Force the sidebar to be open from the start
st.set_page_config(
    page_title="Note Summary & Quiz Generator",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. The Final Fixed CSS
st.markdown("""
    <style>
    /* 1. Make the Fork/GitHub icons invisible without deleting the header container */
    /* This prevents the sidebar from breaking */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0px;
    }

    /* 2. Lock the Sidebar OPEN and remove the 'X' (close) button */
    button[aria-label="Close sidebar"] {
        display: none !important;
    }

    /* 3. Remove the 'Open' arrow (if it somehow collapses) */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* 4. Force the sidebar to stay visible on all devices */
    section[data-testid="stSidebar"] {
        display: flex !important;
        min-width: 300px !important;
    }

    /* 5. Pull content up to fill the gap left by the hidden header */
    .block-container {
        padding-top: 2rem !important;
    }

    /* 6. Hide the footer branding */
    footer {
        visibility: hidden;
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
                    
