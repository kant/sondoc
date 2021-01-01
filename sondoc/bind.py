import os
from pathlib import Path
from subprocess import run
from typing import List


def bind(
    input: Path,
    output: Path,
    follow: bool = False,
) -> None:
    md_inputs: List[str] = []
    output_path = output.absolute()
    os.chdir(input)
    for root, _, files in os.walk(".", followlinks=follow):
        for file_ in files:
            if file_.endswith(".md"):
                md_inputs.append(os.path.join(root, file_))

    run(
        [
            "pandoc",
            "-s",
            "--toc",
            "--file-scope",
            "--self-contained",
            "--shift-heading-level-by=-1",
            "-o",
            str(output_path),
        ]
        + sorted(md_inputs),
        check=True,
    )
    print(f"Bound: {output}")
