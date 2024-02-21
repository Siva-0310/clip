#!/usr/bin/env python
import sys
import json
from pathlib import Path
storage_file = Path.home() / '.clip_storage.json'
def load_storage():
    if storage_file.exists():
        with open(storage_file,'r') as file:
            return json.load(file)
    return {"indexed_storage": [], "key_storage": {}}
def save_storage(data:dict) -> None:
    with open(storage_file,'w') as file:
        json.dump(data,file,indent=4)
def list_entries(all_values:bool = False,indexed:bool = True) -> None:
    if all_values:
        print(json.dumps(load_storage(),indent=4))
    elif indexed:
        print(json.dumps(load_storage()["indexed_storage"],indent=4))
    else:
        print(json.dumps(load_storage()["key_storage"],indent=4))
def clear() -> None:
    data = {"indexed_storage": [], "key_storage": {}}
    save_storage(data)
def get(index:int = -1,key_based:bool = False) -> None:
    stor = load_storage()
    if not key_based:
        if len(stor["indexed_storage"]) < index or index == -1:
            print(stor["indexed_storage"][index])
    elif stor["key_storage"].get(index,-1) != -1:
        print(stor["key_storage"][index])
def add_entry(value:str,key:str=None) -> None:
    if value is None:
        if not sys.stdin.isatty():
            value = sys.stdin.read().rstrip("\n")
        else:
            print("Error: No value provided for adding.")
            return
    data = load_storage()
    print(data)
    if key is None:
        data["indexed_storage"].append(value)
    else:
        data["key_storage"][key] = value
    save_storage(data)
def main():
    args = sys.argv[1:]
    print(args)
    command = args[0]
    if command == 'add':
        if len(args) >= 2:
            if (args[1] == "-k" or args[1] == "--key"):
                if len(args) < 4:
                    print("Error: No value provided for adding.")
                    return
                key = args[2]
                value = args[3]
                add_entry(value,key)
                return
            value = args[1]
            add_entry(value)
        else:
            print("Error: No valid options provided.")
    if command == "ls":
        if len(args) >= 2:
            if args[1] == "-a" or args[1] == "--all":
                list_entries(all_values=True)
            elif args[1] == "-k" or args[1] == "--key_storage":
                list_entries(indexed=False)
            else:
                print("Error: No valid options provided.")
        else:
            list_entries()
    if command == "clear":
        clear()
    if command == 'get':
        if len(args) >= 2:
            if args[1] == "-k" or args[1] == "--key":
                if len(args) >= 3:
                    get(index=args[2],key_based=True)
                else:
                    print("Error: No key provided for retrieving.")
            else:
                try:
                    index = int(args[1])
                    get(index=index)
                except:
                    print("Error: No valid index provided for retrieving.")
        else:
            get()
 
main()