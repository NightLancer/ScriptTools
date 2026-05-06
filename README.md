# Global Persist Swapkey
Tool for saving all currently-applied(active) swapkeys' values to a mod's ini (ensuring they will not be reset after swapping to other mod/renaming mod's folder).<br>
Supports any 3dmigoto-based modloader as long as `d3dx_user.ini` is located on same level as main `Mods` folder.<br>
Doesn't support symlinked `Mods` folder.<br>

## Setup:
* Advanced (regedit submenu) [\***recommended**\*]:
  - Install ![Python](https://www.python.org/downloads/) with `Path` variable checkmarked
  - Download latest ![GlobalPersistSwapkey](https://github.com/NightLancer/ScriptTools/releases/tag/GlobalPersistSwapkey) archive from release page
  - Extract archive's content inside any stable path(folder) that won't be renamed/moved
  - Run `Add Context-menu command.bat` to register submenu [ -a]<br>
    - (To delete submenu run `Delete Context-menu command.bat`) [ -d]<br>
* Simple (no registry, no python installation):
  - Download (only) ![GlobalPersistSwapkey.exe](https://github.com/NightLancer/ScriptTools/releases/download/GlobalPersistSwapkey/GlobalPersistSwapkey.exe)
    
## Usage:
  * Set desired mod variation in-game and press `F10`
  * Advanced setup:
    - Open mod folder and click on command from context menu(RMB):<br>
    ![subm](https://github.com/user-attachments/assets/aa24ef01-c960-4f4f-af08-af83c889db1a)<br>
  * Simple setup:
    - Move `GlobalPersistSwapkey.exe` inside needed mod folder and run it
  * Script will look for all `.ini` files inside given mod folder(skipping `DISABLED`) and set new swapvalues:<br>
    ![disp](https://github.com/user-attachments/assets/65df97bd-cbd9-4444-9d84-4a060099c047)


# SwapLock
Lock all mods' swapkeys behind desired master key. Helps to prevent unintended accidental swapping for mods having a lot of keyboard mapped(especially over in-game keys).

## Setup:
* Place `SwapLock.ini` inside `BufferValues` folder (if you don't have one - can just place in 'Mods' folder)
* Run `SwapLock.py` inside single modfolder - or outside several modfolders to process all at once.<br>
  Before overwriting ini backup will be created.<br>
   ![1](https://github.com/user-attachments/assets/fd1cf361-3654-4e1a-bd27-d14401d51e23)<br>
   - running it over already processed inis will not take effect
     ![2](https://github.com/user-attachments/assets/412fbf7b-78d8-4ec8-80d6-f506645d056b)<br>
* To restore backuped version run `SwapLock.py -r` from console within needed folder(s)
   ![3](https://github.com/user-attachments/assets/dd089267-73e7-49c0-9cb1-50ee10a252ad)<br>

  
## Usage:
* Press `\` key (main keyboard) to toggle lock state. Key can be changed in the `SwapLock.ini`<br>
  Information about lock state will be displayed for 2 seconds upon change.<br>
  ![4](https://github.com/user-attachments/assets/ca153b7c-ed35-45ed-b56d-fdca782a5643)
  
