"""
Parse keyboard shortcuts data from Roland SP-404 manual PDF
"""
import argparse
from parse_pdf import read_to_json
from translator import translate_file
from targets.telegraph import telegraph_update
from targets.markdown import markdown_render


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["parse", "telegraph", "markdown", "translate"])
    
    args = parser.parse_args()
    if args.command == "parse":
        read_to_json(pdf_filename="pdf/SP-404MK2_v5_reference_eng03_W.pdf", json_filename="tables.json")
    
    elif args.command == "telegraph":
        telegraph_update(src_filename="translated.json", locale="Ru")
    
    elif args.command == "markdown":
        markdown_render(src_filename="translated.json", dst_filename="shortcuts.md", locale="Ru")

    elif args.command == "translate":
        translate_file()

    else:    
        print(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
