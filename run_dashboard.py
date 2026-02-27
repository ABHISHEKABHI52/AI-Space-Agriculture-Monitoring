"""
Run Dashboard
Convenience script to start the Streamlit dashboard
"""

import sys
import os
import subprocess


def main():
    """Main function to run dashboard"""
    print("=" * 70)
    print(" " * 10 + "🌱 Plant Health Monitoring Dashboard 🚀")
    print("=" * 70)
    print("\n Starting Streamlit application...")
    print("\n Dashboard will open in your browser automatically.")
    print(" Press Ctrl+C to stop the server.\n")
    print("=" * 70)
    
    # Path to streamlit app
    app_path = os.path.join("app", "streamlit_app.py")
    
    if not os.path.exists(app_path):
        print(f"\n❌ Dashboard file not found: {app_path}")
        return 1
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.headless", "false"
        ])
        return 0
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
