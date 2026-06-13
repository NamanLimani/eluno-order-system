import pandas as pd
import numpy as np
import random
import os

# Ensure the data directory exists
os.makedirs("mlops/data", exist_ok=True)

def generate_historical_orders(num_records=1000):
    np.random.seed(42)
    random.seed(42)

    data = []
    lens_types = ["Single Vision", "Progressive", "Plano"]
    coatings = ["None", "Anti-Reflective", "Blue Light", "Transitions"]
    locations = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Online"]
    stages = ["Intake", "Inventory Check", "Processing", "QC", "Shipped"]

    for i in range(num_records):
        lens = random.choice(lens_types)
        coating = random.choice(coatings)
        loc = random.choice(locations)
        stage = random.choice(stages)
        
        # Base processing time in hours
        base_time = random.uniform(1, 48)
        
        # Add complexity multipliers
        if lens == "Progressive":
            base_time *= 1.5
        if coating != "None":
            base_time *= 1.2
        if stage == "QC" or stage == "Processing":
            base_time += random.uniform(5, 15)

        # SLA Thresholds (e.g., 48 hours for Single Vision, 72 for Progressive)
        sla_limit = 72 if lens == "Progressive" else 48
        
        # Determine if it breached based on the calculated base_time + some noise
        time_elapsed = base_time + random.uniform(-5, 10)
        
        # 1 = Breached, 0 = Safe
        breached_sla = 1 if time_elapsed > sla_limit else 0

        data.append({
            "order_id": f"HIST-{1000 + i}",
            "lens_type": lens,
            "coating": coating,
            "store_location": loc,
            "current_stage": stage,
            "time_elapsed_hours": round(time_elapsed, 2),
            "breached_sla": breached_sla
        })

    df = pd.DataFrame(data)
    filepath = "mlops/data/historical_orders.csv"
    df.to_csv(filepath, index=False)
    print(f"✅ Generated {num_records} synthetic orders and saved to {filepath}")
    
    # Print a quick distribution of the target variable
    print(df['breached_sla'].value_counts(normalize=True))

if __name__ == "__main__":
    generate_historical_orders()