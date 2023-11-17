import argparse

# logging.basicConfig(filename=str(settings.LOCAL_FOLDER / "docmaker.log"), encoding='utf-8', level=logging.DEBUG)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True, help='Command to be used')

p_link_macro = subparsers.add_parser("link-macro")

args = parser.parse_args()
match args.command:
    case "link-macro":
        from docmaker import link_lo_macro
        link_lo_macro()            
   