from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from database import SessionLocal, Order, Inventory
from schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from services.alerts import check_sla_and_alert  
router = APIRouter(prefix="/orders", tags=["Orders"])

# Dependency: Opens a database session per request and securely closes it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # 1. Extract details from the flexible JSONB payload
    power = order.lens_details.get("power", "0.00")
    coating = order.lens_details.get("coating", "None")

    # 2. MODULE 1 LOGIC: Check in-house inventory
    in_stock_item = db.query(Inventory).filter(
        Inventory.lens_type == order.lens_type,
        Inventory.power == str(power),
        Inventory.coating == coating,
        Inventory.stock_count > 0
    ).first()

    # 3. Apply the routing decision based on the data
    if in_stock_item:
        initial_status = "In-House - Fast Track"
        # Optional: Deduct from inventory (in_stock_item.stock_count -= 1)
    else:
        initial_status = "External Order Processing"

    # 4. Create and save the order with the new intelligent status
    db_order = Order(
        source=order.source,
        status=initial_status,
        lens_type=order.lens_type,
        store_location=order.store_location,
        lens_details=order.lens_details
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.get("/", response_model=list[OrderResponse])
def get_active_orders(db: Session = Depends(get_db)):
    # Retrieves all orders that haven't been delivered
    return db.query(Order).filter(Order.status != "Delivered").all()


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int, 
    update_data: OrderStatusUpdate, 
    background_tasks: BackgroundTasks, # Inject BackgroundTasks here
    db: Session = Depends(get_db)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = update_data.status
    
    if update_data.delay_reason:
        current_details = dict(db_order.lens_details)
        current_details["delay_log"] = update_data.delay_reason
        db_order.lens_details = current_details
    
    db.commit()
    db.refresh(db_order)

    # --- MODULE 3: AI SLA PREDICTION ---
    # Calculate exactly how many hours this order has been active
    # Note: Using naive datetime to match SQLAlchemy's default timestamp setup
    time_diff = datetime.now() - db_order.created_at
    hours_elapsed = time_diff.total_seconds() / 3600

    # Add the AI check to the background task queue
    background_tasks.add_task(
        check_sla_and_alert,
        order_id=db_order.id,
        lens_type=db_order.lens_type,
        coating=db_order.lens_details.get("coating", "None"),
        store_location=db_order.store_location,
        current_stage=update_data.status,
        
        # To trigger the alert immediately for the demo, we simulate a massive delay
        # by artificially adding 80 hours to the elapsed time.
        time_elapsed_hours=hours_elapsed + 80.0 
    )
    
    return db_order