#!/usr/bin/env python

import sys
import json
from pathlib import Path

SCRIPT_VERSION = '1.0.0'

ERROR_ID_INVALID_INDEX = 1001
ERROR_ID_INVALID_KEY = 1002
ERROR_ID_INVALID_ARGUMENTS = 1003
ERROR_ID_UNKNOWN_COMMAND = 1004
ERROR_ID_INVALID_OPTION = 1005

storage_file = Path.home() / '.clip_storage.json'


def load_storage() -> dict:
    try:
        if storage_file.exists():
            with open(storage_file, 'r') as file:
                return json.load(file)
    except PermissionError:
        sys.stderr.write("Error: Permission denied while trying to read the storage file.\n")
        sys.exit(1)
    except json.JSONDecodeError:
        sys.stderr.write("Error: The storage file is not in valid JSON format.\n")
        sys.exit(1)
    return {"indexed_storage": [], "key_storage": {}}


def save_storage(data: dict) -> None:
    try:
        with open(storage_file, 'w') as file:
            json.dump(data, file, indent=4)
    except PermissionError:
        sys.stderr.write("Error: Permission denied while trying to write to the storage file.\n")
        sys.exit(1)
    except InterruptedError:
        sys.stderr.write("Error: The file operation was interrupted.\n")
        sys.exit(1)
    except OSError as e:
        if e.errno == 28:  # Disk full
            sys.stderr.write("Error: No space left on device to write to the storage file.\n")
        else:
            sys.stderr.write(f"Error: An OS error occurred: {e}\n")
        sys.exit(1)

def list_entries(all_values: bool = False, indexed: bool = True) -> None:
    storage = load_storage()
    if all_values:
        json.dump(storage,sys.stdout,indent=4)
    elif indexed:
        json.dump(storage["indexed_storage"],sys.stdout, indent=4)
    else:
        json.dump(storage["key_storage"],sys.stdout, indent=4)
    sys.stdout.write("\n")
def get_index(index, key_based: bool = False) -> None:
    storage = load_storage()
    if not key_based:
        try:
            index = int(index)  # Ensure index is an integer
            sys.stdout.write(storage["indexed_storage"][index])
        except (IndexError, ValueError):
            sys.stderr.write(f"Error ID {ERROR_ID_INVALID_INDEX}: Enter a valid index.\n")
            sys.exit(ERROR_ID_INVALID_INDEX)
        except Exception as e:
            sys.stderr.write(f"Unexpected error: {e}\n")
            sys.exit(0)
    else:
        try:
            sys.stdout.write(storage["key_storage"][index])
        except KeyError:
            sys.stderr.write(f"Error ID {ERROR_ID_INVALID_KEY}: Enter a valid key.\n")
            sys.exit(ERROR_ID_INVALID_KEY)
        except Exception as e:
            sys.stderr.write(f"Unexpected error: {e}\n")
            sys.exit(0)
    sys.stdout.write("\n")
def rm_index(index, key_based: bool = False) -> None:
    storage = load_storage()
    if not key_based:
        try:
            index = int(index)  # Ensure index is an integer
            storage["indexed_storage"].pop(index)
        except (IndexError, ValueError):
            sys.stderr.write(f"Error ID {ERROR_ID_INVALID_INDEX}: Enter a valid index.\n")
            sys.exit(ERROR_ID_INVALID_INDEX)
    else:
        if index not in storage["key_storage"]:
            sys.stderr.write(f"Error ID {ERROR_ID_INVALID_KEY}: Enter a valid key.\n")
            sys.exit(ERROR_ID_INVALID_KEY)
        storage["key_storage"].pop(index)
    save_storage(storage)


def add_entry(value: str, key: str = None) -> None:
    data = load_storage()
    if key is None:
        data["indexed_storage"].append(value)
    else:
        data["key_storage"][key] = value
    save_storage(data)


def validate_args_for_add(args: list):
    if len(args) < 1 or (args[0] in ("-k", "--key") and len(args) < 3):
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments.\n")
        return False
    return True


def add_arg(args: list, n: int):
    if not validate_args_for_add(args):
        sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if args[0] not in ("-k", "--key"):
        add_entry(args[0])
    else:
        add_entry(value=args[2], key=args[1])


