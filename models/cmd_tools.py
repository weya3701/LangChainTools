from langchain.tools import tool
import subprocess
import sys


@tool(description="在終端機下linux或mac作業系統命令的工具")
def run_command(command: str) -> str:

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)

        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(
            f"Command failed with return code {e.returncode}",
            file=sys.stderr
        )
        print(e.stderr, file=sys.stderr)
    except FileNotFoundError:
        print("Command not found.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

    return result.stdout


@tool(description="像Linux命令cat，用來讀取特定檔案內容的功具，引入參數是檔案路徑")
def cat_command(fpath: str) -> str:

    try:
        with open(fpath, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Fild not found: {fpath}"
    except Exception as e:
        return f"An error occurred: {e}"


@tool(description="像Linux命令sed，用來取代檔案部份符合正規表示式內容")
def sed_command(command: str):
    file_path, pattern, replacement = command.split(' ')
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f'Error: File not found: {file_path}'

    modified_lines = [line.replace(pattern, replacement) for line in lines]

    try:
        with open(file_path, 'w') as f:
            f.writelines(modified_lines)
            rsp = "Successfully replaced {} with {} in {}".format(
                pattern, replacement, file_path
            )
        return rsp
    except Exception as e:
        return f'Error writing to file: {e}'
