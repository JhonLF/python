import os
import shutil
import time
import argparse
import hashlib
from datetime import datetime


def log_action(action, path, log_file):
    """
    Logs an action to the log file
    """
    # Log string with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {action}: {path}"

    # Print log message
    print(log_message)

    # Append log message to file
    with open(log_file, "a") as log:
        log.write(log_message + "\n")


def file_md5(file_path):
    """
    Calculates MD5 hash of file
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read file in chunks
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def sync_dirs(src, dest, log_file):
    """
    Syncs source directory with destination
    """

    # Walk through source directory tree
    for src_dir, _, files in os.walk(src):

        # Build equivalent destination path
        dest_dir = src_dir.replace(src, dest, 1)

        # Check if destination directory exists, create if needed
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            log_action("Directory created", dest_dir, log_file)

        # Loop through files in current directory
        for file in files:

            # Build full source and destination paths
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(dest_dir, file)

            # Copy if destination file does not exist or is different
            if not os.path.exists(dest_file) or file_md5(src_file) != file_md5(dest_file):
                shutil.copy2(src_file, dest_file)
                log_action("File copied/updated", dest_file, log_file)

    # Walk through destination tree backwards
    for dest_dir, _, files in os.walk(dest, topdown=False):

        # Get corresponding source path
        src_dir = dest_dir.replace(dest, src, 1)

        # If source folder does not exist, remove destination folder
        if not os.path.exists(src_dir):
            shutil.rmtree(dest_dir)
            log_action("Directory removed", dest_dir, log_file)

        # Loop through destination files
        for file in files:

            # Build paths
            dest_file = os.path.join(dest_dir, file)
            src_file = os.path.join(src_dir, file)

            # If source file does not exist, remove destination file
            if not os.path.exists(src_file):
                os.remove(dest_file)
                log_action("File removed", dest_file, log_file)


def main():
    """
    Main entry point
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Synchronize directories")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("replica", help="Replica directory")
    parser.add_argument("interval", type=int, help="Sync interval in seconds")
    parser.add_argument("log", help="Log file path")
    args = parser.parse_args()

    # Run synchronization continuously
    while True:
        sync_dirs(args.source, args.replica, args.log)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
