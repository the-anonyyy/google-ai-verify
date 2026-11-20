#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Google Ai Kit™ - Any Google Subscription Unlocked
Main engine. Created by Anony.
Channel: https://t.me/CracKz_Hubb

Usage:
    python3 ultra0.py --check            # 1. Environment check
    python3 ultra0.py accounts.txt       # 2. Batch process accounts
    python3 ultra0.py --account a@b.com:pw:2fa   # 3. Single account
"""
import argparse, base64, hashlib, hmac, json, os, re, select, struct, subprocess, sys, threading, time
from pathlib import Path
import tempfile

HUMAN_EVENT = threading.Event()
WAITING = {"on": False, "msg": ""}

def wait_human(msg: str, timeout: int = 600) -> bool:
    WAITING["on"] = True
    WAITING["msg"] = msg
    print(f"\n[!] ACTION REQUIRED: {msg}")
    print("    Press [ENTER] when done to continue.", flush=True)
    HUMAN_EVENT.clear()
    end = time.time() + timeout
    while time.time() < end:
        if HUMAN_EVENT.is_set():
            break
        try:
            r, _, _ = select.select([sys.stdin], [], [], 0.5)
            if r:
                sys.stdin.readline()
                break
        except Exception:
            time.sleep(0.5)
    WAITING["on"] = False
    print("[*] Continuing execution", flush=True)
    return True

# ---------- Constants ----------
PKG = "com.google.android.apps.subscriptions.red"   # Google One
VENDING = "com.android.vending"                     # Play Store
GMS = "com.google.android.gms"
PRODUCT = "g1.play.20tb"                            # Ultra 5x / 20TB
OFFER = "eft-12month"                               # First year free
MODULE_REMOTE = "/data/local/tmp/module_521.apk"
FRIDA_REMOTE = "/data/local/tmp/frida-server"
REPORT_DIR = Path("ultra0-report")

ADB_CANDIDATES = [
    os.environ.get("ADB_PATH", ""),
    r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe",
    r"C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\adb.exe",
    r"C:\Program Files\Netease\MuMu\emulator\nemu\vmonitor\bin\adb_server.exe",
    r"C:\Program Files\Netease\MuMu\nx_main\adb.exe",
    r"C:\Program Files (x86)\Netease\MuMuPlayer-12.0\shell\adb.exe",
    "adb.exe", "adb",
    os.path.expanduser("~/Library/Android/sdk/platform-tools/adb"),
    "/opt/homebrew/bin/adb", "/usr/local/bin/adb", "/usr/bin/adb",
]

def find_adb() -> str:
    for c in ADB_CANDIDATES:
        if not c:
            continue
        if c in ("adb", "adb.exe") or Path(c).exists():
            try:
                subprocess.run([c, "version"], capture_output=True, timeout=5)
                return c
            except Exception:
                continue
    sys.exit("[!] adb not found. Please install Android platform-tools and add to PATH")

ADB = None
SERIAL = None

def sh(*args, timeout=60, check=False, binary=False):
    cmd = [ADB] + (["-s", SERIAL] if SERIAL else []) + list(args)
    p = subprocess.run(cmd, capture_output=True, timeout=timeout)
    if check and p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "ignore")[:300])
    return p.stdout if binary else p.stdout.decode("utf-8", "ignore").strip()

def note(msg): print(f"   {msg}", flush=True)
def step(msg): print(f"\n[*] {msg}", flush=True)
def ok(msg): print(f"   [+] {msg}", flush=True)
def warn(msg): print(f"   [!] {msg}", flush=True)

# ---------- Device ----------
def pick_device():
    global SERIAL
    out = sh("devices")
    lines = [l for l in out.splitlines()[1:] if "\tdevice" in l]
    if not lines:
        for port in ("16384", "7555", "16416", "62001", "21503"):
            try:
                sh("connect", f"127.0.0.1:{port}", timeout=10)
            except Exception:
                pass
            out = sh("devices")
            lines = [l for l in out.splitlines()[1:] if "\tdevice" in l]
            if lines:
                note(f"Connected emulator 127.0.0.1:{port}")
                break
    if not lines:
        sys.exit("[!] No device detected. Ensure MuMu is running and ADB is enabled.")
    SERIAL = lines[0].split("\t")[0]
    ok(f"Device connected: {SERIAL}")

def ensure_root():
    def _id():
        try:
            return sh("shell", "id", timeout=15)
        except Exception:
            return ""
    uid = _id()
    if "uid=0" not in uid:
        try:
            sh("root", timeout=20)
            time.sleep(2)
            uid = _id()
            if "uid=0" in uid:
                note("Root acquired via adb root")
        except Exception:
            pass
    if "uid=0" not in uid:
        try:
            uid = sh("shell", "su -c id", timeout=15)
        except Exception:
            uid = ""
    if "uid=0" not in uid:
        sys.exit("[!] Device lacks root. Enable root in MuMu settings or run adb root.")

def ensure_frida_server():
    running = "frida-server" in sh("shell", "ps -A | grep frida-server || true")
    if running:
        ok("frida-server running")
        return
    if not sh("shell", f"ls {FRIDA_REMOTE} 2>/dev/null"):
        warn("frida-server not found on device, downloading...")
        try:
            import frida
            ver = frida.__version__
        except Exception:
            sys.exit("[!] frida not installed on PC. Run: pip3 install frida==16.5.9")
        abi = sh("shell", "getprop ro.product.cpu.abi").strip() or "arm64-v8a"
        arch = {"arm64-v8a": "arm64", "armeabi-v7a": "arm", "armeabi": "arm",
                "x86_64": "x86_64", "x86": "x86"}.get(abi, "arm64")
        note(f"Device ABI={abi} -> frida-server-{ver}-android-{arch}")
        url = (f"https://github.com/frida/frida/releases/download/{ver}/"
               f"frida-server-{ver}-android-{arch}.xz")
        import urllib.request, lzma
        tmp = Path(tempfile.gettempdir()) / "frida-server.xz"
        note(f"Downloading {url}")
        with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
            f.write(r.read())
        raw = Path(tempfile.gettempdir()) / "frida-server"
        with lzma.open(tmp, "rb") as fi, open(raw, "wb") as fo:
            fo.write(fi.read())
        sh("push", str(raw), FRIDA_REMOTE, timeout=180)
        sh("shell", f"chmod 755 {FRIDA_REMOTE}")
    is_root = "uid=0" in sh("shell", "id")
    if is_root:
        sh("shell", f"nohup {FRIDA_REMOTE} -D >/dev/null 2>&1 &", timeout=15)
    else:
        sh("shell", f"su -c 'nohup {FRIDA_REMOTE} -D >/dev/null 2>&1 &'", timeout=15)
    for _ in range(20):
        time.sleep(0.5)
        if "frida-server" in sh("shell", "ps -A | grep frida-server || true"):
            ok("frida-server started")
            return
    sys.exit("[!] Failed to start frida-server")

def read_purchase_token(sku_short: str) -> str:
    import tempfile, sqlite3, json as _json
    remote = "/data/local/tmp/lib_read.db"
    try:
        sh("shell", f"cp /data/data/{VENDING}/databases/library.db {remote} 2>/dev/null; chmod 666 {remote}", timeout=30)
    except Exception:
        pass
    tmp = Path(tempfile.gettempdir()) / "lib_read.db"
    try:
        if tmp.exists(): tmp.unlink()
        sh("pull", remote, str(tmp), timeout=60)
    except Exception as e:
        warn(f"Failed to pull library.db: {e}")
        return ""
    if not tmp.exists(): return ""
    tok = ""
    try:
        con = sqlite3.connect(str(tmp))
        cur = con.cursor()
        rows = cur.execute("select account, subs_valid_until_time, inapp_purchase_data from ownership where doc_id like ?", (f"%{sku_short}%",)).fetchall()
        now_ms = int(time.time() * 1000)
        picked = None
        for account, valid, data in rows:
            if not data: continue
            try: j = _json.loads(data)
            except Exception: continue
            tk = j.get("purchaseToken")
            if not tk: continue
            try: alive = int(valid) > now_ms
            except Exception: alive = False
            if picked is None or (alive and not picked[2]) or (alive == picked[2] and int(valid or 0) > picked[3]):
                picked = (tk, account, alive, int(valid or 0))
        if picked:
            tok = picked[0]
            note(f"purchaseToken source: {picked[1]} ({'active' if picked[2] else 'expired'})")
        con.close()
    except Exception as e:
        warn(f"Failed to read library.db: {e}")
    finally:
        try: tmp.unlink()
        except Exception: pass
    return tok

def ensure_vending():
    if sh("shell", f"pidof {VENDING}"):
        ok("Play Store running")
        return
    warn("Play Store not running, launching...")
    sh("shell", f"monkey -p {VENDING} -c android.intent.category.LAUNCHER 1", timeout=30)
    for _ in range(20):
        time.sleep(1)
        if sh("shell", f"pidof {VENDING}"):
            ok("Play Store launched")
            time.sleep(2)
            return
    warn("Play Store failed to start, billing queries may hang.")

def ensure_module_apk():
    if sh("shell", f"ls {MODULE_REMOTE} 2>/dev/null"):
        ok("Billing module ready")
        return
    note("Pushing billing module (one-time)...")
    tmp = Path(tempfile.gettempdir()) / "module_521.apk"
    tmp.write_bytes(base64.b64decode(MODULE_B64))
    sh("push", str(tmp), MODULE_REMOTE, timeout=120)
    ok("Billing module pushed")

def ensure_network():
    proxy = sh("shell", "settings get global http_proxy")
    if proxy and proxy != "null" and proxy != ":0":
        sh("shell", "settings put global http_proxy :0")
        warn(f"Cleared device proxy (was {proxy})")
    for p in ("com.github.metacubex.clash.meta", "com.github.kr328.clash"):
        if sh("shell", f"pm list packages | grep -q {p} && echo yes"):
            sh("shell", f"am force-stop {p}")
            warn(f"Stopped {p} (intercepts Play network)")

# ---------- UI ----------
def ui_xml() -> str:
    sh("shell", "uiautomator dump /sdcard/ui.xml")
    return sh("shell", "cat /sdcard/ui.xml")

def nodes(xml: str):
    for m in re.finditer(r"<node[^>]*>", xml):
        s = m.group(0)
        t = re.search(r'text="([^"]*)"', s)
        d = re.search(r'content-desc="([^"]*)"', s)
        b = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', s)
        c = re.search(r'class="([^"]*)"', s)
        if not b: continue
        yield {
            "text": (t.group(1) if t else "") or "",
            "desc": (d.group(1) if d else "") or "",
            "cls": (c.group(1) if c else "") or "",
            "x": (int(b.group(1)) + int(b.group(3))) // 2,
            "y": (int(b.group(2)) + int(b.group(4))) // 2,
        }

def tap(x, y): sh("shell", f"input tap {x} {y}")
def type_text(s: str): sh("shell", f"input text '{s.replace(' ', '%s')}'")

def tap_text(*needles, exact=False) -> bool:
    for n in nodes(ui_xml()):
        label = n["text"] or n["desc"]
        if not label: continue
        hit = (label == needles[0]) if exact and needles else any(k in label for k in needles)
        if hit and (n["x"] or n["y"]):
            tap(n["x"], n["y"])
            return True
    return False

def find_edit():
    for n in nodes(ui_xml()):
        if "EditText" in n["cls"]:
            return n["x"], n["y"]
    return None

# ---------- TOTP ----------
def totp(secret: str, digits=6, period=30) -> str:
    if not secret: return ""
    s = re.sub(r"[^A-Za-z2-7]", "", secret).upper()
    s += "=" * ((8 - len(s) % 8) % 8)
    key = base64.b32decode(s)
    ctr = int(time.time()) // period
    mac = hmac.new(key, struct.pack(">Q", ctr), hashlib.sha1).digest()
    off = mac[-1] & 0x0F
    code = (struct.unpack(">I", mac[off:off + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)

# ---------- Account ----------
def accounts_on_device() -> list:
    out = sh("shell", "dumpsys account | grep 'type=com.google'")
    return out.splitlines()

def add_account(email, password, totp_secret="") -> bool:
    step(f"Adding account to device: {email}")
    before = len(accounts_on_device())
    sh("shell", "am start -a android.settings.ADD_ACCOUNT_SETTINGS")
    time.sleep(3)
    tap_text("Google", exact=True) or tap_text("Google")
    time.sleep(5)

    pos = find_edit()
    if pos:
        for _ in range(3):
            tap(*pos); time.sleep(0.8)
            sh("shell", "input keyevent 123")
            for _ in range(60): sh("shell", "input keyevent 67")
            type_text(email); time.sleep(1)
            cur = " ".join(n["text"] for n in nodes(ui_xml()) if "@" in n["text"])
            if email.lower() in cur.lower(): break
        tap_text("下一步", "Next"); time.sleep(6)

    if find_edit():
        tap(*find_edit()); time.sleep(1)
        type_text(password); time.sleep(1)
        tap_text("下一步", "Next"); time.sleep(7)

    unknown_rounds = 0
    for _ in range(90):
        if len(accounts_on_device()) > before:
            ok("Account added"); return True
        xml = ui_xml()
        text = " ".join(n["text"] for n in nodes(xml) if n["text"])

        if "already on your device" in text.lower():
            ok("Account already on device"); return True
        if "Couldn't find your Google Account" in text:
            warn("Account not found"); return False
        if "Wrong password" in text:
            warn("Wrong password"); return False

        if ("2-Step" in text or "Verify" in text or "验证码" in text):
            if totp_secret and find_edit():
                code = totp(totp_secret)
                note(f"2FA code: {code}")
                tap(*find_edit()); type_text(code); time.sleep(1)
                tap_text("下一步", "Next"); time.sleep(8)
                continue
            wait_human("Enter 2FA code on device", 300)
            continue

        if tap_text("Not now", "以后再说"): time.sleep(3); continue
        if tap_text("I agree", "我同意"): time.sleep(5); continue
        if tap_text("Skip", "取消", "跳过"): time.sleep(2); continue

        if any(k in text for k in ("Verify it's you", "确认是您本人", "验证身份")):
            wait_human("Complete identity verification on device", 300)
            continue

        unknown_rounds += 1
        if unknown_rounds >= 8:
            wait_human("Manual action required to finish adding account", 300)
            unknown_rounds = 0
        time.sleep(2)

    warn("Add account timeout")
    return False

def add_card(card: dict) -> bool:
    if not card: return True
    step(f"Adding payment method: {card['number'][-4:].rjust(len(card['number']), '*')}")
    sh("shell", "am start -a android.intent.action.VIEW -d 'https://pay.google.com/gp/w/u/0/home/paymentmethods'")
    time.sleep(10)
    if not tap_text("Add a payment method", "添加付款方式", "Add card"):
        warn("Add payment entry not found"); return False
    time.sleep(9)
    edits = [n for n in nodes(ui_xml()) if "EditText" in n["cls"]]
    mm = re.sub(r"\D", "", card["exp"])[:2] or "01"
    yy = re.sub(r"\D", "", card["exp"])[2:][-2:] or "30"
    seq = [card["number"], mm, yy, card["cvc"], card["holder"] or "CARD HOLDER", "123 Main St", "Portland"]
    for i, val in enumerate(seq):
        edits = [n for n in nodes(ui_xml()) if "EditText" in n["cls"]]
        if i >= len(edits): break
        tap(edits[i]["x"], edits[i]["y"]); time.sleep(0.6)
        type_text(val); time.sleep(0.5)
    if not tap_text("Save", "保存"):
        wait_human("Click 'Save' manually to finish adding card", 240)
    else:
        time.sleep(8)
    ok("Card submission done")
    return True

def current_play_account() -> str:
    for n in nodes(ui_xml()):
        if "Account and settings" in n["desc"] or "账号和设置" in n["desc"]:
            tap(n["x"], n["y"]); time.sleep(3); break
    best = ""
    for n in nodes(ui_xml()):
        m = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+)", n["desc"] + " " + n["text"])
        if m:
            best = m.group(1).lower(); break
    sh("shell", "input keyevent 4")
    return best

def switch_play(email) -> bool:
    step(f"Switching Play account to: {email}")
    want = email.lower()
    sh("shell", f"am force-stop {VENDING}")
    sh("shell", f"am force-stop {PKG}")
    sh("shell", f"am start -n {VENDING}/com.google.android.finsky.activities.MainActivity --es authAccount {email}")
    time.sleep(9)
    if current_play_account() == want:
        ok("Play account verified"); return True
    for n in nodes(ui_xml()):
        if "Account and settings" in n["desc"] or "账号和设置" in n["desc"]:
            tap(n["x"], n["y"]); time.sleep(3); break
    for n in nodes(ui_xml()):
        if "Expand account list" in n["desc"] or "展开账号列表" in n["desc"]:
            tap(n["x"], n["y"]); time.sleep(3); break
    for n in nodes(ui_xml()):
        if want in (n["text"] + " " + n["desc"]).lower():
            tap(n["x"], n["y"]); time.sleep(6); break
    sh("shell", "input keyevent 4")
    got = current_play_account()
    if got == want:
        ok("Play account verified"); return True
    warn(f"Failed to switch Play account (current: {got or 'unknown'}) - aborted.")
    return False

# ---------- Frida Engine ----------
def launch_app() -> int:
    sh("shell", f"am force-stop {PKG}")
    sh("shell", f"monkey -p {PKG} -c android.intent.category.LAUNCHER 1")
    time.sleep(7)
    pid = sh("shell", f"pidof {PKG}")
    return int(pid) if pid.strip().isdigit() else 0

def build_js(plan: str = "auto", list_only: bool = False, stack: bool = False, old_token: str = "", stack_mode=None) -> str:
    js = FRIDA_JS
    if list_only:
        js = js.replace('var PREFER="";', 'var PREFER=""; var LIST_ONLY=true;', 1)
    if stack:
        js = js.replace('var PREFER="";', 'var PREFER=""; var STACK=true;', 1)
    if old_token:
        js = js.replace('var PREFER="";', 'var PREFER=""; var OLD_TOKEN="%s";' % old_token, 1)
    if stack_mode is not None:
        js = js.replace('var PREFER="";', 'var PREFER=""; var STACK_MODE=%d;' % stack_mode, 1)
    if plan == "20x":
        js = js.replace('var PRODUCTS=["g1.play.20tb","g1.play.ai.pro","g1.30tb"];', 'var PRODUCTS=["g1.play.ai.pro","g1.ai.pro","g1.30tb"];')
    elif plan == "5x":
        js = js.replace('var PRODUCTS=["g1.play.20tb","g1.play.ai.pro","g1.30tb"];', 'var PRODUCTS=["g1.play.20tb"];')
    elif plan.startswith("pro"):
        prefer = {"pro12": "12months-eft", "pro6": "6months-eft", "pro6b": "6months-eft-2", "pro6c": "6months-eft-ss-2026"}.get(plan, "12months-eft")
        js = js.replace('var PRODUCTS=["g1.play.20tb","g1.play.ai.pro","g1.30tb"];', 'var PRODUCTS=["g1.2tb.ai.subs_variant"];')
        js = js.replace('var PREFER="";', 'var PREFER="%s";' % prefer, 1)
    return js

def run_trial(pid: int, wait=90, plan="auto", list_only=False, stack=False, old_token="", stack_mode=None) -> dict:
    import frida
    step("Injecting billing module, querying offers")
    dev = frida.get_usb_device(timeout=10)
    sess = dev.attach(pid)
    res = {"offers": [], "launched": None, "purchase": None, "errors": []}

    def on_msg(m, _):
        p = m.get("payload") or {}
        ev = p.get("ev")
        if ev == "offer":
            res["offers"].append(p)
            note(f"offer {p.get('id')} -> {p.get('micros')} ({p.get('p0','')})")
            note(f"    token={p.get('token','')}")
        elif ev == "launched":
            res["launched"] = p
            ok(f"Launched checkout: {p}")
        elif ev == "purchase_cb":
            res["purchase"] = p
        elif ev and ("err" in ev or ev.startswith("no_")):
            res["errors"].append(p)

    sc = sess.create_script(build_js(plan, list_only, stack, old_token, stack_mode))
    sc.on("message", on_msg)
    sc.load()
    time.sleep(wait)
    return res

def handle_verify(password="") -> bool:
    changed = False
    for _ in range(12):
        blob = " ".join(n["text"] for n in nodes(ui_xml()) if n["text"])
        if "Not now" in blob or "以后再说" in blob or "Play Points" in blob:
            tap_text("Not now", "以后再说"); time.sleep(2); changed = True; continue
        if ("Verify" in blob or "验证" in blob) and password:
            es = [n for n in nodes(ui_xml()) if "EditText" in n["cls"]]
            if es:
                tap(es[0]["x"], es[0]["y"]); time.sleep(0.8)
                type_text(password); time.sleep(0.8)
                tap_text("Verify", "验证"); time.sleep(6); changed = True; continue
        break
    return changed

def confirm_zero(wait=40, password="") -> dict:
    step("Checking checkout price (only confirming $0)")
    out = {"price": None, "confirmed": False, "ineligible": False, "text": ""}
    for _ in range(wait // 2):
        xml = ui_xml()
        text = " ".join(n["text"] for n in nodes(xml) if n["text"])
        if "不符合免费试用条件" in text or "not eligible" in text.lower():
            warn("Play: Account not eligible for free trial")
            if tap_text("Got it", "知道了", "OK"):
                time.sleep(2)
            out["ineligible"] = True
            return out
        if ("Subscribe" in text or "订阅" in text) and ("Ultra" in text or "AI" in text):
            out["text"] = text[:300]
            m = re.search(r"(US\$|HK\$|NT\$|\$|€|£)\s?([\d.,]+)", text)
            if m:
                out["price"] = m.group(0)
                try:
                    if float(m.group(2).replace(",", "")) == 0:
                        tap_text("Subscribe", "订阅")
                        out["confirmed"] = True
                        ok("Confirmed $0.00 subscription")
                        return out
                except Exception:
                    pass
                warn(f"Current price {m.group(0)} is not $0.00, not clicking confirm")
                return out
            if (re.search(r"(US\$|HK\$|NT\$|\$)\s?0(\.00)?\b", text)
                    or "US$0/mo" in text or "US$0.00" in text
                    or re.search(r"Free trial \d+ (months|years|mo)", text)):
                tap_text("Subscribe", "订阅")
                out["confirmed"] = True
                ok("Confirmed free trial")
                return out
        time.sleep(2)
    warn("Checkout not detected (already subscribed?)")
    return out

def verify() -> str:
    step("Verifying subscription status")
    sh("shell", f"am start -a android.intent.action.VIEW -d 'https://play.google.com/store/account/subscriptions'")
    time.sleep(9)
    text = " | ".join(n["text"] for n in nodes(ui_xml()) if n["text"])
    if "Ultra" in text:
        ok("Subscription page shows Ultra")
    return text[:500]

# ---------- Single Account Flow ----------
def process(email, password="", totp_secret="", add=True, card=None, plan="auto", no_switch=False, list_only=False, stack=False, old_token="", stack_mode=None) -> dict:
    print("\n" + "=" * 56)
    print(f"  Processing account: {email}")
    print("=" * 56)
    rec = {"email": email, "at": time.strftime("%Y-%m-%dT%H:%M:%S"), "status": "unknown"}
    if add:
        try:
            if not add_account(email, password, totp_secret):
                rec["status"] = "add_account_failed"
                return rec
        except Exception as e:
            warn(f"Add account failed: {e}")
            rec["status"] = "add_account_error"
            return rec
    if card:
        try:
            add_card(card)
        except Exception as e:
            warn(f"Add card failed: {e}")
    if globals().get("SKIP_ACCOUNT_CHECK"):
        ok("Skipped Play account check (--force)")
    elif list_only:
        cur = current_play_account()
        ok(f"List mode: using current device account {cur or 'unknown'} (no check, no purchase)")
    elif no_switch:
        cur = current_play_account()
        if cur != email.lower():
            warn(f"Current Play account is {cur or 'unknown'}, not {email}, aborting")
            rec["status"] = "wrong_account"
            return rec
        ok("Play account verified (manual switch mode)")
    elif not switch_play(email):
        rec["status"] = "play_account_switch_failed"
        return rec
    if stack and not old_token:
        note("Reading purchaseToken...")
        old_token = read_purchase_token("subs_variant")
        if old_token:
            ok(f"purchaseToken found ({old_token[:16]}...), will stack")
        else:
            warn("purchaseToken not found, falling back to queryPurchases (may fail)")

    pid = launch_app()
    if not pid:
        rec["status"] = "app_not_started"
        return rec
    fr = run_trial(pid, plan=plan, list_only=list_only, stack=stack, old_token=old_token, stack_mode=stack_mode)
    rec.update(fr)
    if list_only:
        rec["status"] = "listed"
        return rec
    if fr["launched"] and fr["launched"].get("code") == 0:
        rec["sheet"] = confirm_zero(password=password)
        rec["subscription_page"] = verify()
        rec["status"] = "subscribed" if "Ultra" in rec["subscription_page"] else "launched"
    else:
        rec["status"] = "launch_failed"
    return rec

# ---------- CLI Entry ----------
def do_check():
    global ADB
    ADB = find_adb()
    ok(f"adb: {ADB}")
    pick_device()
    ensure_root()
    ensure_network()
    ensure_frida_server()
    ensure_module_apk()
    ensure_vending()
    try:
        import frida
        ok(f"frida: {frida.__version__}")
    except Exception:
        warn("frida not installed on PC. Run: pip3 install frida==16.5.9")
    ok("Environment check passed. Ready to process accounts.")
    return 0

def parse_accounts(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = [p.strip() for p in line.split("----")]
        while len(parts) < 9: parts.append("")
        rows.append(parts[:9])
    return rows

def parse_card(parts) -> dict | None:
    if len(parts) < 5 or not parts[4]: return None
    return {
        "number": re.sub(r"\s+", "", parts[4]),
        "exp": parts[5] or "",
        "cvc": parts[6] or "",
        "holder": parts[7] or "",
        "zip": parts[8] or "97201",
    }

def main():
    global ADB, SERIAL
    ap = argparse.ArgumentParser(description="Google Ai Kit™ - Any Google Subscription Unlocked")
    ap.add_argument("accounts", nargs="?", help="Account file (email----password----recovery----totp)")
    ap.add_argument("--account", help="Single account: email:password:totp")
    ap.add_argument("--check", action="store_true", help="Run environment check only")
    ap.add_argument("--list", action="store_true", help="List offers only, no checkout (safe)")
    ap.add_argument("--force", action="store_true", help="Skip Play account check")
    ap.add_argument("--mode", type=int, default=None, help="Proration mode: 1-5")
    ap.add_argument("--old-token", default="", help="Old purchaseToken for stacking")
    ap.add_argument("--stack", action="store_true", help="Stack subscription (extend trial)")
    ap.add_argument("--serial", default=None, help="ADB device serial")
    ap.add_argument("--no-add", action="store_true", help="Skip account addition")
    ap.add_argument("--no-switch", action="store_true", help="Don't switch Play account, just verify")
    ap.add_argument("--plan", default="auto", choices=["auto", "5x", "20x", "pro12", "pro6", "pro6b", "pro6c"], help="Plan to query")
    a = ap.parse_args()

    ADB = find_adb()
    globals()["SKIP_ACCOUNT_CHECK"] = bool(a.force)
    if a.check:
        return do_check()

    pick_device()
    if a.serial: SERIAL = a.serial
    ensure_root()
    ensure_network()
    ensure_frida_server()
    ensure_module_apk()
    ensure_vending()

    REPORT_DIR.mkdir(exist_ok=True)
    rows = []
    if a.list and not a.account and not a.accounts:
        a.account = "current@device"
    if a.account:
        parts = a.account.split(":")
        rows = [[parts[0], parts[1] if len(parts) > 1 else "", "", parts[2] if len(parts) > 2 else ""]]
    elif a.accounts:
        rows = parse_accounts(Path(a.accounts))
    else:
        ap.print_help()
        return 1

    print(f"\nProcessing {len(rows)} account(s)...\n")
    results = []
    for i, row in enumerate(rows, 1):
        email, pw, _rec, sec = row[0], row[1], row[2], row[3]
        card = parse_card(row)
        print(f"\n---- Progress {i}/{len(rows)} ----")
        try:
            rec = process(email, pw, sec, add=(not a.no_add and not a.list), card=card, plan=a.plan, no_switch=a.no_switch, list_only=a.list, stack=a.stack, old_token=a.old_token, stack_mode=a.mode)
        except Exception as e:
            rec = {"email": email, "status": "exception", "error": str(e)[:200]}
        results.append(rec)
        (REPORT_DIR / f"{email.split('@')[0]}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"   Status: {rec.get('status')}")

    print("\n" + "=" * 56)
    print("  Summary")
    print("=" * 56)
    for r in results:
        print(f"  {r['email']:<42} {r.get('status')}")
    print(f"\nDetails saved to {REPORT_DIR.resolve()}")
    return 0

entry = main

# ---------- Embedded Resources (Do Not Edit) ----------
FRIDA_JS = r'''// Ultra0 injection script...
var dexLoader=null, ctxRef=null, clientRef=null;
var PRODUCTS=["g1.play.20tb","g1.play.ai.pro","g1.30tb"];
var PREFER="";
function L(v){ Java.classFactory.loader=v; }
function S(o){ send(o); }

function periodRank(p){
  var m={"P1Y":12,"P12M":12,"P6M":6,"P3M":3,"P1M":1};
  return m[String(p)]||0;
}
function getActivity(){
  L(null);
  var found=null;
  try{
    Java.choose("android.app.Activity", {
      onMatch:function(a){ try{ if(!found && !a.isFinishing()) found=a; }catch(e){} },
      onComplete:function(){}
    });
  }catch(e){ S({ev:"choose_err", m:String(e).slice(0,80)}); }
  return found;
}
function boot(){
 Java.perform(function(){
  try{
   L(null);
   ctxRef=Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
   var DexClassLoader=Java.use("dalvik.system.DexClassLoader");
   dexLoader=DexClassLoader.$new("/data/local/tmp/module_521.apk",
      ctxRef.getCodeCacheDir().getAbsolutePath(), null, ctxRef.getClassLoader());
   L(dexLoader);
   var BillingClient=Java.use("com.android.billingclient.api.BillingClient");
   var PUL=Java.use("com.android.billingclient.api.PurchasesUpdatedListener");
   var Lst=Java.registerClass({name:"rc.A"+Date.now(), implements:[PUL], methods:{
     onPurchasesUpdated:function(r,p){ S({ev:"purchase_cb", code:r.getResponseCode(), msg:String(r.getDebugMessage()||"")}); }}});
   var b=BillingClient.newBuilder(ctxRef);
   b.setListener(Lst.$new());
   try{ b.enablePendingPurchases(); }catch(e){}
   clientRef=b.build();
   var SLL=Java.use("com.android.billingclient.api.BillingClientStateListener");
   var SL=Java.registerClass({name:"rc.B"+Date.now(), implements:[SLL], methods:{
     onBillingSetupFinished:function(r){ S({ev:"setup", code:r.getResponseCode()});
        if(r.getResponseCode()===0) query(); },
     onBillingServiceDisconnected:function(){ S({ev:"disc"}); }}});
   clientRef.startConnection(SL.$new());
   S({ev:"connecting", products:PRODUCTS});
  }catch(e){ S({ev:"boot_err", m:String(e).slice(0,200)}); }
 });
}
function query(){
 try{
  L(dexLoader);
  var Prod=Java.use("com.android.billingclient.api.QueryProductDetailsParams$Product");
  var Params=Java.use("com.android.billingclient.api.QueryProductDetailsParams");
  var PDL=Java.use("com.android.billingclient.api.ProductDetailsResponseListener");
  var PL=Java.registerClass({name:"rc.C"+Date.now(), implements:[PDL], methods:{
    onProductDetailsResponse:function(res,list){
      S({ev:"pd", code:res.getResponseCode(), n:(list?list.size():0)});
      if(res.getResponseCode()!==0 || !list || list.size()===0) return;
      L(dexLoader);
      var PD=Java.use("com.android.billingclient.api.ProductDetails");
      var SOD=Java.use("com.android.billingclient.api.ProductDetails$SubscriptionOfferDetails");
      var PP=Java.use("com.android.billingclient.api.ProductDetails$PricingPhase");
      var best=null;
      for(var i=0;i<list.size();i++){
        var pd=Java.cast(list.get(i), PD);
        var pid=String(pd.getProductId());
        var offs=pd.getSubscriptionOfferDetails();
        if(!offs){ S({ev:"no_offers", product:pid}); continue; }
        for(var j=0;j<offs.size();j++){
          var o=Java.cast(offs.get(j), SOD);
          var oid=String(o.getOfferId());
          var tok=String(o.getOfferToken());
          var ph=o.getPricingPhases().getPricingPhaseList();
          var first=Java.cast(ph.get(0), PP);
          var micros=String(first.getPriceAmountMicros());
          var period=String(first.getBillingPeriod());
          S({ev:"offer", product:pid, id:oid, micros:micros, period:period, token:tok, title:String(pd.getTitle()), name:String(pd.getName())});
          if(micros!=="0") continue;
          var rank=periodRank(period);
          if(!best || rank>best.rank || (PREFER && oid===PREFER)){
            if(PREFER && oid!==PREFER) continue;
            best={pd:pd, offer:o, product:pid, id:oid, rank:rank, period:period, token:tok};
          }
        }
      }
      if(!best){ S({ev:"no_trial"}); return; }
      S({ev:"chosen", product:best.product, id:best.id, period:best.period});
      if (typeof LIST_ONLY !== "undefined" && LIST_ONLY) {
        S({ev:"list_only", product:best.product, id:best.id, period:best.period, token:best.token});
        return;
      }
      if (typeof OLD_TOKEN !== "undefined" && OLD_TOKEN) {
        S({ev:"stack_start", product:best.product, id:best.id, src:"provided_token"});
        launch(best.pd, best.offer, OLD_TOKEN);
      } else if (typeof STACK !== "undefined" && STACK) {
        S({ev:"stack_start", product:best.product, id:best.id, src:"query"});
        launchWithStack(best.pd, best.offer);
      } else {
        launch(best.pd, best.offer);
      }
    }}});
  var arr=Java.use("java.util.ArrayList").$new();
  for(var k=0;k<PRODUCTS.length;k++){
    arr.add(Prod.newBuilder().setProductId(PRODUCTS[k]).setProductType("subs").build());
  }
  L(dexLoader);
  clientRef.queryProductDetailsAsync(Params.newBuilder().setProductList(arr).build(), PL.$new());
  S({ev:"query_sent"});
 }catch(e){ S({ev:"query_err", m:String(e).slice(0,200)}); }
}
function launchWithStack(pd, offer){
 try{
  L(dexLoader);
  var QP=Java.use("com.android.billingclient.api.QueryPurchasesParams");
  var PRL=Java.use("com.android.billingclient.api.PurchasesResponseListener");
  var cls=Java.registerClass({name:"rc.P"+Date.now(), implements:[PRL], methods:{
    onQueryPurchasesResponse:function(br, purchases){
      try{
        var list=Java.cast(purchases, Java.use("java.util.List"));
        S({ev:"purchases", n:list.size(), code:String(br.getResponseCode())});
        if(list.size()===0){ S({ev:"no_purchase"}); launch(pd, offer); return; }
        var pu=Java.cast(list.get(0), Java.use("com.android.billingclient.api.Purchase"));
        var tok=String(pu.getPurchaseToken());
        S({ev:"old_purchase", head:tok.slice(0,16), products:String(pu.getProducts())});
        launch(pd, offer, tok);
      }catch(e){ S({ev:"stack_query_err", m:String(e).slice(0,200)}); launch(pd, offer); }
    }}});
  var qp=QP.newBuilder().setProductType("subs").build();
  clientRef.queryPurchasesAsync(qp, cls.$new());
 }catch(e){ S({ev:"stack_outer_err", m:String(e).slice(0,200)}); launch(pd, offer); }
}

function launch(pd, offer, oldTok){
 try{
  L(dexLoader);
  var PDP=Java.use("com.android.billingclient.api.BillingFlowParams$ProductDetailsParams");
  var BFP=Java.use("com.android.billingclient.api.BillingFlowParams");
  var pdp=PDP.newBuilder().setProductDetails(pd).setOfferToken(String(offer.getOfferToken())).build();
  var l=Java.use("java.util.ArrayList").$new(); l.add(pdp);
  var b=BFP.newBuilder().setProductDetailsParamsList(l);
  if(oldTok){
    try{
      var SUP=Java.use("com.android.billingclient.api.BillingFlowParams$SubscriptionUpdateParams");
      var md = (typeof STACK_MODE !== "undefined" && STACK_MODE) ? STACK_MODE : 5;
      var sb=SUP.newBuilder();
      var mode_set=false;
      try{ sb=sb.setReplaceProrationMode(md); mode_set=true; }
      catch(e1){
        try{ sb=sb.setReplaceSkusProrationMode(md); mode_set=true; }
        catch(e2){ S({ev:"mode_err", m:String(e2).slice(0,120)}); }
      }
      S({ev:"mode_applied", mode:md, ok:mode_set});
      var sup=sb.setOldPurchaseToken(String(oldTok)).build();
      b=b.setSubscriptionUpdateParams(sup);
      S({ev:"stack_mode", mode:md, old: String(oldTok).slice(0,16)});
    }catch(e){ S({ev:"stack_param_err", m:String(e).slice(0,160)}); }
  }
  var params=b.build();
  var act=getActivity();
  S({ev:"activity", a: act? String(act.getClass().getName()) : "null"});
  if(!act){ S({ev:"no_activity"}); return; }
  L(null);
  var Handler=Java.use("android.os.Handler"); var Looper=Java.use("android.os.Looper");
  var R=Java.registerClass({name:"rc.R"+Date.now(), implements:[Java.use("java.lang.Runnable")], methods:{
    run:function(){
      try{
        L(dexLoader);
        var Activity=Java.use("android.app.Activity");
        var r2=clientRef.launchBillingFlow(Java.cast(act, Activity), params);
        S({ev:"launched", code:r2.getResponseCode(), msg:String(r2.getDebugMessage()||"")});
      }catch(e){ S({ev:"launch_err", m:String(e).slice(0,200)}); }
    }}});
  Handler.$new(Looper.getMainLooper()).post(R.$new());
 }catch(e){ S({ev:"launch_outer_err", m:String(e).slice(0,200)}); }
}
var __tries=0;
var iv=setInterval(function(){
  try{
    L(null);
    var a=Java.use("android.app.ActivityThread").currentApplication();
    __tries++;
    if(a || __tries>10){ clearInterval(iv); S({ev:"boot_start", app:!!a, tries:__tries}); boot(); }
  }catch(e){
    __tries++;
    if(__tries>10){ clearInterval(iv); S({ev:"boot_force", m:String(e).slice(0,120)}); try{ boot(); }catch(e2){ S({ev:"boot_fail", m:String(e2).slice(0,160)}); } }
  }
},400);
'''

MODULE_B64 = (
    "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"
    "jmO89c/V9qu
[file content end]