from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, Inventory

router = APIRouter(prefix="/inventory", tags=["Inventory Operations"])

# Dependency: Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for adding new stock
class InventoryCreate(BaseModel):
    lens_type: str
    power: str
    coating: str
    stock_count: int

@router.get("/")
def get_all_inventory(db: Session = Depends(get_db)):
    """Retrieves the current stock levels of all lenses."""
    return db.query(Inventory).all()

@router.post("/")
def add_inventory_stock(item: InventoryCreate, db: Session = Depends(get_db)):
    """Adds a new physical lens to the warehouse database."""
    # Check if this exact lens already exists
    existing_item = db.query(Inventory).filter(
        Inventory.lens_type == item.lens_type,
        Inventory.power == item.power,
        Inventory.coating == item.coating
    ).first()

    if existing_item:
        # If it exists, just add to the stock count
        existing_item.stock_count += item.stock_count
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # If it is brand new, create a new row
        new_item = Inventory(**item.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item