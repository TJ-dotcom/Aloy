#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

# Set environment variable
os.environ["GOOGLE_API_KEY"] = "AIzaSyAG2etNNhF0jFo7mUC847JqcPzdCLid7Tw"

try:
    from compiler.main import app
    
    # Test with current directory
    current_dir = Path('.')
    print(f"Testing with directory: {current_dir.absolute()}")
    print(f"Directory exists: {current_dir.exists()}")
    print(f"requirements.txt exists: {(current_dir / 'requirements.txt').exists()}")
    
    if __name__ == "__main__":
        # Run the app
        app()
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
