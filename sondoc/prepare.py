import os
from pathlib import Path

from PIL import Image

from .transform import html_crossref

target_width = 1024 + 256

want_webp = True


def mkdir(path: Path):
    directory = path.parent
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def rebase(old: Path, new: Path, path: Path) -> Path:
    suffix = Path(str(path)[len(str(old)) :].strip("/"))
    return Path(new, suffix)


def resize(input: Path, output: Path, suffix: str) -> None:
    mkdir(output)
    img = Image.open(input)
    size = img.size
    width = size[0]
    factor = target_width / width
    new_size = tuple([int(x * factor) for x in size])
    img = img.resize(new_size, Image.LANCZOS)
    if want_webp:
        out = output.with_suffix(".webp")
        img.save(out, method=6, quality=85)
    else:
        out = output.with_suffix(".jpg")
        img.save(out, optimize=True, quality=85)
    print(f"Resized: {suffix}")


def transform(input: Path, output: Path, suffix: str) -> None:
    directory = mkdir(output)
    with input.open("r", encoding="UTF-8") as i:
        result = html_crossref(i.read(), directory)
    with output.open("w", encoding="UTF-8") as o:
        o.write(result)
    print(f"Transformed: {suffix}")


def build(command, input: Path, output: Path, match):
    _build(command, input, output, match, len(str(output)))


def _build(command, input: Path, output: Path, match, outlen: int):
    for entry in input.iterdir():
        if entry.is_dir():
            new_path = Path(output, entry.name)
            if entry.is_symlink():
                if not new_path.is_symlink():
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                    new_path.symlink_to(os.readlink(entry), target_is_directory=True)
            else:
                _build(command, entry, new_path, match, outlen)
        if not entry.match(match):
            continue
        result = rebase(input, output, entry)
        suffix = Path(str(result)[outlen:].strip("/"))
        if result.exists():
            entry_stat = entry.stat()
            result_stat = result.stat()
            if entry_stat.st_mtime > result_stat.st_mtime:
                command(entry, result, suffix)
        else:
            command(entry, result, suffix)


def prepare(input: Path, output: Path):
    build(resize, input, output, "*.jpg")
    build(resize, input, output, "*.png")
    build(transform, input, output, "*.md")
