import os
import sys
import time
import argparse
import logging
import hashlib
from pathlib import Path

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source_dir, replica_dir, logger):
    source_dir = Path(source_dir)
    replica_dir = Path(replica_dir)

    replica_dir.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        rel_path = Path(root).relative_to(source_dir)
        target_root = replica_dir / rel_path

        target_root.mkdir(exist_ok=True)

        for file_name in files:
            source_file = Path(root) / file_name
            replica_file = target_root / file_name

            if not replica_file.exists():
                logger.info(f"Creating file: {replica_file}")
                copy_file(source_file, replica_file, logger)
            else:
                source_md5 = calculate_md5(source_file)
                replica_md5 = calculate_md5(replica_file)
                if source_md5 != replica_md5:
                    logger.info(f"Updating file: {replica_file}")
                    copy_file(source_file, replica_file, logger)

    for root, dirs, files in os.walk(replica_dir):
        rel_path = Path(root).relative_to(replica_dir)
        corresponding_source_root = source_dir / rel_path

        for file_name in files:
            replica_file = Path(root) / file_name
            source_file = corresponding_source_root / file_name

            if not source_file.exists():
                logger.info(f"Removing file: {replica_file}")
                replica_file.unlink()

def copy_file(src, dst, logger):
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
            fdst.write(fsrc.read())
    except Exception as e:
        logger.error(f"Failed to copy {src} to {dst}. Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="One-way folder synchronization script.")
    parser.add_argument("--source", required=True, help="Path to the source folder.")
    parser.add_argument("--replica", required=True, help="Path to the replica folder.")
    parser.add_argument("--log-file", required=True, help="Path to the log file.")
    parser.add_argument("--interval", type=int, default=60, help="Sync interval in seconds.")

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        filename=args.log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logger = logging.getLogger(__name__)

    logger.info("Starting folder synchronization service.")
    logger.info(f"Source: {args.source}")
    logger.info(f"Replica: {args.replica}")
    logger.info(f"Interval: {args.interval} seconds")

    # Run synchronization periodically
    try:
        while True:
            sync_folders(args.source, args.replica, logger)
            logger.info("Synchronization cycle complete. Waiting for next interval...")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Synchronization service interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
