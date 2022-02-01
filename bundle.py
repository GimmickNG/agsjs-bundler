#!/usr/bin/env python3
import re, pathlib, requests, tempfile
import os, shutil, random, http.server
import argparse, logging, sys

def bundle_ags(data_dir, filepath, game_name, test_input=False, port=0, clobber=False, interactive=True):
    with tempfile.TemporaryDirectory() as outdir:
        index = 'https://raw.githubusercontent.com/ericoporto/ags/master/Emscripten/my_game.html'
        js = 'https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.js'
        wasm = 'https://raw.githubusercontent.com/ericoporto/agsjs/main/ags.wasm'
        logger.debug("Using temporary directory %s", outdir)
        logger.debug('')

        logger.info("Copying files ...")
        game_files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
        num_files = len(game_files)
        for i, file in enumerate(game_files):
            dest = os.path.join(outdir, file)
            logger.debug("[%i/%i] %s ...", i+1, num_files, file)
            shutil.copy(os.path.join(data_dir, file), dest)
        logger.debug('')

        logger.info("Downloading ...")
        logger.debug("[1/3] %s\t> index.html ...", index)
        with open(os.path.join(outdir, 'index.html'), 'w') as index_page:
            index_html = requests.get(index, allow_redirects=True).text
            index_html = re.sub("<title>.*?</title>", f"<title>{re.escape(game_name)}</title>", index_html)
            index_page.write(index_html)
        logger.debug('')

        logger.debug("[2/3] %s\t\t\t\t> ags.js ...", js)
        with open(os.path.join(outdir, 'ags.js'), 'wb') as js_data:
            js_data.write(requests.get(js, allow_redirects=True).content)
        logger.debug('')

        logger.debug("[3/3] %s\t\t\t\t> ags.wasm ...", wasm)
        with open(os.path.join(outdir, 'ags.wasm'), 'wb') as wasm_data:
            wasm_data.write(requests.get(wasm, allow_redirects=True).content)
        logger.debug('')

        logger.info("Writing file list ...")
        with open(os.path.join(outdir, "my_game_files.js"), 'w') as filelist:
            filelist.write(f"var gamefiles = {game_files};")

        test_input = test_input if not interactive else input("Test game? [yN]: ").lower() == "y"
        if test_input:
            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=outdir, **kwargs)
                def log_message(self, format, *args):
                    logger.debug("SRVMSG: %s", args)
            try:
                logger.info('')
                port = args.port or random.randint(2048, 65535)
                httpd = http.server.HTTPServer(('localhost', port), Handler)
                logger.warning("Paste the following URL in your browser to verify the game works: http://localhost:%d/", port)
                logger.warning(">>> Press Ctrl+C (^C) to stop testing, and resume bundling. <<<")
                httpd.serve_forever()
            except KeyboardInterrupt: pass
            finally:
                httpd.server_close()
                httpd.shutdown()
                logger.debug("Testing finished.")

        while not clobber:
            filename = filepath 
            if interactive and not filepath:
                filename = input("Enter output path: ")
            if filename.endswith('.zip'):
                filename = filename[:-4]

            exists = os.path.exists(filename + ".zip")
            if not clobber and exists:
                logger.warning("Warning: name %s exists.", filename)
                if interactive:
                    clobber = input(f"Overwrite? [yN]: ").lower() == "y"
            else:
                break

        if exists and not clobber:
            raise FileExistsError(f"File already exists at {filename}.zip")
        logger.debug("Saving to %s.zip ...", filename)
        shutil.make_archive(filename, 'zip', outdir)

if __name__ == "__main__":
    from_commandline = len(sys.argv) > 1

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--indir", help="The input directory which contains your game files (e.g. acsetup.cfg, any .ags file(s), etc.)")
    parser.add_argument("-o", "--out", help="The output zip file path")
    parser.add_argument("-n", "--name", help="The name of your game, which will appear in the title of index.html")
    parser.add_argument("-f", "--overwrite", action="store_true", help="Overwrites the output file, if it exists")
    parser.add_argument("-t", "--test", action="store_true", help="Serves the game for testing before generating the zip; helpful for checking game compatibility")
    parser.add_argument("-p", "--port", type=int, help="Port to serve game at when testing the game; if set, also sets --test")
    parser.add_argument("-s", "--silent", action="store_true", help="Suppresses all unnecessary output; equivalent to -ccc")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints debug output")
    args = parser.parse_args()

    if args.silent:
        log_level = logging.ERROR
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(format="%(message)s", level=log_level)
    logger = logging.getLogger('bundler')

    title = ("=" * 12) + " AGS Web Bundle Tool " + ("=" * 12)
    logger.info(title)

    try:
        data_dir = args.indir or pathlib.Path(input("Enter data directory path: "))
        if not os.path.exists(data_dir):
            logger.error("Error: path %s does not exist. Exiting...", data_dir)
        else:
            game_name = args.name or input("Enter the name of your game: ")
            if game_name == "":
                raise Exception("Game name cannot be blank.")
            bundle_ags(data_dir, args.out, game_name, args.test or args.port, args.port, args.overwrite, True)
            logger.info("Finished!")
            logger.info("You can now upload this file to Newgrounds/Itch/GameJolt/etc.")
            logger.info('')
            logger.info("Thank you for using AGS JS!")
            logger.info("- By ericoporto @ https://www.github.com/ericoporto/agsjs")
    except KeyboardInterrupt:
        logger.error("Exiting: halted by user")
        sys.exit(130)
    except OSError as err:
        logger.error("Error when saving zip file: %s", err)
        logger.error("Perhaps the file name is invalid? Try again with a different file name.")
    except Exception as err:
        logger.error("Error: %s", err)
    logger.info("=" * len(title))
    if not from_commandline:
        try:
            input("Press Enter to exit.")
        except KeyboardInterrupt: pass
