import sys
import os

# Ensure Python can find the 'steps' and 'pipelines' folders inside mlops
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipelines.training_pipeline import run_training_pipeline

if __name__ == "__main__":
    run_training_pipeline()