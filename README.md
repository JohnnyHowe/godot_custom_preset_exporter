# Godot Export Preset Modifier

Python helpers to export Godot projects via the CLI, including exporting with modified or custom presets. Preset reading/editing is handled by the `godot_export_preset_access` submodule.

## Features
- Run headless Godot exports with a named preset.
- Export using a modified copy of an existing preset.
- Export using a custom preset definition you provide.

## Requirements
- Python 3.x (version not pinned).
- Godot installed and available on `PATH` as `godot`.
- The `godot_export_preset_access` submodule initialized (see `.gitmodules`).

## Usage
### Export Using an Existing Preset
```python
from godot_custom_preset_exporter import export_preset

export_preset(
    project_root=r"C:\Projects\MyGame",
    preset_name="Windows Desktop",
    export_path=r"C:\Exports\MyGame.exe",
    debug=False,
)
```

### Export Using a Modified Preset
```python
from godot_custom_preset_exporter import export_modified_preset

export_modified_preset(
    project_root=r"C:\Projects\MyGame",
    export_preset_name="Windows Desktop",
    export_preset_data_overrides={
        "options": {
            "binary_format/embed_pck": True
        }
    },
    export_path=r"C:\Exports\MyGame.exe",
    debug=False,
)
```

### Export Using a Custom Preset
```python
from godot_custom_preset_exporter import export_custom_preset

export_custom_preset(
    project_root=r"C:\Projects\MyGame",
    export_preset_data={
        "name": "My Custom Preset",
        "platform": "Windows Desktop",
        "runnable": True,
        "options": {
            "binary_format/embed_pck": True,
        },
    },
    export_path=r"C:\Exports\MyGame.exe",
    debug=False,
)
```

## Notes
- Preset access and editing examples live in the submodule README: `godot_export_preset_access/README.md`.
- `export_presets.cfg` is updated in-place when you save via the accessor.
