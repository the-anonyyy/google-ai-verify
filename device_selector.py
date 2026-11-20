# Google Ai Kit™ - Device Selector
import subprocess
import sys

def select_device(adb_path: str) -> str:
    try:
        out = subprocess.run([adb_path, "devices"], capture_output=True, text=True).stdout
        devices = [line.split("\t")[0] for line in out.splitlines()[1:] if "\tdevice" in line]
        
        if not devices:
            print("[!] No Android devices found. Is MuMu running?")
            return None
            
        if len(devices) == 1:
            return devices[0]
            
        print("[?] Multiple devices detected:")
        for i, dev in enumerate(devices):
            print(f"  {i+1}) {dev}")
            
        choice = input("Select device number: ")
        return devices[int(choice)-1]
    except Exception as e:
        print(f"[!] Error selecting device: {e}")
        return None