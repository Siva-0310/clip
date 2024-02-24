import sys
from .constants import ERROR_ID_INVALID_ARGUMENTS
from .util import *
from .validation import *

def add_arg(args: list, n: int):
    if not validate_args_for_add(args):
        sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if args[0] not in ("-k", "--key"):
        add_entry(args[0])
    else:
        add_entry(value=args[2], key=args[1])


def ls_arg(args: list, n: int):
    if not validate_option_for_ls(args, n):
        sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if n > 0 and args[0] in ("-a", "--all"):
        list_entries(all_values=True)
    elif n > 0 and args[0] in ("-k", "--key"):
        list_entries(indexed=False)
    else:
        list_entries()


def rm_arg(args: list, n: int):
    if not validate_args_for_rm(args, n):
        sys.exit(ERROR_ID_INVALID_ARGUMENTS)
    if n == 0:
        rm_index(-1)
    elif args[0] in ("-k", "--key"):
        rm_index(index=args[1], key_based=True)
    else:
        rm_index(index=args[0])


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