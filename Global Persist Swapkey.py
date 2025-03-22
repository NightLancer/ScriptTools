# Author: NightLancerX
import os
import re
from pathlib import Path

def read_master_ini(master_ini_path):
    swapkey_mapping = {}
    namespace_mapping = {}  # New mapping for namespace-based entries
    
    try:
        with open(master_ini_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Try to match the regular file path pattern
                match = re.match(r'\$\\mods\\skinselectimpact\\(?:.*\/)*([^\\]+)\\(.+?)\s*= (\d+)', line)
                if match:
                    mod_name, swapkey, value = match.groups()
                    key = str(os.path.join(mod_name, swapkey)).lower()
                    swapkey_mapping[key] = value
                    continue
                
                # Try to match the namespace pattern
                namespace_match = re.match(r'\$\\([a-f0-9_]+)\\(\w+)\s*= (\d+)', line)
                if namespace_match:
                    namespace, swapkey, value = namespace_match.groups()
                    namespace_mapping[(namespace, swapkey)] = value
    except FileNotFoundError:
        print(f"!!!d3dx_user.ini file not found at: {master_ini_path}!!!\n")
    
    return swapkey_mapping, namespace_mapping

def collect_ini(path, ignore=True):
    ini_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if (ignore and "DISABLED" in file.upper()):
                continue
            if os.path.splitext(file)[1] == ".ini":
                ini_files.append(os.path.join(root, file))
    return ini_files

def update_ini_file(modpath, file_path, swapkey_mapping, namespace_mapping):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Processing - {os.path.basename(file_path)}\n")
    modified = [False]  # Use a list to track modification status
    
    # Check if the file has a namespace definition
    namespace_match = re.search(r'namespace\s*=\s*([a-f0-9_]+)', content)
    namespace = namespace_match.group(1) if namespace_match else None
    
    def replace(match):
        swapkey = match.group(1)
        old_value = match.group(2)
        
        new_value = None
        if namespace:
            # Try to find the value in the namespace mapping
            new_value = namespace_mapping.get((namespace, swapkey))
            key = f"{namespace}\\{swapkey}"  # For display purposes
        else:
            # Use the original path-based mapping
            key = (str(Path(file_path).relative_to(modpath))+'\\'+swapkey).lower()
            new_value = swapkey_mapping.get(key)
        
        if new_value and new_value != old_value:
            print(f"{key}, {old_value} -> {new_value}\n")
            modified[0] = True
            return f'global persist ${swapkey} = {new_value}'
        return match.group(0)  # Return unchanged if no replacement found
    
    updated_content = re.sub(r'global persist \$(\w+) = (\d+)', replace, content)
    
    if modified[0]:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Updated: {os.path.basename(file_path)}\n")
    else:
        print("*No changes*\n")

def main():
    modpath = r"D:\Mods\3dmigoto_ZenlessZoneZero\Mods\SkinSelectImpact"
    master_ini_path = r"D:\Mods\3dmigoto_ZenlessZoneZero\d3dx_user.ini"
    swapkey_mapping, namespace_mapping = read_master_ini(master_ini_path)
    
    if not swapkey_mapping and not namespace_mapping:
        print("No valid mappings found in the d3dx_user.ini.\n")
        return

    ini_files = collect_ini(os.getcwd())
    for ini_file in ini_files:
        update_ini_file(modpath, ini_file, swapkey_mapping, namespace_mapping)

if __name__ == "__main__":
    main()

os.system("pause")
