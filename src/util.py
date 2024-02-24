import json
import sys
from .constants import storage_file,ERROR_ID_INVALID_INDEX,ERROR_ID_INVALID_KEY


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