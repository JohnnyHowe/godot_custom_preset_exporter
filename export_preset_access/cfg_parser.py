import json
from pathlib import Path


CUSTOM_KEY_PREFIX = "_"
HEADER_KEY = CUSTOM_KEY_PREFIX + "block_header"
VALUE_PARSE_FAILED_KEY = CUSTOM_KEY_PREFIX + "could_not_parse"


class Reader:
	_file_lines: list[str]
	_stripped_lines: list[str]
	blocks: dict

	def __init__(self, file: Path):
		self.file_path = file
		self.reload()

	def reload(self):
		self._load_file_contents()
		self._load_sections()

	def _load_file_contents(self):
		with open(self.file_path, "r") as file:
			self._file_lines = file.readlines()
			self._stripped_lines = Reader.strip_lines_and_remove_empty(self._file_lines)

	def _load_sections(self):
		self.blocks = {}
		current_block = []
		for line in self._stripped_lines:
			if Reader.is_block_header(line):
				self._add_block_if_valid(current_block)
				current_block = []
			current_block.append(line)
		self._add_block_if_valid(current_block)

	def _add_block_if_valid(self, block: list[str]) -> None:
		if len(block) == 0:
			return
		header = block[0]
		self.blocks[header] = Reader._block_to_dict(block)

	@staticmethod
	def _block_to_dict(lines: list[str]):
		data = {VALUE_PARSE_FAILED_KEY: []}
		for line in Reader.strip_lines_and_remove_empty(lines):
			Reader._parse_block_line(line, data)
		return data

	def _parse_block_line(line: str, data: dict) -> None:
		if Reader.is_block_header(line):
			data[HEADER_KEY] = line
			return

		key, value = line.split("=", 1)
		try:
			data[key] = json.loads(value)
		except:
			data[key] = value
			data[VALUE_PARSE_FAILED_KEY].append(key)

	@staticmethod
	def is_block_header(line: str) -> bool:
		return line.startswith("[") and line.endswith("]")

	@staticmethod
	def strip_lines_and_remove_empty(lines: list[str]) -> list[str]:
		return [line.strip() for line in lines if line.strip()]


class Saver:
	blocks: dict

	def __init__(self, blocks: dict):
		self.blocks = blocks

	def save_as_json(self, file_path: Path) -> None:
		with open(file_path, "w") as file:
			file.write(json.dumps(self.blocks, indent="\t"))
			
	def save_as_cfg(self, file_path: Path) -> None:
		with open(file_path, "w") as file:
			file.write(self._get_as_cfg_str())

	def _get_as_cfg_str(self) -> str:
		lines = []
		for block_data in self.blocks.values():
			lines.append(f"{Saver._get_block_data_as_cgf_str(block_data)}\n")

		return "\n".join(lines)

	@staticmethod
	def _get_block_data_as_cgf_str(block_data: dict) -> str:
		lines = [block_data[HEADER_KEY], ""]
		for key, value in block_data.items():
			if key.startswith(CUSTOM_KEY_PREFIX):
				continue

			value_str = value
			if not key in block_data.get(VALUE_PARSE_FAILED_KEY, []):
				try:
					value_str = json.dumps(value) 
				except:
					value_str = f"\"{value}\"" 

			lines.append(f"{key}={value_str}")

		return "\n".join(lines)