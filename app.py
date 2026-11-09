"""
Glacier-Statistical-Analysis-2025 Web App Entry Point
Author: Antigravity Glacier Statistical Analysis Suite

This entry point allows Streamlit Community Cloud and other cloud hosts
to detect and launch the dashboard directly from the repository root.
"""

import os
import sys

# Add dashboard directory to system path
dashboard_dir = os.path.join(os.path.dirname(__file__), "presentation_package", "dashboard")
sys.path.insert(0, dashboard_dir)

# Execute the core dashboard application
dashboard_app = os.path.join(dashboard_dir, "app.py")
with open(dashboard_app, "rb") as f:
    code = compile(f.read(), dashboard_app, "exec")
    exec(code, {"__name__": "__main__", "__file__": dashboard_app})
