"""Gemini API module"""
import os
import google.generativeai as genai
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro-vision')

async def query_gemini(image: UploadFile, prompt: str):
    """Get response text from Gemini for a given image and prompt"""
    image_data = {
        'mime_type': image.content_type,
        'data': image.file.read()
    }
    response = await model.generate_content_async(contents=[prompt, image_data])
    return response.text
