# Package Metadata Patch

The original repository contains no `package.json`, `pyproject.toml`, or `setup.py`. It is a script-based toolkit.

If packaging is added later, use the following values:

## Suggested pyproject.toml snippet

```toml
[project]
name = "google-ai-kit"
version = "1.0.0"
description = "Any Google Subscription Unlocked"
authors = [{name = "Anony"}]
license = {text = "MIT"}
keywords = ["google", "ai", "android", "adb", "frida"]
requires-python = ">=3.10"
dependencies = [
  "frida==16.5.9",
  "textual==8.2.8",
]

[project.urls]
Homepage = "https://t.me/CracKz_Hubb"
Repository = "https://github.com/the-anonyyy/google-ai-verify"
Bugs = "https://github.com/the-anonyyy/google-ai-verify/issues"