"""Build or verify the complete downloadable repository package."""
from pathlib import Path
import argparse
import zipfile

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'Oakheart_Claude_Skills.zip'

def members():
    ignored={'.git','__pycache__','.dist-build','.dist-previous','eval-results'}
    return {('oakheart-skills/'+p.relative_to(ROOT).as_posix()): p.read_bytes()
            for p in sorted(ROOT.rglob('*')) if p.is_file() and p != OUT
            and not ignored.intersection(p.relative_to(ROOT).parts)
            and p.suffix not in {'.pyc','.bundle'}}

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
expected=members()
if args.check:
    with zipfile.ZipFile(OUT) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == set(expected), 'Download inventory differs; run bundle.py'
        assert all(z.read(n)==b for n,b in expected.items()), 'Download is stale; run bundle.py'
    print('Complete download verified')
else:
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in expected.items():
            info=zipfile.ZipInfo(name,(2026,9,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data)
    print(f'Built {OUT.name} ({OUT.stat().st_size} bytes)')
