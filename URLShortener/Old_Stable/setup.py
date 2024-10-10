import sys
from cx_Freeze import setup, Executable

# Dependências adicionais podem ser adicionadas aqui
build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="URLShortener",
    version="1.7",
    description="URL Shortener App",
    options={"build_exe": build_exe_options},
    executables=[Executable("url_shortner.py", base=base, icon="internet.ico")],
)
