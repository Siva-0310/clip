import sys
from .constants import ERROR_ID_INVALID_ARGUMENTS,ERROR_ID_INVALID_OPTION


def validate_args_for_get(args: list, n: int) -> bool:
    if n < 1:
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments for get.")
        return False
    if args[0] in ["-k", "--key"] and n < 2:
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Key-based get requires a key.")
        return False
    return True

def validate_option_for_clear(args: list, n: int) -> bool:
    if n > 0 and args[0] not in ("-k", "--key", "-i", "--index"):
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_OPTION}: Invalid option '{args[0]}' for ls.\n")
        return False
    return True

def validate_args_for_rm(args: list, n: int) -> bool:
    if n > 0 and args[0] in ("-k", "--key") and len(args) < 2:
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments.\n")
        return False
    return True

def validate_option_for_ls(args: list, n: int) -> bool:
    if n > 0 and args[0] not in ("-a", "--all", "-k", "--key"):
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_OPTION}: Invalid option '{args[0]}' for ls.\n")
        return False
    return True

def validate_args_for_add(args: list):
    if len(args) < 1 or (args[0] in ("-k", "--key") and len(args) < 3):
        sys.stderr.write(f"Error ID {ERROR_ID_INVALID_ARGUMENTS}: Enter valid arguments.\n")
        return False
    return True