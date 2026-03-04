import os
import google.generativeai as genai
from PIL import Image
import io
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def configure_gemini():
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    return False

def generate_jewelry_design(design_data: dict, output_dir: str = "static/generated_designs"):
    if not configure_gemini():
        return None, "Gemini API key not configured"
    
    try:
        prompt = f"""
        Create a stunning, photorealistic jewelry design with the following specifications:
        
        Type: {design_data['type']} (Ring, Necklace, Bracelet, or Earrings)
        Primary Metal: {design_data['material']} {design_data['karat']} - highly polished, luxurious finish
        Metal Color: {design_data['color']} - rich and elegant tone
        Design Shape: {design_data['shape']} - intricate and sophisticated pattern
        Gemstone Type: {design_data['gemstone_type']}
        Gemstone Color: {design_data['gemstone_color']} - brilliant and sparkling
        
        Style Requirements:
        - Professional jewelry photography style
        - Studio lighting with soft reflections
        - Ultra-detailed, 8K quality render
        - Elegant presentation on a simple background
        - Luxury aesthetic suitable for high-end jewelry catalog
        - Sharp focus on craftsmanship details
        
        The piece should look like it's from a premium luxury jewelry collection.
        """
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
        
        response = model.generate_content(prompt)
        
        image_data = None
        if response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                    break
        
        if not image_data and hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            image_data = part.inline_data.data
                            break
        
        if not image_data:
            return None, "No image generated"
        
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"design_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        image_bytes = base64.b64decode(image_data) if isinstance(image_data, str) else image_data
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        return f"/static/generated_designs/{filename}", None
        
    except Exception as e:
        return None, str(e)