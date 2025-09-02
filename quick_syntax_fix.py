
import textwrap, py_compile, sys, re, os, importlib

FILE = "profit_sprint.py"
start = 320
end   = 341

print("📄  Showing context lines {}-{} of {}".format(start, end-1, FILE))
with open(FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(start, end):
    if i < len(lines):
        print(f"{i:>4}: {lines[i].rstrip()}")

# --- simple auto-patch -------------------------------------------------
changed = False
pattern_try = re.compile(r"^\s*try\s*:\s*$")
pattern_incomplete = re.compile(r"^\s*(except|finally)\b")

for idx in range(len(lines)):
    # find 'try:' with no except/finally before next dedent
    if pattern_try.match(lines[idx]):
        # look ahead for except/finally at same indent
        indent = len(lines[idx]) - len(lines[idx].lstrip())
        for j in range(idx+1, len(lines)):
            if lines[j].strip() == "":         # blank lines OK
                continue
            if len(lines[j]) - len(lines[j].lstrip()) < indent:
                # block ended with no except/finally – fix it
                lines.insert(j, " " * indent + "except Exception as e:\n")
                lines.insert(j+1, " " * (indent+4) + "print('⛔ runtime error:', e)\n")
                changed = True
                print(f"🔧  Added missing except at line {j}")
                break
            if pattern_incomplete.match(lines[j]):  # already has except/finally
                break

if changed:
    with open(FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("✅  File patched and saved.")
else:
    print("ℹ️  No obvious missing except/finally found. Check colon or indentation manually.")

# --- compile to verify -------------------------------------------------
try:
    py_compile.compile(FILE, doraise=True)
    print("✅  Syntax OK – restarting sprint.")
    if FILE in sys.modules:
        importlib.reload(sys.modules[FILE])
    else:
        importlib.import_module(FILE.replace(".py",""))
    from profit_sprint import start_profit_sprint
    start_profit_sprint()
except Exception as e:
    print("❌  Still syntax error:", e)

print("### End ###")
