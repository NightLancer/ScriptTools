# Author: NightLancerX
import os
import re
from pathlib import Path

master_ini_content = None

def read_master_ini(master_ini_path):
    global master_ini_content
    swapkey_mapping = {}
    try:
        with open(master_ini_path, 'r', encoding='utf-8') as file:
            master_ini_content = file.read() #save in case of namespaces later
            for line in master_ini_content.splitlines():
                match = re.match(r'\$\\mods\\(?:.*\/)*([^\\]+)\\(.+?)\s*= (\d+)', line)
                if match:
                    mod_name, swapkey, value = match.groups()
                    key = str(os.path.join(mod_name, swapkey)).lower()
                    swapkey_mapping[key] = value
                    continue
    except FileNotFoundError:
        print(f"!!!d3dx_user.ini file not found at: {master_ini_path}!!!\n")
    
    return swapkey_mapping

def collect_ini(path, ignore=True):
    ini_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if (ignore and "DISABLED" in file.upper()):
                continue
            if os.path.splitext(file)[1] == ".ini":
                ini_files.append(os.path.join(root, file))
    return ini_files

def update_ini_file(modpath, file_path, swapkey_mapping):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nProcessing - {os.path.basename(file_path)}")
    modified = [False]  # Use a list to track modification status
    
    # Check if the file has a namespace definition
    namespace_match = re.search(r'namespace\s*=\s*(.+)', content) #if someone uses it with spaces he's insane.
    namespace = namespace_match.group(1).strip() if namespace_match else None
    
    def replace(match):
        swapkey = match.group(1)
        old_value = match.group(2)
        
        key = None
        new_value = None
        
        if namespace:
            _namespace = re.sub(r"[\\/]", ".", namespace).lower()   
            search = re.search(rf"{_namespace}.{swapkey}\s*=\s*(\d+)", master_ini_content)
            if search:
                new_value = search.group(1)
                key = f"{namespace}\\{swapkey}"
        else:
            key = (str(Path(file_path).relative_to(modpath))+'\\'+swapkey).lower()
            new_value = swapkey_mapping.get(key)
        
        if new_value and new_value != old_value:
            print(f"{key.replace('skinselectimpact', '')}, {old_value} -> {new_value}")
            modified[0] = True
            return f'global persist ${swapkey} = {new_value}'
        return match.group(0)  # Return unchanged if no replacement found
    
    updated_content = re.sub(r'global persist \$(\w+) = (\d+)', replace, content)
    
    if modified[0]:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    else:
        print("*No changes*")
        
def find_mod_paths(current_path):
    mods_index = current_path.rfind("Mods")
    
    if mods_index == -1:
        print("Warning: Not running from within a Mods folder!")
        return None, None
    
    modpath = current_path[:mods_index] + "Mods"
    master_ini_path = os.path.join(modpath.rsplit("Mods", 1)[0], "d3dx_user.ini")
    
    return modpath, master_ini_path

def main():
    modpath, master_ini_path = find_mod_paths(os.getcwd())
    if not modpath or not master_ini_path:
        print("Could not determine paths. Please run this script from within the Mods folder."); return
        
    print(f"Using mod path: {modpath}")
    print(f"Using master INI: {master_ini_path}")
    
    swapkey_mapping = read_master_ini(master_ini_path)
    
    if not swapkey_mapping:
        print("No valid mappings found in the d3dx_user.ini.\n"); return

    ini_files = collect_ini(os.getcwd())
    for ini_file in ini_files:
        update_ini_file(modpath, ini_file, swapkey_mapping)

if __name__ == "__main__":
    main()

os.system("pause")
