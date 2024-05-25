from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)


def swagger_patch(*args, **kwargs):
    """
    Для быстрой загрузки документации SwaggerIU
    """

    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")


applications.get_swagger_ui_html = swagger_patch

app = FastAPI()


@app.post("/rolls/", response_model=schemas.Roll)
def create_roll(roll: schemas.RollCreate, db: Session = Depends(get_db)):
    db_roll = models.Roll(length=roll.length, weight=roll.weight, date_removed=roll.date_removed)
    db.add(db_roll)
    db.commit()
    return db_roll


@app.delete("/rolls/{roll_id}", response_model=schemas.Roll)
def delete_roll(roll_id: int, db: Session = Depends(get_db)):
    db_roll = db.query(models.Roll).filter(models.Roll.id == roll_id).first()
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll not found")
    db.delete(db_roll)
    db.commit()
    return db_roll


@app.put("/rolls/{roll_id}/remove_date", response_model=schemas.Roll)
def update_date_removed(roll_id: int, date_delete: schemas.RollDateDelete, db: Session = Depends(get_db)):
    db_roll = db.query(models.Roll).filter(models.Roll.id == roll_id).first()
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll not found")
    db_roll.date_removed = date_delete.date_removed
    db.commit()
    return db_roll


@app.get("/rolls/", response_model=list[schemas.Roll])
def list_rolls(length: float | None = None, weight: float | None = None,
               date_added: datetime | None = None, date_removed: datetime | None = None,
               db: Session = Depends(get_db)):
    query = db.query(models.Roll)
    if length:
        query = query.filter(models.Roll.length == length)
    if weight:
        query = query.filter(models.Roll.weight == weight)
    if date_added:
        query = query.filter(models.Roll.date_added == date_added)
    if date_removed:
        query = query.filter(models.Roll.date_removed == date_removed)
    return query.all()


@app.get("/stats/", response_model=dict)
def status_rolls(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    added_rolls = db.query(models.Roll).filter(models.Roll.date_added.between(start_date, end_date)).count()
    removed_rolls = db.query(models.Roll).filter(models.Roll.date_removed.between(start_date, end_date)).count()

    rolls_in_period = db.query(models.Roll).filter(models.Roll.date_added.between(start_date, end_date)).all()
    if not rolls_in_period:
        raise HTTPException(status_code=404, detail="Roll not found")

    total_length = sum(roll.length for roll in rolls_in_period)
    total_weight = sum(roll.weight for roll in rolls_in_period)
    avg_length = total_length / len(rolls_in_period)
    avg_weight = total_weight / len(rolls_in_period)
    max_length = max(roll.length for roll in rolls_in_period)
    min_length = min(roll.length for roll in rolls_in_period)
    max_weight = max(roll.weight for roll in rolls_in_period)
    min_weight = min(roll.weight for roll in rolls_in_period)

    storage_durations = [(roll.date_removed - roll.date_added).days for roll in rolls_in_period if roll.date_removed]
    if storage_durations:
        max_duration = max(storage_durations)
        min_duration = min(storage_durations)
    else:
        max_duration = None
        min_duration = None

    return {
        "added_rolls": added_rolls,
        "removed_rolls": removed_rolls,
        "average_length": avg_length,
        "average_weight": avg_weight,
        "max_length": max_length,
        "min_length": min_length,
        "max_weight": max_weight,
        "min_weight": min_weight,
        "total_weight": total_weight,
        "max_storage_duration": max_duration,
        "min_storage_duration": min_duration
    }

