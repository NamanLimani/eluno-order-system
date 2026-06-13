import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

# 1. Establish the connection string (Dynamic for Docker vs Local)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://eluno_admin:eluno_password@localhost:5432/eluno_orders")

# 2. Create the Database Engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Define the Order Table Schema
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)              # e.g., 'Website', 'In-Store'
    status = Column(String, default="Intake")        # Tracks the state-machine stage
    lens_type = Column(String, index=True)           # e.g., 'Single Vision', 'Progressive', 'Plano'
    store_location = Column(String)
    
    # THE HYBRID FLEXIBILITY COLUMN
    lens_details = Column(JSONB) 

    # SLA Tracking Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# 4. Define the Inventory Table Schema
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    lens_type = Column(String, index=True)
    power = Column(String)     # e.g., "-2.00"
    coating = Column(String)   # e.g., "Anti-Reflective"
    stock_count = Column(Integer, default=0)

# Create the tables in the database
Base.metadata.create_all(bind=engine)