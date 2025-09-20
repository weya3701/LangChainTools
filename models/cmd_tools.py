from langchain.tools import tool
import subprocess
import sys


@tool(description="在終端機下linux或mac作業系統命令的工具")
def run_command(command):

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
