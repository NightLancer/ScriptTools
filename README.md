# Global Persist Swapkey
Automatically saves(writes to mod's ini) all active swapkey values for given mod(s).<br>
Supports XXMI/GIMI/SRMI/ZZMI/3dmigoto/etc as long as `d3dx_user.ini` is located on same level as main `Mods` folder.<br>

## Setup:
* Ensure Python is installed (and was added to Path variable during install)
  - (Optional) Open console(as Admin if needed) and execute: `pip install colorama` (coloring library for better readability)
* Advanced (regedit submenu) [\***recommended**\*]:
  - Put `Global Persist Swapkey.py`, `S.ico`, `Add Context-menu command.bat`, `Delete Context-menu command.bat` inside any stable path(folder) that won't be renamed/moved
  - Run `Add Context-menu command.bat` to register submenu<br>
    - (To delete submenu run `Delete Context-menu command.bat`)<br>
* Simple (direct script file):
  - (Optional) create shortcut to the script with empty work directory 
    
## Usage:
  * Set desired mod variation in-game and press `F10`
  * Advanced setup:
    - Open mod folder and click on command from context menu(RMB):<br>
    ![subm](https://github.com/user-attachments/assets/aa24ef01-c960-4f4f-af08-af83c889db1a)<br>
  * Simple setup:
    - Copy `Global Persist Swapkey.py`(or prepared shortcut) inside needed mod folder and run it
  * Script will look for all `.ini` files inside given mod folder(skipping `DISABLED`) and set new swapvalues:<br>
    ![disp](https://github.com/user-attachments/assets/65df97bd-cbd9-4444-9d84-4a060099c047)
