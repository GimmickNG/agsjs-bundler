# agsjs-bundler
A quick script to bundle ags games and the agsjs js/wasm dependencies into a zip file for running online. (This code uses quite a few snippets from stackoverflow, e.g. http server related code, etc.)

Depends on the awesome agsjs library  by ericoporto at https://www.github.com/ericoporto/agsjs. 
This script merely takes the generated [``ags.js``](https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.js), [``ags.wasm``](https://github.com/ericoporto/agsjs/raw/main/ags.wasm) and [``index.html``](https://raw.githubusercontent.com/ericoporto/ags/emscripten/Emscripten/my_game.html) in the repository (click each file for their direct link), generates the file list ``my_game_files.js`` based on the files in your data directory and compiles it all into a zip for upload to [Newgrounds](https://www.newgrounds.com)/[Itch](https://www.itch.io)/[GameJolt](https://www.gamejolt.com)/etc. 

You can also test whether the game runs properly when it prompts you; this will open up a http server which serves all the files at ``localhost:<random port>``.

# Requirements
Python 3.4+, but works best on Python 3.7+
Requires the ``requests`` library. Get it with ``python -m pip install requests``.

## Caveats
- Please carefully read the limitations at https://github.com/ericoporto/ags/blob/emscripten/Emscripten/README.md#changes-from-other-ports if you encounter issues when testing the exported game.
- As mentioned in the above link, if your game has data in subdirectories, it might have to be moved to be in the same directory (i.e. the directory structure might need to be flattened.) This tool only enumerates the files in the same level as the specified data directory, so if you see files are missing in the output .zip then it might be for this reason.

# Usage
1. Copy the script to a folder of your choice.
2. Open a terminal (e.g. Powershell, XTerm, etc.) in the same directory as the script, and run it with the command ``python bundle.py``. Alternatively, if using Windows, just double-click ``bundle.py`` to run it directly.
3. Enter the data directory. This is the directory containing your .ags files and other data (in the example below, ``audio.vox``, ``acsetup.cfg`` and ``game.ags`` are in the ``D:\game_data`` directory)
4. A temporary folder will be created to house the files before the zip is built. Wait for the steps to continue.
5. If you want to test the game, enter "y" or "Y" at the prompt. Anything else will be treated as a 'no'.
    - If you selected "Y" to testing the game, the link where the server is hosting the content will be displayed; paste this in your browser of choice.
    - The game should appear. If there is a black screen with an error message instead, then your game may have issues exporting. Check the [Caveats](#Caveats) section for more information.
6. If the game runs correctly, then press ``Ctrl+C`` to stop the server and resume the bundling process.
7. Enter the output file name or path when prompted.
8. Wait for the file to be saved at the given location.
9. You can now upload this file to the site of your choice!


## Sample Run
```
============ AGS Web Bundle Tool ============
Enter data directory path: E:\mygame
Enter the name of your game: Test Game

Copying files:
[1/3] acsetup.cfg ...DONE
[2/3] audio.vox ...DONE
[3/3] game.ags ...DONE

Downloading:
[1/3] https://raw.githubusercontent.com/ericoporto/ags/emscripten/Emscripten/my_game.html       > index.html ...DONE
[2/3] https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.js                            > ags.js ...DONE
[3/3] https://github.com/ericoporto/agsjs/raw/main/ags.wasm                                     > ags.wasm ...DONE

Writing file list ...DONE

Test game? [yN]: y

Paste the following URL in your browser to verify the game works: http://localhost:5633/
>>> Press Ctrl+C (^C) to stop testing, and resume bundling. <<<
Testing finished.

Enter output filename: test.zip
Saving to test.zip ...DONE

Finished! Output: test.zip
You can now upload this file to Newgrounds/Itch/GameJolt/etc.
Thank you for using AGS JS!
- By ericoporto @ https://www.github.com/ericoporto/agsjs
=============================================
Press any key to continue...
```
