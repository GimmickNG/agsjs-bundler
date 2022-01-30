# agsjs-bundler
A script to bundle ags games and the agsjs js/wasm dependencies into a zip file for running online.

Depends on the awesome agsjs library  by ericoporto at https://www.github.com/ericoporto/agsjs. 
This script merely takes the generated [``ags.js``](https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.js), [``ags.wasm``](https://github.com/ericoporto/agsjs/raw/main/ags.wasm) and [``index.html``](https://raw.githubusercontent.com/ericoporto/ags/emscripten/Emscripten/my_game.html) in the repository (click each file for their direct link), generates the file list ``my_game_files.js`` based on the files in your data directory and compiles it all into a zip for upload to [Newgrounds](https://www.newgrounds.com)/[Itch](https://www.itch.io)/[GameJolt](https://www.gamejolt.com)/etc. 

You can also test whether the game runs properly when it prompts you; this will open up a http server which serves all the files at ``localhost:<random port>``.

# Requirements
Tested on Python 3.9, but should work on Python 3.4+

## Caveats
- Please carefully read the limitations at https://github.com/ericoporto/ags/blob/emscripten/Emscripten/README.md#changes-from-other-ports if you encounter issues when testing the exported game.
- As mentioned in the above link, if your game has data in subdirectories, it might have to be moved to be in the same directory (i.e. the directory structure might need to be flattened.) This tool only enumerates the files in the same level as the specified data directory, so if you see files are missing in the output .zip then it might be for this reason.

# Usage
1. Copy the script to a folder of your choice.
2. Open a terminal (e.g. Powershell, XTerm, etc.) in the same directory as the script, and run it with the command ``python bundle.py``.

## Sample Run
```
============ AGS Web Bundle Tool ============
Enter data directory path: D:\game_data\

Copying files:
[1/3] acsetup.cfg > C:\Users\GimmickNG\AppData\Local\Temp\tmpeqjrcivd\acsetup.cfg ...DONE
[2/3] audio.vox > C:\Users\GimmickNG\AppData\Local\Temp\tmpeqjrcivd\audio.vox ...DONE
[3/3] game.ags > C:\Users\GimmickNG\AppData\Local\Temp\tmpeqjrcivd\game.ags ...DONE

Downloading:
[1/3] https://raw.githubusercontent.com/ericoporto/ags/emscripten/Emscripten/my_game.html    > index.html ...DONE
[2/3] https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.js                         > ags.js ...DONE
[3/3] https://github.com/ericoporto/agsjs/raw/main/ags.wasm                                  > ags.wasm ...DONE

Writing file list ...DONE

Test game? [yN]: y

Paste the following URL in your browser to verify the game works: http://localhost:32053/
>>> Press Ctrl+C (^C) to stop testing, and resume export. <<<
Testing finished.

Enter output filename: D:\game_export.zip
Saving to D:\game_export.zip ...DONE

Finished! Output: D:\game_export.zip
You can now upload this file to Newgrounds/Itch/GameJolt/etc.!

Thank you for using AGS JS!
By ericoporto @ https://www.github.com/ericoporto/agsjs
=============================================
```
