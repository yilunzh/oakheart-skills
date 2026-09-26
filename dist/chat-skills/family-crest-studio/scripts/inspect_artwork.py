#!/usr/bin/env python3
"""Read-only helper: report file type basics, dimensions, placed-size PPI, and simple SVG structure cues."""
from pathlib import Path
import argparse, json, hashlib, math
from PIL import Image
import xml.etree.ElementTree as ET

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def positive_size(value):
    size = float(value)
    if not math.isfinite(size) or size <= 0:
        raise argparse.ArgumentTypeError("Physical dimensions must be finite and positive")
    return size

def inspect(path: Path, width_inches=None, height_inches=None):
    for size in (width_inches, height_inches):
        if size is not None and (not math.isfinite(size) or size <= 0):
            raise ValueError("Physical dimensions must be finite and positive")
    result = {"path": str(path), "exists": path.exists(), "sha256": None, "kind": None}
    if not path.exists():
        return result
    result["sha256"] = sha256_of(path)
    suf = path.suffix.lower()
    if suf in {'.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff'}:
        result["kind"] = "raster"
        with Image.open(path) as im:
            result["width_px"], result["height_px"] = im.size
        if width_inches is not None or height_inches is not None:
            # A single physical dimension assumes the original aspect ratio.
            if width_inches is None:
                width_inches = height_inches * result["width_px"] / result["height_px"]
            if height_inches is None:
                height_inches = width_inches * result["height_px"] / result["width_px"]
            result["placed_size_inches"] = {"width": width_inches, "height": height_inches}
            result["placed_ppi"] = {
                "x": result["width_px"] / width_inches,
                "y": result["height_px"] / height_inches,
            }
            result["aspect_ratio_preserved"] = math.isclose(
                result["placed_ppi"]["x"], result["placed_ppi"]["y"], rel_tol=1e-6
            )
    elif suf == '.svg':
        result["kind"] = "svg"
        tree = ET.parse(path)
        root = tree.getroot()
        result["root_tag"] = root.tag
        result["image_elements"] = len(root.findall('.//{http://www.w3.org/2000/svg}image'))
        result["path_elements"] = len(root.findall('.//{http://www.w3.org/2000/svg}path'))
    else:
        result["kind"] = "other"
    return result

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--width-inches', type=positive_size, help='Placed raster width in inches')
    ap.add_argument('--height-inches', type=positive_size, help='Placed raster height in inches; one dimension preserves aspect ratio')
    args = ap.parse_args()
    print(json.dumps(inspect(Path(args.path), args.width_inches, args.height_inches), indent=2, ensure_ascii=False))
