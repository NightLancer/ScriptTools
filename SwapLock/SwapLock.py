# Author: NightLancerX
import os
import re
import shutil
import argparse
try:
    from colorama import init, Fore
except ImportError:
    Fore_GREEN, Fore_RED, Fore_YELLOW = '','',''
else: 
    init(autoreset=True)
    Fore_GREEN = Fore.GREEN
    Fore_RED = Fore.RED
    Fore_YELLOW = Fore.YELLOW

def collect_ini(path, ignore=True):
    ini_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if (ignore and "DISABLED" in file.upper()):
                continue
            if os.path.splitext(file)[1] == ".ini":
                ini_files.append(os.path.join(root, file))
    return ini_files

def make_backup(ini_path):
    folder, filename = os.path.split(ini_path)
    name, ext = os.path.splitext(filename)
    backup_name = f"DISABLED_{name}_backup{ext}"
    backup_path = os.path.join(folder, backup_name)

    # Always overwrite existing backup
    shutil.copy2(ini_path, backup_path)
    print(f"Backup created: {Fore_YELLOW}{backup_name}{Fore.RESET}")
    return backup_path


def restore_backups(path):
    restored = 0
    for root, _, files in os.walk(path):
        for file in files:
            if file.startswith("DISABLED_") and "_backup" in file and file.endswith(".ini"):
                backup_path = os.path.join(root, file)

                # Recover original name
                name = file.replace("DISABLED_", "").replace("_backup", "")
                ini_path = os.path.join(root, name)

                if os.path.exists(ini_path):
                    os.remove(ini_path)

                os.rename(backup_path, ini_path)
                print(f"Restored backup -> {Fore_GREEN}{ini_path}{Fore.RESET}")
                restored += 1

    if not restored:
        print("No backup files found to restore.")


def process(ini_path):
    with open(ini_path, 'r') as file:
        content = file.read()

    pattern = r"(condition\s*=\s*.*?)(?=\r?\n)"

    count = 0
    locked = 0
    def replace_match(match):
        nonlocal count, locked
        text = match.group(1)
        if "lock" in text:
            locked += 1
            return text
        count += 1
        return text + " && $\SwapLock\\locked == 0"

    updated_content = re.sub(pattern, replace_match, content)
    print(f"Conditions processed: {Fore_GREEN}{count}{Fore.RESET}")
    if locked:
        print(f"!! Already locked conditions: {Fore_YELLOW}{locked}{Fore.RESET} !!")

    if updated_content != content:
        make_backup(ini_path)
        with open(ini_path, 'w') as file:
            file.write(updated_content)
        print(f"{os.path.basename(ini_path)} has been updated.\n")
    else:
        print("No replacements made.\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--restore", action="store_true", help="Restore from DISABLED_*_backup.ini files")
    args = parser.parse_args()

    cwd = os.getcwd()

    if args.restore:
        restore_backups(cwd)
        return

    ini_files = collect_ini(cwd)
    for ini_file in ini_files:
        print(f"Processing - {os.path.basename(ini_file)}\n")
        process(ini_file)


if __name__ == "__main__":
    main()

os.system("pause")