from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[schemas.AlertOut])
def list_alerts(
    status: str | None = Query(default=None, pattern="^(OPEN|ACK|RESOLVED)$"),
    bin_id: int | None = None,
    db: Session = Depends(get_db),
):
     return crud.list_alerts(db=db, status=status, bin_id=bin_id)

@router.patch("/{alert_id}", response_model=schemas.AlertOut)
def update_alert(alert_id: int, payload: schemas.AlertUpdate, db: Session = Depends(get_db)):
    a = crud.update_alert_status(db=db, alert_id=alert_id, status=payload.status)
    if not a:
        raise HTTPException(status_code=404, detail="Alert not found")
    return a