from pathlib import Path
import runpy
import os
import sys


project_root = Path(__file__).resolve().parent
venv_python = project_root / ".venv" / "bin" / "python"

if venv_python.exists() and Path(sys.executable).resolve() != venv_python.resolve():
	os.execv(str(venv_python), [str(venv_python), str(Path(__file__).resolve())])

script_path = project_root / "day1" / "hello.py"
runpy.run_path(str(script_path), run_name="__main__")