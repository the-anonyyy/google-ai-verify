# Google Ai Kit™ - macOS Runner
# Anony t.me/Trusted_Liar_0 · t.me/CracKz_Hubb
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("  Google Ai Kit™ - Anony Engine VIP (macOS)")
    print("  Channel: https://t.me/CracKz_Hubb")
    print("=" * 60)
    
    if not Path("ultra0.py").exists():
        print("[!] ultra0.py not found.")
        sys.exit(1)
        
    # Execute the main engine
    subprocess.run([sys.executable, "ultra0.py"] + sys.argv[1:])

if __name__ == "__main__":
    main()