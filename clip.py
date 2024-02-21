#!/usr/bin/env python


import sys
import json
from pathlib import Path


storage_file = Path.home() / '.clip_storage.json'


def load_storage() -> dict:
    if storage_file.exists():
        with open(storage_file,'r') as file:
            return json.load(file)
    return {"indexed_storage": [], "key_storage": {},"temp_storage":None}


def save_storage(data:dict) -> None:
    with open(storage_file,'w') as file:
        json.dump(data,file,indent=4)


def list_entries(all_values:bool = False,indexed:bool = True) -> None:
    storage = load_storage()
    if all_values:
        print(json.dumps(storage,indent=4))
    elif indexed:
        print(json.dumps(storage["indexed_storage"],indent=4))
    else:
        print(json.dumps(storage["key_storage"],indent=4))


def get_index(index:int = -1,key_based:bool = False) -> None:
    storage = load_storage()
    if not key_based:
        try:
            print(storage["indexed_storage"][index])
        except:
            print("enter valid index")
        return
    else:
        try:
            print(storage["key_storage"][index])
        except:
            print("enter the valid index")
        return
    

def add_entry(value:str,key:str=None) -> None:
    data = load_storage()
    if key is None:
        data["indexed_storage"].append(value)
    else:
        data["key_storage"][key] = value
    save_storage(data)


def add_arg(args:list,n:int):
    if args[0] != "-k" and args[0] != "--key" and n >= 1:
        add_entry(args[0])
        return
    if n < 3:
        print("enter the valid arguments")
        return
    key,val = args[1],args[2]
    add_entry(value=val,key=key)

def ls_arg(args:list,n:int):
    if n != 0 and (args[0] == "-a" or args[0] == "--all"):
        list_entries(all_values=True)
        return
    if n != 0 and (args[0] == "-k" or args[0] == "--key_storage"):
        list_entries(indexed=False)
        return
    list_entries()


def get_arg(args:list,n:int):
    if (args[0] == "-k" or args[0] == "--key") and  n >= 2:
        get_index(index=args[1],key_based=True)
        return
    try:
        index = int(args[0])
    except:
        print("enter the valid index")
        return
    get_index(index=index)


def clear_arg() -> None:
    data = {"indexed_storage": [], "key_storage": {},"temp_storage": None}
    save_storage(data)


def main():
    args = sys.argv[1:]
    n = len(args)-1
    if n != 0 and args[0] == "add":
        add_arg(args[1:],n)
    elif n != 0 and args[0] == "get":
        get_arg(args[1:],n)
    elif args[0] == "clear":
        clear_arg()
    elif n != 0 and args[0] == "ls":
        ls_arg(args[1:],n)
 
if __name__ == "__main__":
    main()