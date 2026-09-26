"""Run deterministic packaging, drift and helper checks; no model or network calls."""
import os
from pathlib import Path
import subprocess
import sys
from sync import inventory, verify_release

ROOT = Path(__file__).resolve().parent
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def run(*args, cwd=ROOT):
    subprocess.run([sys.executable, *args], cwd=cwd, env=os.environ, check=True)

verify_release()
before = inventory(ROOT/'dist')
run('build.py')
assert inventory(ROOT/'dist') == before, 'Build is not reproducible'
run('validate.py')
for name in ['learning-loop', 'software-delivery-agency']:
    run('-m', 'unittest', 'discover', '-p', 'test_*.py', cwd=ROOT/'dist/codex/skills'/name/'scripts')
run('-m', 'unittest', 'discover', '-s', 'tests')
print('Package checks passed. Native activation and behavioral quality require separate evidence.')
