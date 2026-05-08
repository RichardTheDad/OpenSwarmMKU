import os

from agency_swarm.tools import BaseTool
from pydantic import Field


class WriteFile(BaseTool):
    """
    Writes content to a file on the local filesystem.
    Use this to save marketing content, research briefs, QA reports, and other
    deliverables to the clients/[client-name]/outputs/ folder.

    - Overwrites existing files
    - Creates directories automatically
    - file_path must be an absolute path
    """

    file_path: str = Field(
        ...,
        description="Absolute path to the file to write.",
    )
    content: str = Field(..., description="The content to write to the file")

    def run(self):
        try:
            if not os.path.isabs(self.file_path):
                return f"Error: File path must be absolute: {self.file_path}"

            file_exists = os.path.exists(self.file_path)

            if file_exists:
                if not os.path.isfile(self.file_path):
                    return f"Error: Path exists but is not a file: {self.file_path}"
                operation = "overwritten"
            else:
                directory = os.path.dirname(self.file_path)
                if directory and not os.path.exists(directory):
                    try:
                        os.makedirs(directory, exist_ok=True)
                    except Exception as e:
                        return f"Error creating directory {directory}: {str(e)}"
                operation = "created"

            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.content)

                file_size = os.path.getsize(self.file_path)
                line_count = self.content.count("\n") + (
                    1 if self.content and not self.content.endswith("\n") else 0
                )
                return f"Successfully {operation} file: {self.file_path}\nSize: {file_size} bytes, Lines: {line_count}"

            except PermissionError:
                return f"Error: Permission denied writing to file: {self.file_path}"
            except Exception as e:
                return f"Error writing file: {str(e)}"

        except Exception as e:
            return f"Error during write operation: {str(e)}"
