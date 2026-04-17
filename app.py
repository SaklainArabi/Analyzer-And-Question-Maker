import streamlit as st
import base64
from api_call import note_generator , audio_generator, quiz_generator

# 1. Essential Page Config (Hiding the sidebar by default on mobile)
st.set_page_config(
    page_title="Note Summary & Quiz Generator",
    layout="wide",
    initial_sidebar_state="auto"
)

# 2. Surgical CSS to hide ONLY Fork, GitHub, and Deploy
st.markdown("""
    <style>
    /* Hides the GitHub icon, Fork text, and Deploy button */
    header[data-testid="stHeader"] div[data-testid="stStatusWidget"],
    .stAppDeployButton {
        display: none !important;
    }
    
    /* Hides the '...' Main Menu (optional, but cleaner) */
    #MainMenu {
        visibility: hidden;
    }

    /* Hides the Streamlit footer */
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# main code

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
                    
