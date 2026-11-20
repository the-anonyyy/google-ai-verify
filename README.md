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
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Support & Community](#support--community)
- [Credits](#credits)
- [License](#license)

## Pitch

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
### Windows

```
powershell
git clone https://github.com/the-anonyyy/google-ai-verify.git
cd google-ai-verify
.\run-all.ps1

### macOS

```
git clone https://github.com/the-anonyyy/google-ai-verify.git
cd google-ai-verify
adb devices
sh run-macos.sh
```

The launchers install pinned dependencies (textual==8.2.8, frida==16.5.9) on first run when needed.


## Usage:
1.  Start MuMuPlayer (or compatible rooted Android) with root and ADB enabled, Google Play and Google One signed in.
2.  Run the platform launcher - .\run-all.ps1 (for windows) or sh run-macos.sh ( for macos).
3.  In the dashboard, select Check Device & Offers for Step 1 (lists offers, no checkout).
4.  Review live status. Use advanced run modes only when intentionally selecting a specific stage.
5.  For CLI on Windows: 
.\run-all.ps1 -Step 1
.\run-all.ps1 -Step 0
.\run-all.ps1 -AllStages

Optional flags: -Serial emulator-5554, -Email "account@gmail.com".
Steps 2–5 can open real Google Play checkout and may submit a subscription. Verify every outcome directly in Google Play.

No central .env or JSON config is required for normal operation. Sensitive account lists belong in gitignored accounts.txt files.

## FAQ
Does Step 1 charge money?
No. Step 1 only lists offers. Steps 2–5 can open real checkouts.
Is MuMuPlayer included?
No. Install it yourself from the official site.
Can I use any Android emulator?
A rooted, ADB-enabled instance is required. MuMuPlayer is the supported workflow on Windows.
Where are logs?
Technical logs in logs/, stage reports in ultra0-report/.
Does the toolkit guarantee eligibility or free subscriptions?
No. Verify every offer, charge, and renewal directly in Google Play.
How do I stop a running stage?
Use the dashboard Stop controls. Stop does not reverse a submitted Google Play checkout.
Support & Community
Channel : https://t.me/CracKz_Hubb   (@CracKz_Hubb)
Contact : https://t.me/Trusted_Liar_0  (@Trusted_Liar_0)

## Credits
© 2026 Anony. All rights reserved.
License
MIT License. Copyright (c) 2026 Anony. See LICENSE.

Maintained by Anony · 2026
Channel : https://t.me/CracKz_Hubb   (@CracKz_Hubb)
Contact : https://t.me/Trusted_Liar_0  (@Trusted_Liar_0)
