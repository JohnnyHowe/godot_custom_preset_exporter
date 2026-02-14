import os
import shlex
import subprocess
from pathlib import Path
from typing import Optional


ENCRYPTION_KEY_KEY = "SCRIPT_AES256_ENCRYPTION_KEY"


def export_preset(
        project_root: Path,
        preset_name: str,
        export_path: Path,
        debug: bool,
        encryption_key: Optional[str] = None
):
    """
    Wraps `godot --headless --export...`.
    See https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html
    """

    command = [
        "godot", "--headless",
        "--path", _sanitise_path(project_root),
        "--export-debug" if debug else "--export-release", preset_name, _sanitise_path(
            export_path)
    ]

    shlex.join(command)

    env = os.environ.copy()
    if encryption_key != None:
        print("ADDING KEY TO ENV")
        env[ENCRYPTION_KEY_KEY] = encryption_key
    else:
        print("ENSURING KEY NOT IN ENV")
        env.pop(ENCRYPTION_KEY_KEY)		# Ensure it's not there

    subprocess.run(command, env=env)


def _sanitise_path(path: Path) -> str:
    return str(path.resolve()).replace("\\\\", "/").replace("\\", "/")
