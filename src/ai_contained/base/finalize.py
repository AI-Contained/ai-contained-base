"""Finalize script — installs all providers at image build time."""

import glob
import os
import pathlib
import shutil
import subprocess

UV = shutil.which("uv")
if not UV:
    raise RuntimeError("uv not found in PATH")


def main() -> None:
    """Symlink provider binaries and install all provider packages."""
    for b in glob.glob("/opt/ai-contained-*/bin/*"):
        p = pathlib.Path(b)
        dest = pathlib.Path(f"/usr/local/bin/{p.name}")
        if p.is_file() and not dest.exists():
            os.symlink(b, dest)

    for provider in sorted(glob.glob("/opt/ai-contained-*/")):
        subprocess.run(
            [UV, "pip", "install", "--system", "--python", "/usr/local/bin/python3", "--break-system-packages", provider],
            check=True,
        )
