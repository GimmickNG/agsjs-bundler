# agsjs-bundler
A script to bundle ags games and the agsjs js/wasm dependencies into a zip file for running online.

Depends on the awesome agsjs library  by ericoporto at https://www.github.com/ericoporto/agsjs. 
This script merely takes the generated [``ags.js``](https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.js), [``ags.wasm``](https://github.com/ericoporto/agsjs/raw/main/ags.wasm) and [``index.html``](https://raw.githubusercontent.com/ericoporto/ags/emscripten/Emscripten/my_game.html) in the repository (click each file for their direct link), and generates the file list ``my_game_files.js`` based on the files in your data directory.

# Requirements
Tested on Python 3.9, but should work on Python 3.4+

# Usage
Copy the script to a folder of your choice.

Open a terminal (e.g. Powershell/XTerm) in the same directory as the script, and run it with the command ``python compile.py``.
