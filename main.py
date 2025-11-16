"""
Parse keyboard shortcuts data from Roland SP-404 manual PDF
"""

import argparse
from process.parse_pdf import read_to_json
from process.translator import translate_file
from targets.telegraph import telegraph_update
from targets.markdown import markdown_render


def main():
    pdf = "pdf/SP-404MK2_v5_reference_eng03_W.pdf"
    tables = "json/tables.json"
    translated = "json/translated.json"
    markdown = "output/shortcuts.md"
    tmp_bilingual = "json/bilingual.json"
    locale = "Ru"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=["parse", "telegraph", "markdown", "translate"]
    )
    args = parser.parse_args()
    command = args.command

    if command == "parse":
        read_to_json(
            pdf_filename=pdf, json_filename=tables, page_numbers=range(144, 149)
        )

    elif command == "telegraph":
        telegraph_update(src_filename=translated, locale=locale)

    elif command == "markdown":
        markdown_render(src_filename=translated, dst_filename=markdown, locale=locale)

    elif command == "translate":
        translate_file(src_json_filename=tables, dst_json_filename=tmp_bilingual)

    else:
        print(f"Unknown command {command}")


if __name__ == "__main__":
    main()
