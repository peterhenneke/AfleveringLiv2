import sys
import subprocess

try:
    from pypdf import PdfReader
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    from pypdf import PdfReader

reader = PdfReader("c:/Users/Peter/Desktop/Learning/Liv2/Liv2-2026.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open("c:/Users/Peter/Desktop/Learning/Liv2/Liv2-2026-extracted.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Extraction complete.")
