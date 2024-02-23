#!/usr/bin/env python

import sys
import json
from pathlib import Path

# Define error IDs
ERROR_ID_INVALID_INDEX = 1001
ERROR_ID_INVALID_KEY = 1002
ERROR_ID_INVALID_ARGUMENTS = 1003
ERROR_ID_UNKNOWN_COMMAND = 1004
ERROR_ID_INVALID_OPTION = 1005

storage_file = Path.home() / '.clip_storage.json'


def load_storage() -> dict:
    if storage_file.exists():
        with open(storage_file, 'r') as file:
            return json.load(file)
    return {"indexed_storage": [], "key_storage": {}}


def save_storage(data: dict) -> None:
    with open(storage_file, 'w') as file:
        json.dump(data, file, indent=4)


def list_entries(all_values: bool = False, indexed: bool = True) -> None:
    storage = load_storage()
    if all_values:
        print(json.dumps(storage, indent=4))
    elif indexed:
        print(json.dumps(storage["indexed_storage"], indent=4))
    else:
        print(json.dumps(storage["key_storage"], indent=4))


def get_index(index, key_based: bool = False) -> None:
    storage = load_storage()
    if not key_based:
        try:
            index = int(index)  # Ensure index is an integer
            print(storage["indexed_storage"][index])
        except (IndexError, ValueError):
            print(f"Error ID {ERROR_ID_INVALID_INDEX}: Enter a valid index.")
            sys.exit(ERROR_ID_INVALID_INDEX)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(0)
    else:
        try:
            print(storage["key_storage"][index])
        except KeyError:
            print(f"Error ID {ERROR_ID_INVALID_KEY}: Enter a valid key.")
            sys.exit(ERROR_ID_INVALID_KEY)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(0)

def rm_index(index, key_based: bool = False) -> None:
    storage = load_storage()
    if not key_based:
        try:
            index = int(index)  # Ensure index is an integer
            storage["indexed_storage"].pop(index)
        except (IndexError, ValueError):
            print(f"Error ID {ERROR_ID_INVALID_INDEX}: Enter a valid index.")
            sys.exit(ERROR_ID_INVALID_INDEX)
    else:
        if index not in storage["key_storage"]:
            print(f"Error ID {ERROR_ID_INVALID_KEY}: Enter a valid key.")
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
        print(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments.")
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
        print(f"Error ID {ERROR_ID_INVALID_OPTION}: Invalid option '{args[0]}' for ls.")
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
        print(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Key-based removal requires a key.")
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
        print(f"Error ID {ERROR_ID_INVALID_OPTION}: Invalid option '{args[0]}' for clear.")
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
        print(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments for get.")
        return False
    if args[0] in ["-k", "--key"] and n < 2:
        print(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Key-based get requires a key.")
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
  
  help   Shows this help message.

Options:
  -k, --key         Specifies a key for key-based operations.
  -a, --all         Lists all entries (indexed and key-based).
  -i, --index     Specifies indexed storage for the clear command.
"""
    print(help_text)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("help", "--help", "-h"):
        help_command()
        return

    command = sys.argv[1]
    args = sys.argv[2:]
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
        print(f"Error ID {ERROR_ID_UNKNOWN_COMMAND}: Unknown command '{command}'.")
        help_command()
        sys.exit(ERROR_ID_UNKNOWN_COMMAND)

if __name__ == "__main__":
    main()
