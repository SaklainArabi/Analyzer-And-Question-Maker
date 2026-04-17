from google import genai
import os
from dotenv import load_dotenv
from gtts import gTTS
import io

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# note generator
def note_generator(uploaded_files):
     content=[]
     for f in uploaded_files:
          f.seek(0)
          
          content.append({
          "inline_data": {
               "mime_type": f.type,
               "data": f.read()
          }})
     prompt =f"summarize the files in a way that is essential for exam for each file and make sure to keep the important points and key takeaways in the summary and also give as many bullet points for each file"
     content.append(prompt)
     response = client.models.generate_content(
          model ="gemini-3-flash-preview",
          contents = content
     )
     return response.text


def audio_generator(text):
     speech = gTTS(text,lang="en",slow = False)
     audio_buffer = io.BytesIO()
     speech.write_to_fp(audio_buffer)
     return audio_buffer


def quiz_generator(uploaded_files,difficulty):
     content2=[]
     for f in uploaded_files:
          f.seek(0)
          
          content2.append({
          "inline_data": {
               "mime_type": f.type,
               "data": f.read()
          }})
          prompt =f"""
     Act as an expert Academic Examiner. Analyze each file individually.
     Generate 5 MCQs for EACH file at a {difficulty} difficulty level.
     Provide 4 options for each question.
     At the end, provide an 'Answer Key & Explanations' section with 1-2 sentence justifications.Strict Rule: Do not hallucinate information. Only use the content found within the uploaded files.
     """
          content2.append(prompt)
          response2 = client.models.generate_content(
               model ="gemini-3-flash-preview",
               contents = content2
          )
     return response2.text
