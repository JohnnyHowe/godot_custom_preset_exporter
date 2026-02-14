import copy

from typing import Optional
from pathlib import Path

from .export_preset_utilities import *
from . import cfg_parser


OPTIONS_KEY = "options"


class ExportPresetAccessor:
    file_path: Path
    _presets: dict
    _reader: cfg_parser.Reader

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.reload()

    def reload(self):
        self._reader = cfg_parser.Reader(self.file_path)
        self._presets = {}

        self._presets = {data["name"]: data for header, data in self._reader.blocks.items() if not "options" in header}

        # Add "options" to presets
        options_by_index = {get_index_from_header(header): data for header, data in self._reader.blocks.items() if "options" in header}
        for data in self._presets.values():
            index = get_index_from_header(data[cfg_parser.HEADER_KEY])
            data[OPTIONS_KEY] = options_by_index[index]

    def get_preset_names(self) -> list[str]:
        return list(self._presets.keys())

    def get_preset(self, name: str) -> dict:
        """ Returns a REFERENCE to the preset"""
        return self._presets[name]

    def get_preset_copy(self, name: str) -> dict:
        return copy.deepcopy(self.get_preset(name))

    def set_preset(self, data: dict):
        name = data["name"]
        if name in self._presets:
            self._presets.pop(name)
        self._ensure_index_valid_and_unique(data)
        self._presets[name] = data

    def save(self) -> None:
        blocks = {}
        for preset in self._presets.values():
            self._add_presets_as_blocks(preset, blocks)
        self._save_cgf_blocks(blocks)

    @staticmethod
    def _add_presets_as_blocks(preset_data: dict, blocks: dict):
        """
        Append a preset and its options block to a CFG blocks dictionary.

        Args:
            preset_data: Preset dictionary containing a header and an OPTIONS_KEY entry.
            blocks: Target block map that will be populated with preset and options blocks.
        """
        preset_data_copy = preset_data.copy()
        options = preset_data_copy.pop(OPTIONS_KEY)

        blocks[preset_data[cfg_parser.HEADER_KEY]] = preset_data_copy
        blocks[options[cfg_parser.HEADER_KEY]] = options

    def _save_cgf_blocks(self, blocks: dict):
        cfg_parser.Saver(blocks).save_as_cfg(self.file_path)

    @staticmethod
    def from_project(project_root: Path):
        return ExportPresetAccessor(project_root / "export_presets.cfg")

    # =============================================================================================
    # region Index Logic
    # =============================================================================================

    def _get_index_from_preset(self, name: str) -> int:
        """
        Gets the index from the preset header.<br>
        For example `[preset.2] -> 2`.
        """
        return get_index_from_header(self.get_preset(name)[cfg_parser.HEADER_KEY])

    def _ensure_index_valid_and_unique(self, data: str):
        """
        Ensures index:
        * Greater or equal to 0.
        * Not the same as any other preset.
        """
        current_index = get_index_from_header(data[cfg_parser.HEADER_KEY])
        names_by_index = self._get_names_by_index()

        if current_index < 0 or len(names_by_index) <= current_index or names_by_index[current_index] != None:
            new_index = [names_by_index, None].index(None)
            data[cfg_parser.HEADER_KEY] = set_header_index(data[cfg_parser.HEADER_KEY], new_index)
            data[OPTIONS_KEY][cfg_parser.HEADER_KEY] = set_header_index(data[OPTIONS_KEY][cfg_parser.HEADER_KEY], new_index)

    def _is_index_in_use(self, index: int) -> bool:
        pass

    def _is_index_valid(self, name: str) -> bool:
        """
        Valid if
        * is integer >= 0
        * no other presets have the same index
        """
        header = self.get_preset(name)[cfg_parser.HEADER_KEY]
        index = get_index_from_header(header)

        if index < 0:
            return False

        # does any other have the same index?
        names_by_index = self._get_names_by_index([name])
        current_name_at_index = names_by_index[index]
        if current_name_at_index != name:
            return False

        return True

    def _give_first_unique_index(self, name: str):
        preset = self.get_preset(name)
        header = preset[cfg_parser.HEADER_KEY]
        set_header_index(header, self._get_first_free_index())

    def _get_first_free_index(self) -> int:
        names_by_index = self._get_names_by_index()
        for index, name in enumerate(names_by_index):
            if name == None:
                return index
        return len(names_by_index)

    def _get_names_by_index(self, names_to_exclude: list[str] = []) -> list[Optional[str]]:
        names_lists = []
        for name, data in self._presets.items():
            if name in names_to_exclude:
                continue
            index = get_index_from_header(data[cfg_parser.HEADER_KEY])
            # ensure long enough
            while len(names_lists) <= index:
                names_lists.append([])
            # add
            names_lists[index].append(name)

        # filter
        names = []
        for name_list in names_lists:
            if len(name_list) == 0:
                names.append(None)
            elif len(name_list) == 1:
                names.append(name_list[0])
            else:
                names.append(name_list)
        return names
