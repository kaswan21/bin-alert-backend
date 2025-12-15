from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/readings", tags=["readings"])


@router.post("", response_model=dict)
def create_reading(payload: schemas.ReadingCreate, db: Session = Depends(get_db)):
    try:
        reading, alert = crud.create_reading_and_maybe_alert(
            db=db,
            bin_id=payload.bin_id,
            fill_percent=payload.fill_percent,
        )
    except ValueError as e:
        if str(e) == "BIN_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Bin not found")
        raise

    return {
        "reading": schemas.ReadingOut.model_validate(reading),
        "alert": schemas.AlertOut.model_validate(alert) if alert else None,
    }