from pathlib import Path
import subprocess

EP_ROOT = Path(".").resolve()
EP_BUILD_DIR = Path("./build").resolve()
EXPECTED_MSGS = ["Generating the epJSON schema!", "generating embedded epJSON schema"]


def build():
    lines = subprocess.check_output(
        [
            "cmake",
            "--build",
            str(EP_BUILD_DIR),
            "--config",
            "Release",
        ],
        encoding="utf-8",
        stderr=subprocess.STDOUT,
    ).splitlines()
    return lines


IDD_IN = EP_ROOT / "idd/Energy+.idd.in"
assert IDD_IN.exists()


def ensure_target_built(lines, msg):
    lines = [x.strip() for x in lines if "epJSON schema" in x]
    missing_lines = set(EXPECTED_MSGS) - set(lines)
    assert lines == EXPECTED_MSGS, f"{msg}: missing: {missing_lines}: {lines}"

errors = []

# Build: first time: we get both
lines = build()
try:
    ensure_target_built(lines, "Failed on first build")
except Exception as e:
    errors.append(str(e))

# Insert a fake IDD change, we should also get both
with open(IDD_IN, "r") as f:
    lines = f.read().splitlines()
ori_lines = lines.copy()

lines.append("")
lines.append("FakeObject,")
with open(IDD_IN, "w") as f:
    f.write("\n".join(lines) + "\n")

lines = build()
try:
    ensure_target_built(lines, "Failed after IDD change")
except Exception as e:
    errors.append(str(e))

with open(IDD_IN, "w") as f:
    f.write("\n".join(ori_lines) + "\n")

lines = build()
try:
    ensure_target_built(lines, "Failed after IDD change revert")
except Exception as e:
    errors.append(str(e))

assert not errors, "\n".join(errors)
