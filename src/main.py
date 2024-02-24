import sys
from .args import add_arg,help_command,clear_arg,ls_arg,rm_arg,get_arg
from .constants import SCRIPT_VERSION,ERROR_ID_UNKNOWN_COMMAND

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