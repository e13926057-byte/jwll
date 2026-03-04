from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.auth import get_current_active_user
from services.ai_service import generate_jewelry_design
import models
import schemas
import json

router = APIRouter(prefix="/api", tags=["AI Design"])

@router.post("/ai/generate-design", response_model=schemas.GenerateDesignResponse)
def generate_design(
    design_request: schemas.GenerateDesignRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    image_url, error = generate_jewelry_design(design_request.dict())
    
    if error:
        raise HTTPException(status_code=500, detail=f"Failed to generate design: {error}")
    
    design_data = models.UserGeneratedDesign(
        user_id=current_user.id,
        selected_options=json.dumps(design_request.dict()),
        generated_image_url=image_url
    )
    db.add(design_data)
    db.commit()
    db.refresh(design_data)
    
    return {
        "id": design_data.id,
        "generated_image_url": image_url,
        "message": "Design generated successfully"
    }

@router.get("/designs", response_model=List[schemas.UserGeneratedDesignResponse])
def get_user_designs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    designs = db.query(models.UserGeneratedDesign).filter(
        models.UserGeneratedDesign.user_id == current_user.id
    ).order_by(models.UserGeneratedDesign.created_at.desc()).all()
    return designs

@router.post("/design-requests", response_model=schemas.DesignRequestResponse)
def create_design_request(
    request: schemas.DesignRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    jeweler = db.query(models.Jeweler).filter(
        models.Jeweler.id == request.jeweler_id
    ).first()
    if not jeweler:
        raise HTTPException(status_code=404, detail="Jeweler not found")
    
    if request.generated_design_id:
        design = db.query(models.UserGeneratedDesign).filter(
            models.UserGeneratedDesign.id == request.generated_design_id,
            models.UserGeneratedDesign.user_id == current_user.id
        ).first()
        if not design:
            raise HTTPException(status_code=404, detail="Design not found")
    
    design_request = models.DesignRequest(
        user_id=current_user.id,
        **request.dict()
    )
    db.add(design_request)
    db.commit()
    db.refresh(design_request)
    return design_request

@router.get("/design-requests", response_model=List[schemas.DesignRequestResponse])
def get_design_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    requests = db.query(models.DesignRequest).filter(
        models.DesignRequest.user_id == current_user.id
    ).order_by(models.DesignRequest.request_date.desc()).all()
    return requests

@router.put("/design-requests/{request_id}", response_model=schemas.DesignRequestResponse)
def update_design_request(
    request_id: int,
    update_data: schemas.DesignRequestUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    design_request = db.query(models.DesignRequest).filter(
        models.DesignRequest.id == request_id,
        models.DesignRequest.user_id == current_user.id
    ).first()
    
    if not design_request:
        raise HTTPException(status_code=404, detail="Design request not found")
    
    if update_data.status:
        design_request.status = update_data.status
    if update_data.jeweler_price_offer:
        design_request.jeweler_price_offer = update_data.jeweler_price_offer
    
    db.commit()
    db.refresh(design_request)
    return design_request