from pathlib import Path
from typing import Optional

from .godot_export_preset_access import ExportPresetAccessor
from .export_custom_preset import export_custom_preset


MODIFIED_PRESET_SUFFIX = " (copy from jons export script)"


def export_modified_preset(
	project_root: Path,
	export_preset_name: str,
	export_preset_data_overrides: dict,
	export_path: Path,
	debug: bool = False,
	encryption_key: Optional[str] = None
):
	"""
	Export the project using a modified export preset derived from preset data.
	1. Copy original.
	2. Modify copy with export_preset_data.
	3. Save copy.
	4. Export.

	Automatically sets the new preset name to "<original-name> (copy from jons export script)".

	Args:
		project_root: Root directory of the Godot project.
		export_preset_name: Export preset to modify.
		export_preset_data: Export preset data used to construct the modified preset.
		export_path: Output path for the exported build.
		debug: Whether to produce a debug export instead of a release export.
		encryption_key: Optional encryption key to use for the export.
	"""
	preset_accessor = ExportPresetAccessor.from_project(project_root)
	preset_data = preset_accessor.get_preset_copy(export_preset_name)

	_overwrite_dict_values(preset_data, export_preset_data_overrides)
	preset_data["name"] = export_preset_name + MODIFIED_PRESET_SUFFIX
	preset_accessor.save()

	export_custom_preset(
		project_root,
		preset_data,
		export_path,
		debug,
		encryption_key
	)


def _overwrite_dict_values(to_modify: dict, source_of_truth: dict) -> None:
	for key, value in source_of_truth.items():
		if isinstance(value, dict):
			_overwrite_dict_values(to_modify[key], source_of_truth[key])
		else:
			to_modify[key] = value

