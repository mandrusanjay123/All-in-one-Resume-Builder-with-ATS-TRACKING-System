import base64
import io
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert PDF to Image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]

        # Convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts=[
        {
            "mime_type":"image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()

        }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("NO File Uploaded")
    

# streamlit app
st.set_page_config(page_title="ATS RESUME EXPERT")
st.header(" 👨🏻‍💻📝📊 Your All-in one Resume Builder with ATS TRACKING System")
input_text=st.text_area("Job Description:",key="input")
uploaded_file=st.file_uploader("upload your resume(PF)....",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")


submit1=st.button("Tell me about the resume")
submit2=st.button("How can I improvise my skills")
submit3=st.button("Percentage Match")
submit4=st.button("What are the Keywords that are Missing")
draft_question= st.text_area(" Paste your question Here if you want to write a draft related to the job questions")
submit5=st.button("Submit")

input_prompt1="""
You are an experienced Human Resource with the experience in the field of data science ,Full stack,Web development,Big data enginering,DEVOPS,Data Analyst,
 your Task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligins with the role.
 Highlight the strengths and weaknesses of the applicant in the relation to the specified job requirement"""

import_prompt2="""
You are a Technical Human Resource Manager with expertise in data science,,Full stack,Web development,Big data enginering,DEVOPS,Data Analyst,
your role is to scrutinize the resume in light of the job descrption provided.
share your insights on the how candidate can Improve his skills which are suitability for the role from an HR perpective.
additionally, offer advice on enhancing the candidate's skills and identify areas """

input_prompt3 = """
You are a skilled ATS(Applicant Tracking System) scanner with a deep understanding of data science,,Full stack,Web development,Big data enginering,DEVOPS,Data Analyst and ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage match if the resume matches the job description
 first the output should come as percentage and then keywords missing and last final thoughts."""


input_prompt4="""
You are an experienced Human Resource with the experience in the field of data science ,Full stack,Web development,Big data enginering,DEVOPS,Data Analyst,
 your Task is to review the provided resume against the job description for these profiles.
And Tell what are the Keywords missing based on the Job description tell these in a sequential order on what all skills or keywords missing to help Improve the resume"""

input_prompt5="""
You are an experienced Human Resource with the experience in the field of data science ,Full stack,Web development,Big data enginering,DEVOPS,Data Analyst,
 your Task is to review the provided resume against the job description for these profiles.
and based on the job description and the person expertise and skills you have to write a draft answer directly as a human writes dont make the draft too generic make it professional and heighlight the relevance between the person and JD and write all the skills and expertises that are aligned in passages instead of points and don't use any brackets if relevant keep it under 300 words for the question """

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(import_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)

elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)

elif submit5:
    if uploaded_file and draft_question is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(f"{input_prompt5}{draft_question}",pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload the resume")
