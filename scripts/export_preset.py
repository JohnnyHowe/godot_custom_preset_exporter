import os
import shlex
import subprocess
from pathlib import Path
from typing import Optional


ENCRYPTION_KEY_ENV_NAME = "SCRIPT_AES256_ENCRYPTION_KEY"


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

	if not export_path.parent.exists():
		print(f"Export path does not exist. Creating it at {str(export_path)}")
		export_path.parent.mkdir(parents=True, exist_ok=True)

	command = [
		"godot", "--headless",
		"--path", _sanitise_path(project_root),
		"--export-debug" if debug else "--export-release",
		preset_name,
		_sanitise_path(export_path)
	]

	print("> " + shlex.join(command))
	subprocess.run(command, env=_get_env_copy_with_key_set(encryption_key))


def _get_env_copy_with_key_set(encryption_key: Optional[str]) -> os._Environ[str]:
	"""
	Sets SCRIPT_AES256_ENCRYPTION_KEY in env.
	If encryption_key is None, no entry for it will exist in env.
	"""
	env_copy = os.environ.copy()
	if encryption_key != None:
		env_copy[ENCRYPTION_KEY_ENV_NAME] = encryption_key
	elif ENCRYPTION_KEY_ENV_NAME in env_copy:
		env_copy.pop(ENCRYPTION_KEY_ENV_NAME)
	return env_copy


def _sanitise_path(path: Path) -> str:
	return str(path.resolve()).replace("\\\\", "/").replace("\\", "/")
