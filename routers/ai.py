from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import base64
from datetime import datetime

import google.generativeai as genai

from database import get_db
from models.models import UserGeneratedDesign, DesignRequest, DesignRequestStatus, User
from schemas.schemas import (
    AIGenerateDesignRequest, 
    UserGeneratedDesignResponse,
    DesignRequestCreate,
    DesignRequestUpdate,
    DesignRequestResponse
)
from routers.auth import get_current_user

router = APIRouter(prefix="/api/ai", tags=["AI Design"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)


def construct_prompt(data: AIGenerateDesignRequest) -> str:
    prompt = f"""Create a high-quality, photorealistic jewelry design with the following specifications:
    
    Type: {data.type}
    Color: {data.color}
    Shape: {data.shape}
    Material: {data.material}
    Karat: {data.karat}
    Gemstone Type: {data.gemstone_type}
    Gemstone Color: {data.gemstone_color}
    
    The design should be elegant, luxurious, and suitable for a high-end jewelry brand. 
    Professional product photography style with elegant background."""
    return prompt


@router.post("/generate-design", response_model=UserGeneratedDesignResponse)
def generate_ai_design(
    design_data: AIGenerateDesignRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    try:
        prompt = construct_prompt(design_data)
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content(
            [prompt],
            generation_config={
                "response_modalities": ["image", "text"]
            }
        )
        
        image_data = None
        for part in response.parts:
            if hasattr(part, 'image') and part.image:
                image_data = part.image
                break
        
        if not image_data:
            raise HTTPException(status_code=500, detail="Failed to generate image")
        
        static_dir = "static/generated_designs"
        os.makedirs(static_dir, exist_ok=True)
        
        filename = f"design_{uuid.uuid4().hex}.png"
        filepath = os.path.join(static_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_data)
        
        design_record = UserGeneratedDesign(
            user_id=current_user.id,
            selected_options=design_data.dict(),
            generated_image_url=f"/static/generated_designs/{filename}"
        )
        db.add(design_record)
        db.commit()
        db.refresh(design_record)
        
        return design_record
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")


@router.get("/designs", response_model=List[UserGeneratedDesignResponse])
def get_user_designs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    designs = db.query(UserGeneratedDesign).filter(
        UserGeneratedDesign.user_id == current_user.id
    ).all()
    return designs


@router.get("/designs/{design_id}", response_model=UserGeneratedDesignResponse)
def get_design(
    design_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    design = db.query(UserGeneratedDesign).filter(
        UserGeneratedDesign.id == design_id,
        UserGeneratedDesign.user_id == current_user.id
    ).first()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design
