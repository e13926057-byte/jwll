from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.models import DesignRequest, DesignRequestStatus
from schemas.schemas import (
    DesignRequestCreate,
    DesignRequestUpdate,
    DesignRequestResponse
)
from routers.auth import get_current_user
from models.models import User

router = APIRouter(prefix="/api/design-requests", tags=["Design Requests"])


@router.get("", response_model=List[DesignRequestResponse])
def get_design_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    requests = db.query(DesignRequest).filter(
        DesignRequest.user_id == current_user.id
    ).all()
    return requests


@router.get("/{request_id}", response_model=DesignRequestResponse)
def get_design_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    design_request = db.query(DesignRequest).filter(
        DesignRequest.id == request_id
    ).first()
    if not design_request:
        raise HTTPException(status_code=404, detail="Design request not found")
    return design_request


@router.post("", response_model=DesignRequestResponse)
def create_design_request(
    request_data: DesignRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_request = DesignRequest(
        user_id=current_user.id,
        jeweler_id=request_data.jeweler_id,
        generated_design_id=request_data.generated_design_id,
        description=request_data.description,
        attachment_url=request_data.attachment_url,
        estimated_budget=request_data.estimated_budget,
        status=DesignRequestStatus.PENDING
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


@router.put("/{request_id}", response_model=DesignRequestResponse)
def update_design_request(
    request_id: int,
    request_update: DesignRequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    design_request = db.query(DesignRequest).filter(
        DesignRequest.id == request_id
    ).first()
    if not design_request:
        raise HTTPException(status_code=404, detail="Design request not found")
    
    if request_update.jeweler_price_offer:
        design_request.jeweler_price_offer = request_update.jeweler_price_offer
    if request_update.status:
        design_request.status = DesignRequestStatus[request_update.status.value.upper()]
    
    db.commit()
    db.refresh(design_request)
    return design_request


@router.get("/jeweler/all", response_model=List[DesignRequestResponse])
def get_all_jeweler_requests(
    jeweler_id: int,
    db: Session = Depends(get_db)
):
    requests = db.query(DesignRequest).filter(
        DesignRequest.jeweler_id == jeweler_id
    ).all()
    return requests
