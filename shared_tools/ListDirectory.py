import os
from typing import Optional

from agency_swarm.tools import BaseTool
from pydantic import Field


class ListDirectory(BaseTool):
    """
    Lists files and directories at a given path.
    Use this to find what files exist in a client outputs folder, assets folder,
    or any other directory before reading or copying files.
    """

    directory_path: str = Field(
        ...,
        description="The absolute path to the directory to list",
    )
    recursive: Optional[bool] = Field(
        False,
        description="If True, list files recursively up to 3 levels deep.",
    )

    def run(self):
        try:
            if not os.path.isabs(self.directory_path):
                return f"Error: directory_path must be an absolute path. Got: {self.directory_path}"
            if not os.path.exists(self.directory_path):
                return f"Error: Directory does not exist: {self.directory_path}"
            if not os.path.isdir(self.directory_path):
                return f"Error: Path is not a directory: {self.directory_path}"

            ignore = {"__pycache__", ".git", ".venv", "venv", "node_modules", ".pytest_cache"}

            def list_tree(path, prefix="", depth=0):
                if depth > 3:
                    return ""
                result = []
                try:
                    entries = sorted(os.listdir(path))
                except PermissionError:
                    return f"{prefix}[Permission Denied]\n"
                entries = [e for e in entries if not e.startswith(".") and e not in ignore]
                for i, entry in enumerate(entries):
                    entry_path = os.path.join(path, entry)
                    connector = "└── " if i == len(entries) - 1 else "├── "
                    new_prefix = prefix + ("    " if i == len(entries) - 1 else "│   ")
                    if os.path.isdir(entry_path):
                        result.append(f"{prefix}{connector}{entry}/\n")
                        if self.recursive and depth < 3:
                            result.append(list_tree(entry_path, new_prefix, depth + 1))
                    else:
                        result.append(f"{prefix}{connector}{entry}\n")
                return "".join(result)

            output = f"{self.directory_path}/\n" + list_tree(self.directory_path)
            return output.rstrip() if output.strip() else f"Directory is empty: {self.directory_path}"

        except Exception as e:
            return f"Error listing directory: {str(e)}"
