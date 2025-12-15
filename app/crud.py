from datetime import datetime , timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models

ALERT_COOLDOWN_MINUTES = 30
def create_bin(
        db: Session,
        name: str,
        location: str | None,
        warning_threshold: int,
        full_threshold: int,
) -> models.Bin:
    b = models.Bin(
        name=name,
        location=location,
        warning_threshold=warning_threshold,
        full_threshold=full_threshold,
        current_level=0,
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return b

def list_bins(db: Session)->list[models.Bin]:
    return db.query(models.Bin).order_by(models.Bin.id).all()

def get_bin(db: Session, bin_id: int) -> models.Bin | None:
    return db.query(models.Bin).filter(models.Bin.id == bin_id).first()


def create_reading_and_maybe_alert(
        db:Session,
        bin_id:int,
        fill_percent:int,
) ->tuple[models.Reading, models.Alert | None]:
    
    b=get_bin(db, bin_id)
    if not b:
        raise ValueError("Bin not found")
    
    reading=models.Reading(bin_id=bin_id, fill_percent=fill_percent)

    db.add(reading)
    b.current_level=fill_percent
    db.commit()
    db.refresh(reading)

    level=_determine_level_(
        fill_percent=fill_percent,
        warning_threshold=b.warning_threshold,
        full_threshold=b.full_threshold,
    )

    if not level:
        return reading, None
    
    alert= _create_alert_if_needed(
        db=db,
        bin_id=bin_id,
        level=level,
        fill_percent=fill_percent,
    )
    return reading, alert
def _determine_level_(
    fill_percent:int,
    warning_threshold:int,
    full_threshold:int,
)-> str | None:
    if fill_percent >= full_threshold:
        return "FULL"
    if fill_percent >= warning_threshold:
        return "WARNING"
    return None

def _create_alert_if_needed(
    db:Session,
    bin_id:int,
    level:str,
    fill_percent:int,
)-> models.Alert | None:
    cutoff=datetime.utcnow() - timedelta(minutes=ALERT_COOLDOWN_MINUTES)

    recent=(
        db.query(models.Alert)
        .filter(
            models.Alert.bin_id == bin_id,
            models.Alert.level == level,
            models.Alert.created_at >= cutoff,
        )
        .order_by(desc(models.Alert.created_at))
        .first()
    )
    if recent:
        return None
    
    open_same=(
        db.query(models.Alert)
        .filter(models.Alert.bin_id == bin_id)
        .filter(models.Alert.level == level)
        .filter(models.Alert.status == "OPEN")
        .order_by(desc(models.Alert.created_at))
        .first()
    )
    if open_same:
        return None
    
    msg = f"{level} alert: fill_percent={fill_percent}"
    alert = models.Alert(
        bin_id=bin_id,
        level=level,
        status="OPEN",
        message=msg,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def list_alerts(
        db:Session,
        status:str | None = None,
        bin_id:int | None = None,
) -> list[models.Alert]:
    query=db.query(models.Alert)
    if status:
        query=query.filter(models.Alert.status == status)
    if bin_id:
        query=query.filter(models.Alert.bin_id == bin_id)
    return query.order_by(desc(models.Alert.created_at)).all()

def update_alert_status(
        db:Session,
        alert_id:int,
        status:str
) -> models.Alert | None:
    a=db.query(models.Alert).filter(models.Alert.id == alert_id).first()

    if not a:
        return None

    a.status = status
    if status == "RESOLVED":
        a.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(a)
    return a