def validate_option_for_ls(args: list, n: int) -> bool:
    if n > 0 and args[0] not in ("-a", "--all", "-k", "--key"):
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_OPTION}: Invalid option '{args[0]}' for ls.\n")
        return False
    return True


def ls_arg(args: list, n: int):
    if not validate_option_for_ls(args, n):
        sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if n > 0 and args[0] in ("-a", "--all"):
        list_entries(all_values=True)
    elif n > 0 and args[0] in ("-k", "--key"):
        list_entries(indexed=False)
    else:
        list_entries()


def validate_args_for_rm(args: list, n: int) -> bool:
    if n > 0 and args[0] in ("-k", "--key") and len(args) < 2:
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments.\n")
        return False
    return True


def rm_arg(args: list, n: int):
    if not validate_args_for_rm(args, n):
        sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if args[0] in ("-k", "--key"):
        rm_index(index=args[1], key_based=True)
    else:
        rm_index(index=args[0])


def validate_option_for_clear(args: list, n: int) -> bool:
    if n > 0 and args[0] not in ("-k", "--key", "-i", "--index"):
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_OPTION}: Invalid option '{args[0]}' for ls.\n")
        return False
    return True


def clear_arg(args: list, n: int) -> None:
    if not validate_option_for_clear(args, n):
       sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if n == 0:
        data = {"indexed_storage": [], "key_storage": {}}
    elif args[0] in ["-k", "--key"]:
        data = {"indexed_storage": load_storage()["indexed_storage"], "key_storage": {}}
    elif args[0] in ["-i", "--index"]:
        data = {"indexed_storage": [], "key_storage": load_storage()["key_storage"]}
    save_storage(data)


def validate_args_for_get(args: list, n: int) -> bool:
    if n < 1:
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments for get.")
        return False
    if args[0] in ["-k", "--key"] and n < 2:
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Key-based get requires a key.")
        return False
    return True

def get_arg(args: list, n: int):
    if not validate_args_for_get(args, n):
       sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if args[0] in ("-k", "--key"):
        get_index(index=args[1], key_based=True)
    else:
        get_index(index=args[0])

def help_command() -> None:
    help_text = """
Usage: script.py [command] [options]

Commands:
  add    Adds a new entry. Use "-k [key]" to add a keyed entry.
         Example: add "Hello, World" or add -k greeting "Hello, World"
  
  get    Retrieves an entry by index or key.
         Example: get 0 or get -k greeting
  
  ls     Lists entries. Use "-a" to list all, "-k" for key storage.
         Example: ls, ls -a, or ls -k
  
  rm     Removes an entry by index or key.
         Example: rm 0 or rm -k greeting
  
  clear  Clears storage. Use "-k" for key storage, "-i" for indexed storage.
         Example: clear, clear -k, or clear -i
   
  -v, --version  Show script version.
  
  help   Shows this help message.

Options:
  -k, --key         Specifies a key for key-based operations.
  -a, --all         Lists all entries (indexed and key-based).
  -i, --index     Specifies indexed storage for the clear command.
"""
    sys.stdout.write(help_text)


def main():
    sys_args = sys.argv
    if not sys.stdin.isatty():
        pipe_input = sys.stdin.readline().strip("\n").split(" ")
        sys_args.extend(pipe_input)
    if len(sys_args) == 2 and sys_args[1] in ("-v","--version"):
        sys.stdout.write(f"clip version: {SCRIPT_VERSION}\n")
        return
    if len(sys_args) < 2 or sys_args[1] in ("help", "--help", "-h"):
        help_command()
        return
    command = sys_args[1]
    args = sys_args[2:]
    n = len(args)

    command_map = {
        "add": add_arg,
        "get": get_arg,
        "clear": clear_arg,
        "ls": ls_arg,
        "rm": rm_arg
    }

    if command in command_map:
        command_map[command](args, n)
    else:
        sys.stderr.write(f"Error ID {ERROR_ID_UNKNOWN_COMMAND}: Unknown command '{command}'.\n")
        help_command()
        sys.exit(ERROR_ID_UNKNOWN_COMMAND)

if __name__ == "__main__":
    main()
