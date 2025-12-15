from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud,schemas

router = APIRouter(
    prefix="/bins",
    tags=["bins"],
)

@router.post("", response_model=schemas.BinOut)
def create_bin(payload: schemas.BinCreate, db: Session = Depends(get_db)):
  
  if(payload.full_threshold < payload.warning_threshold):
      raise HTTPException(status_code=400, detail="full_threshold must be greater than or equal to warning_threshold")
  
  return crud.create_bin(
        db,
        name=payload.name,
        location=payload.location,
        warning_threshold=payload.warning_threshold,
        full_threshold=payload.full_threshold,
  )

@router.get("", response_model=list[schemas.BinOut])
def list_bins(db: Session = Depends(get_db)):
    return crud.list_bins(db)

@router.get("/{bin_id}", response_model=schemas.BinOut)
def get_bin(bin_id: int, db: Session = Depends(get_db)):
    b = crud.get_bin(db, bin_id)
    if not b:
        raise HTTPException(status_code=404, detail="Bin not found")
    return b