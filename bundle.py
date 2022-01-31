#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
from pathlib import Path
from shutil import make_archive
from http.server import HTTPServer, SimpleHTTPRequestHandler
from random import randint
from re import escape, sub as replace
import requests, tempfile, os, shutil

title = ("=" * 12) + " AGS Web Bundle Tool " + ("=" * 12)
print(title)

try:
    data_dir = Path(input("Enter data directory path: "))
    game_name = input("Enter the name of your game: ")
    if os.path.exists(data_dir):
        with tempfile.TemporaryDirectory() as outdir:
            index = 'https://raw.githubusercontent.com/ericoporto/ags/emscripten/Emscripten/my_game.html'
            js = 'https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.js'
            wasm = 'https://github.com/ericoporto/agsjs/raw/main/ags.wasm'
            print()

            print("Copying files:")
            game_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
            num_files = len(game_files)
            for i, file in enumerate(game_files):
                dest = join(outdir, file)
                print(f"[{i+1}/{num_files}] {file} ...", end='')
                shutil.copy(join(data_dir, file), dest)
                print("DONE")
            print()

            print("Downloading:")
            print(f"[1/3] {index}\t> index.html ...", flush=True, end='')
            with open(join(outdir, 'index.html'), 'w') as index_page:
                index_html = requests.get(index, allow_redirects=True).text
                index_html = replace("<title>.*?</title>", f"<title>{escape(game_name)}</title>", index_html)
                index_page.write(index_html)
            print("DONE")

            print(f"[2/3] {js}\t\t\t\t> ags.js ...", flush=True, end='')
            with open(join(outdir, 'ags.js'), 'wb') as js_data:
                js_data.write(requests.get(js, allow_redirects=True).content)
            print("DONE")

            print(f"[3/3] {wasm}\t\t\t\t\t> ags.wasm ...", flush=True, end='')
            with open(join(outdir, 'ags.wasm'), 'wb') as wasm_data:
                wasm_data.write(requests.get(wasm, allow_redirects=True).content)
            print("DONE")
            print()

            print("Writing file list ...", flush=True, end='')
            with open(join(outdir, "my_game_files.js"), 'w') as filelist:
                filelist.write(f"var gamefiles = {game_files};")
            print("DONE")
            print()

            test_game = input("Test game? [yN]: ") == "y"
            if test_game:
                class Handler(SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=outdir, **kwargs)
                    def log_message(self, format, *args):
                        return
                try:
                    print()
                    port = randint(2048, 65535)
                    httpd = HTTPServer(('localhost', port), Handler)
                    print(f"Paste the following URL in your browser to verify the game works: http://localhost:{port}/")
                    print(">>> Press Ctrl+C (^C) to stop testing, and resume bundling. <<<")
                    httpd.serve_forever()
                except KeyboardInterrupt: pass
                finally:
                    httpd.server_close()
                    httpd.shutdown()
                    print("Testing finished.")
            print()

            clobber = False
            while not clobber:
                filename = input("Enter output filename: ")
                if filename.endswith('.zip'):
                    filename = filename[:-4]

                if os.path.exists(filename + ".zip"):
                    clobber = input(f"Warning: name {filename}.zip exists, overwrite? [yN]: ").lower() == "y"
                else:
                    break

            print(f"Saving to {filename}.zip ...", flush=True, end='')
            make_archive(filename, 'zip', outdir)
            print("DONE")
            print()
        try:
            print(f"Finished! Output: {filename}.zip")
            print("You can now upload this file to Newgrounds/Itch/GameJolt/etc.", end='')
            if not test_game:
                print(" - ensure it works in the preview before uploading.")
            print()
            print("Thank you for using AGS JS!")
            print("- By ericoporto @ https://www.github.com/ericoporto/agsjs")
        except:
            print("Could not create the zip file as there was likely an error during the process.")
    else:
        print(f"Error: path {data_dir} does not exist. Exiting...")
except KeyboardInterrupt:
    print()
    print()
    print("Exiting: halted by user")
except OSError as err:
    print()
    print()
    print("Error when saving zip file: ", err)
    print("Perhaps the file name is invalid? Try again with a different file name.")
print("=" * len(title))
input()
