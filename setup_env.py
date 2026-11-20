# Google Ai Kit™ - Environment Setup
import os
import subprocess
import sys
from pathlib import Path

def install_frida():
    try:
        import frida
        if frida.__version__.startswith("16."):
            print(f"   [OK] frida {frida.__version__} installed.")
            return
    except ImportError:
        pass
    print("   [*] Installing frida==16.5.9...")
    subprocess.run([sys.executable, "-m", "pip", "install", "frida==16.5.9"], check=True)

def main():
    print("=" * 60)
    print("  Google Ai Kit™ - Setup")
    print("=" * 60)
    install_frida()
    print("\n[OK] Environment ready. Run: python ultra0.py --check")

if __name__ == "__main__":
    main()