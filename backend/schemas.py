from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
from typing import Optional

# 1. Base structure shared by incoming requests and outgoing responses
class OrderBase(BaseModel):
    source: str = Field(..., examples=["Website", "In-Store"])
    lens_type: str = Field(..., examples=["Single Vision", "Progressive", "Plano"])
    store_location: str = Field(..., examples=["Brooklyn, NY"])
    
    # This matches our PostgreSQL JSONB column
    lens_details: Dict[str, Any] = Field(default_factory=dict, examples=[{"sphere": -2.0, "coating": "Anti-Reflective"}])

# 2. Schema for creating a new order (can add strict creation rules here later)
class OrderCreate(OrderBase):
    pass

# 3. Schema for sending data back to the frontend
class OrderResponse(OrderBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Tells Pydantic to read SQLAlchemy database models

# 4. Schema for updating an order's status and logging delays
class OrderStatusUpdate(BaseModel):
    status: str = Field(..., examples=["Processing", "QC Failed", "Delivered"])
    delay_reason: Optional[str] = Field(default=None, examples=["Lens coating machine broken"])