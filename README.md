# Solution

A simple one-way folder synchronization script written in Python. It periodically updates a replica folder to match a source folder, ensuring that:

1. Files missing in the replica are copied from the source.
2. Files no longer in the source are removed from the replica.
3. Files that have changed (based on MD5 checksums) are updated in the replica.

## Features

- **One-way sync**: The replica folder will match the source folder after each sync cycle.
- **Periodic execution**: The script repeatedly synchronizes at a specified time interval.
- **Logging**: File creation, copying, removal, and errors are logged to a user-specified file.
- **Minimal external dependencies**: Uses only Python standard libraries.
- **MD5 checks**: To detect changes in file contents.

## Requirements

- Python 3.7+ (due to usage of modern standard library features)

## Usage

1. Clone or download this repository:
   ```bash
   git clone https://github.com/isgandat/Solution.git
