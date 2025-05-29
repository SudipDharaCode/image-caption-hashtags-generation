from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import google.generativeai as genai
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app = FastAPI()


async def image_captioning_generation(image):

    image_bytes = image.file.read()
    image = Image.open(io.BytesIO(image_bytes))

    analysis_prompt = """
        You are a professional social media strategist, specializing in creating viral content for Instagram Reels. Your task is to generate a highly engaging, viral-worthy caption and relevant hashtags based on the image.

        Please create a caption that:

        1. Grabs attention immediately (strong, compelling hook).
        2. Connects emotionally with the audience.
        3. Includes a call-to-action (e.g., asking users to like, comment, or share).
        4. Fits the tone and style that resonates with a broad audience (e.g., fun, inspiring, relatable, or trending).
        5. Is optimized for virality and social sharing.

        Additionally, generate the most relevant and trending hashtags that can increase the reach and discoverability of the reel. Make sure these hashtags are specific to the content and fit into popular trends, ensuring the reel has a better chance of going viral.

        The output should only include the caption and a list of at least 10 hashtags.

        **Output Formate** :
            [
              Caption : Lost in the emerald embrace of the ancient forest. The sound of the cascading water, a symphony of nature's artistry.
              Hashtags : #waterfall, #nature, #naturephotography, #pnwonderland, #explore, #travel, #beautifuldestinations, #instatravel, #travelphotography, #hiking
            ]
    """

    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([analysis_prompt, image], stream=True)
    response.resolve()
    
    return response.text




@app.post("/caption-hashtage/")
async def caption_generation(image: UploadFile = File(...)):
    try:
        result = await image_captioning_generation(image)
        return result
    except Exception as e:
        return {"message": "Failed", "error": str(e)}





# ---------------------------
# Run with: uvicorn filename:app --reload
# ---------------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 

    

    