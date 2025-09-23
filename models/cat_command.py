from langchain.tools import BaseTool


class CatCommand(BaseTool):
    name: str = "cat"
    description: str = "像Linux命令cat，用來讀取特定檔案內容的功具"
    # description: str = "Read file contents like the cat command in Linux."

    def _run(self, file_path: str) -> str:
        """Read file contents."""
        try:
            with open(file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"File not found: {file_path}"
        except Exception as e:
            return f"An error occurred: {e}"

    async def _arun(self, file_path: str) -> str:
        """Read file contents asynchronously (not implemented)."""
        raise NotImplementedError("Async cat is not supported yet.")


