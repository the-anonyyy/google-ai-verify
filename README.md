<div align="center">
  <h1>Google Ai Kit By Anony™</h1>
  <p><em>Any Google Subscription Unlocked</em></p>
</div>

<p align="center">
  <a href="https://github.com/the-anonyyy/google-ai-verify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://github.com/the-anonyyy/google-ai-verify/releases"><img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="Version"></a>
  <a href="https://github.com/the-anonyyy/google-ai-verify"><img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg" alt="Platform"></a>
  <a href="https://t.me/CracKz_Hubb"><img src="https://img.shields.io/badge/Telegram-Channel-blue.svg" alt="Telegram Channel"></a>
  <a href="https://t.me/Trusted_Liar_0"><img src="https://img.shields.io/badge/Telegram-Contact-blue.svg" alt="Telegram Contact"></a>
</p>

## Table of Contents

- [What it does](#what-it-does)
- [Requirements](#requirements)
- [Installation](#installation)
  - [1. Emulator Setup (MuMuPlayer)](#1-emulator-setup-mumuplayer)
  - [2. Repository Setup (Windows)](#2-repository-setup-windows)
  - [3. Repository Setup (macOS)](#3-repository-setup-macos)
  - [4. Dashboard Usage Workflow](#4-dashboard-usage-workflow)
- [FAQ](#faq)
- [Support & Community](#support--community)
- [Credits](#credits)
- [License](#license)

## Info

Google Ai Kit is a terminal toolkit for Windows and macOS that inspects Google AI Pro offers through a rooted Android environment, ADB, Frida, and Google Play. It provides a Textual dashboard and CLI for listing available offers and guiding through subscription stages.

## What it does

- Lists available Google AI Pro offers for a signed-in Google account on Android (Step 1).
- Guides through sequential stages (Steps 2–5) that can open Google Play checkout flows for 12-month and +6-month offers.
- Diagnoses and prepares the Android/ADB/Frida environment (Step 0).
- Supports both a Textual TUI dashboard and direct PowerShell/CLI modes on Windows; native shell launcher on macOS.
- Handles device serial selection and optional account email constraints.

## Requirements

| Software / configuration | Windows | macOS |
| --- | --- | --- |
| Terminal and shell | PowerShell 5.1+ | Built-in Terminal (zsh or bash) |
| Python | 3.10+ (`python`) | 3.10+ (`python3`); local `.venv` created by launcher |
| Git | Git for Windows | Git (Xcode CLT or Homebrew) |
| Android | Rooted, ADB-enabled instance; MuMuPlayer for Windows supported | Rooted device or emulator; MuMuPlayer Pro for Mac (Apple Silicon) |
| Apps | Google Play Store and Google One, signed in | Same |
| ADB / Platform-Tools | Launcher can locate or download | Install separately (`brew install android-platform-tools`) |
| Frida | 16.5.9 (prepared by setup helper) | 16.5.9 (installed into `.venv`) |
| Start command | `.\run-all.ps1` | `sh run-macos.sh` |


## Installation
This toolkit requires a rooted Android environment (MuMuPlayer) connected via ADB to run Frida scripts. Follow these steps carefully.

## 1. Emulator Setup (MuMuPlayer)

1. **Download & Install MuMuPlayer**
   - Go to the official MuMuPlayer website (NetEase).
   - Download the Windows or Mac (Apple Silicon) installer.
   - Install it and launch the emulator.

2. **Enable Root & ADB**
   - Open MuMuPlayer settings (gear icon).
   - Go to **"Root Permission"** and turn it **ON**.
   - Go to **"ADB Debugging"** and turn it **ON**.
   - Restart the emulator instance to apply changes.

3. **Install Google Apps**
   - MuMuPlayer usually comes with Google Play Store pre-installed. If not, use the MuMu Store to install it.
   - Open Google Play Store, sign in with your Google account.
   - Open Google One (install it from Play Store if needed) and sign in with the same account.
   - 
## 2. Repository Setup (Windows)

1. **Install Prerequisites**
   - **Python 3.10+**: Download from `python.org`. **IMPORTANT:** Check "Add Python to PATH" during installation.
   - **Git**: Download from `git-scm.com`.

2. **Clone Repo & Run**
   - Open PowerShell (Windows Terminal).
   - Run the following commands:
     ```powershell
     git clone https://github.com/the-anonyyy/google-ai-verify.git
     cd google-ai-verify
     .\run-all.ps1
     ```

3. **Initial Setup**
   - On first run, the launcher will automatically install required Python packages (`textual`, `frida`).
   - It will also locate or download ADB if not found in your PATH.
   - The Textual Dashboard will open.

4. **Connect Emulator**
   - Ensure MuMuPlayer is running.
   - Click **"Check Device & Offers"** in the dashboard (Step 1).
   - If ADB is not connected, the toolkit will attempt to connect automatically to common MuMu ports (`127.0.0.1:16384`, etc.).
   - Verify the device is detected in the Live Status panel.

## 3. Repository Setup (macOS)

1. **Install Prerequisites**
   - **Python 3.10+**: Install via `brew install python` or download from `python.org`.
   - **ADB**: Install via Homebrew: `brew install android-platform-tools`.
   - **Git**: Install via Xcode Command Line Tools (`xcode-select --install`) or Homebrew.

2. **Clone & Run**
   - Open Terminal.
   - Run the following commands:
     ```bash
     git clone https://github.com/the-anonyyy/google-ai-verify.git
     cd google-ai-verify
     adb devices
     sh run-macos.sh
     ```
   - `adb devices` should list your emulator (e.g., `127.0.0.1:16384 device`). If not, start MuMuPlayer Pro and enable ADB.

3. **Initial Setup**
   - The launcher creates a local `.venv` and installs `textual` and `frida`.
   - The Textual Dashboard will open in the terminal.
     
## 4. Dashboard Usage Workflow

Once the dashboard is open and the emulator is connected:

1. **Step 0 — Environment**
   - Select **"Check Device & Offers"** or run the Environment stage.
   - This verifies ADB, root access, and installs `frida-server` on the Android device.
   - It also pushes the required billing module APK (`/data/local/tmp/module_521.apk`).

2. **Step 1 — Available Offers**
   - Select **"Check Device & Offers"** (or the List Offers stage).
   - The toolkit injects Frida, queries the Google Play Billing API, and displays available offers (e.g., `12months-eft`).
   - This step does **not** initiate a purchase.

3. **Step 2–5 — Checkout (Warning: Real Charges Possible)**
   - Select a specific stage (e.g., **Step 2 — Pro 12 months**).
   - The toolkit launches the Google Play checkout sheet inside the emulator.
   - **You must verify the price on the emulator screen.**
   - If the price shows `$0.00` or "Free Trial", the toolkit will confirm the subscription. If it shows a real price, it will abort.
   - **Important:** After each checkout step, verify the subscription status directly in Google Play inside the emulator.
   - 
   
    For CLI on Windows: 
.\run-all.ps1 -Step 1
.\run-all.ps1 -Step 0
.\run-all.ps1 -AllStages

Optional flags: -Serial emulator-5554, -Email "account@gmail.com".
Steps 2–5 can open real Google Play checkout and may submit a subscription. Verify every outcome directly in Google Play.

No central .env or JSON config is required for normal operation. Sensitive account lists belong in gitignored accounts.txt files.

## FAQ
# Q) Does Step 1 charge money?
A) No. Step 1 only lists offers. Steps 2–5 can open real checkouts.
# Q) Is MuMuPlayer included?
A) No. Install it yourself from the official site.
# Q) Can I use any Android emulator?
A) A rooted, ADB-enabled instance is required. MuMuPlayer is the supported workflow on Windows.
# Q) Where are logs?
A) Technical logs in logs/, stage reports in ultra0-report/.
# Q) Does the toolkit guarantee eligibility or free subscriptions?
A) No. Verify every offer, charge, and renewal directly in Google Play.
# Q) How do I stop a running stage?
A) Use the dashboard Stop controls. Stop does not reverse a submitted Google Play checkout.

## Support & Community
Channel : https://t.me/CracKz_Hubb   (@CracKz_Hubb)
Group : https://t.me/Crackz_Hub   (@Crackz_Hub)
Contact : https://t.me/Trusted_Liar_0  (@Trusted_Liar_0)

## Credits
© 2026 Anony. All rights reserved.
Channel : https://t.me/CracKz_Hubb   (@CracKz_Hubb)
Contact : https://t.me/Trusted_Liar_0  (@Trusted_Liar_0)

## License
MIT License. 
Copyright (c) 2026 Anony. 
