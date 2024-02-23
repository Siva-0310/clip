# Clip

This is a simple command-line utility for managing a clipboard storage system. It allows users to add, retrieve, list, remove, and clear text entries stored in a JSON file. This utility supports both indexed and key-value storage, making it versatile for various use cases.

## Features

- **Add Entries:** Add text entries with or without a key.
- **Get Entries:** Retrieve entries by their index or key.
- **List Entries:** Display all entries, or filter by indexed or key-based entries.
- **Remove Entries:** Delete entries by their index or key.
- **Clear Storage:** Completely clear the storage or selectively by indexed or key-based entries.

### Commands and Options

#### Add

Add a new entry to the storage. Entries can be added to indexed storage or associated with a specific key.

- **Syntax**: `add [-k key] value`
- **Options**:
  - `-k`, `--key`: Specify a key for the entry (for key-value storage).
- **Examples**:
  - Add to indexed storage: `clip add "Sample text"`
  - Add to key-value storage: `clip add -k sample "Sample text"`

#### Get

Retrieve and display an entry from the storage.

- **Syntax**: `get [-k key] index`
- **Options**:
  - `-k`, `--key`: Specify that the retrieval should use a key (for key-value storage).
- **Examples**:
  - Get from indexed storage: `clip get 0`
  - Get from key-value storage: `clip get -k sample`

#### List (ls)

List entries stored in the clipboard.

- **Syntax**: `ls [-a | -k]`
- **Options**:
  - `-a`, `--all`: List all entries (both indexed and key-value).
  - `-k`, `--key`: List only key-value entries.
- **Examples**:
  - List indexed entries: `clip ls`
  - List all entries: `clip ls -a`
  - List key-value entries: `clip ls -k`

#### Remove (rm)

Remove an entry from the storage.

- **Syntax**: `rm [-k key] index`
- **Options**:
  - `-k`, `--key`: Specify that the removal should use a key (for key-value storage).
- **Examples**:
  - Remove from indexed storage: `clip rm 0`
  - Remove from key-value storage: `clip rm -k sample`

#### Clear

Clear all entries from the storage or selectively clear indexed or key-value storage.

- **Syntax**: `clear [-i | -k]`
- **Options**:
  - `-i`, `--index`: Clear only the indexed storage.
  - `-k`, `--key`: Clear only the key-value storage.
- **Examples**:
  - Clear all storage: `clip clear`
  - Clear indexed storage: `clip clear -i`
  - Clear key-value storage: `clip clear -k`

#### Help

Display help information about all commands and options.

- **Syntax**: `help`
- **Example**: `clip help`