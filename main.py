#streamlit python llm
import streamlit as st                  # streamlit for app interface
from pathlib import Path                # pathlib for file paths
import google.generativeai as genai     # to allow interaction with gemini ai model

# configure google gemini api by setting up api key. This will allow us to connect us to 
# ai model and generate insights from medical images

genai.configure(api_key="YOUR_API_KEY")

#setting up the system prompt which defines the role of the AI Model
# the prompt specifies that our AI is a medical image analysis system capable of
# detecting diseases like cancer, cardiovascular issues, neurological diseases and more

#prompt
system_prompt='''
You are an advanced AI medical image analysis system. Your primary role is to assist healthcare professionals in analyzing medical images such as MRI, CT scans, X-rays, PET scans, and ultrasound images. You are capable of detecting, classifying, and describing abnormalities related to:

- Oncology: tumors, cancerous growths, metastasis  
- Cardiovascular: heart disease, arterial blockages, stroke indicators, aneurysms  
- Neurology: neurodegenerative diseases, brain lesions, multiple sclerosis, trauma  
- Pulmonology: pneumonia, tuberculosis, lung nodules, COPD  
- Orthopedics: fractures, bone density issues, joint degeneration  
- Other systemic conditions detectable through imaging  

Your tasks include:  
- Identifying potential diseases or abnormalities in medical images.  
- Highlighting areas of concern with clear reasoning.  
- Suggesting possible next diagnostic steps (further scans, lab tests, biopsy).  
- Clearly communicating uncertainty levels (e.g., possible/probable/likely).  
- Always reminding that final interpretation and diagnosis must be made by a qualified medical professional.  

Constraints:  
- You must not provide definitive diagnoses — only assist with probability-based findings and medical insights.  
- Always include a disclaimer: *“This analysis is for informational purposes only and not a substitute for professional medical diagnosis. Please consult a licensed healthcare provider for confirmation.”*  


'''

generation_config={
    "temperature":1,  # controls randomness of value of 1 given balanced output diversity
    "top_p":0.95,  #uses neuclear sampling selecting tokkens from top 25% cummulative probability distribution for diverse responses
    "top_k":40,  #limits token slection to the top 40 tokens based on the probability. Narrowing possible oututss to high porbability tokens
    "max_output_tokens":8192, #this setting allows for longer responses by limiting the maximum length of the generated text to 8192 tokens
    "response_mime_type": "text/plain"  #specifies the format of the output as plain text
}

#safety settings
safety_settings=[
    {
        "category":"HARM_CATEGORY_HARASSMENT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_HATE_SPEECH",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",   # or gemini-1.0-pro if that’s what you have access to
    generation_config=generation_config,
    safety_settings=safety_settings
)


#layout for streamlit application
st.set_page_config(page_title="diagonistics analytics", page_icon="robot")
col1,col2,col3=st.columns([1,2,1]) #using steamlit columns to center the logo and title and make it look appleaing
with col2:
    st.image("edureka.png",width=200)
    st.image("medical.jpg",width=200)

#use Streamlits file uploader widget to accept image file in PNG,JPG OR JPEG formats
upload_file=st.file_uploader("please upload the medical images for analysis",type=["PNG","JPG","JPEG"])
submit_button=st.button("Generate image analysis")

if submit_button:
    #process the uploaded image
    image_data=upload_file.getvalue()
    # making our image ready
    image_parts=[
        {
            "mime_type":"image/jpeg",
            "data":image_data
        },
    ]
    #making our prompt ready
    prompt_parts=[
        image_parts[0],
        system_prompt,
    ]

    #generate a response based on prompt and image
    response=model.generate_content(prompt_parts)
    print(response.text)


    st.write(response.text)
