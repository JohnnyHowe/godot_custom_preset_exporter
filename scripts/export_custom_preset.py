"""
Exports a project with a custom preset.
"""
from pathlib import Path
from typing import Optional
from .export_preset_access import ExportPresetAccessor
from .export_preset import export_preset


def export_custom_preset(
	project_root: Path,
	export_preset_data: dict,
	export_path: Path,
	debug: bool = False,
	encryption_key: Optional[str] = None
):
	"""
	1. Insert preset into project.
	2. Run export_project.export with that preset.

	Args:
		project_root: Root directory of the Godot project.
		export_preset_data: Export preset data used to construct the modified preset.
		export_path: Output path for the exported build.
		debug: Whether to produce a debug export.
		encryption_key: Optional encryption key to use for the export.
	"""
	preset_accessor = ExportPresetAccessor.from_project(project_root)
	preset_accessor.set_preset(export_preset_data)
	preset_accessor.save()

	export_preset(
		project_root,
		export_preset_data["name"],
		export_path,
		debug,
		encryption_key
	)
