"""
Parse keyboard shortcuts data from Roland SP-404 manual PDF
"""

import deepl
from dotenv import load_dotenv
from footer import credits, updated_at
from header import header
import json
import os
import pdfplumber
import re
from telegraph import Telegraph
import textwrap

load_dotenv()  # reads variables from a .env file and sets them in os.environ

deepl_count = 0
deepl_length = 0


def read_to_json(
    pdf_filename="pdf/SP-404MK2_v5_reference_eng03_W.pdf", json_filename="tables.json"
):
    """
    Read and parse tables from a PDF file,
    save nested array to a JSON file.

    Saved file requires minor manual editing afterwards:
    remove repeated table headers on page breaks,
    add missing section titles.
    """
    if not os.path.exists(pdf_filename) or not os.access(pdf_filename, os.R_OK):
        raise RuntimeError(f"Not exists: {pdf_filename}")

    tables = list()
    with pdfplumber.open(pdf_filename) as pdf:
        for page_index in range(144, 149):
            page = pdf.pages[page_index]
            tables.extend(page.extract_tables())

    with open(json_filename, "w") as output:
        json.dump(tables, output, ensure_ascii=False, indent=2)


def buttons_from_str(str=""):
    """
    Extract button names from text.
    Example:
        buttons_from_str("test [One] and [TWO] and more") # ['One', 'TWO']
    """
    pattern = r"\[([^\]]+)\]"
    
    return re.findall(pattern, str)


def shortcuts_in_mode(str=""):
    """
    Extract mode names from text.
    Example:
        buttons_from_str("Shortcuts used in DJ mode") # ['DJ mode']
    """
    pattern = r"Shortcuts used in (.*)"
    
    return re.findall(pattern, str)


def get_deepl_client():
    """
    Provide singleton DeepL client instance
    """
    if not hasattr(get_deepl_client, "client"):
        auth_key = os.getenv("DEEPL_API_KEY")
        proxy = os.getenv("PROXY")
        get_deepl_client.client = deepl.DeepLClient(auth_key, proxy=proxy)

    return get_deepl_client.client


def deepl_translate(text, source_lang="EN", target_lang="RU"):
    """
    Translate a single piece of text
    """
    global deepl_count
    global deepl_length

    deepl_count += 1
    deepl_length += len(text)

    deepl_client = get_deepl_client()
    result = deepl_client.translate_text(text, source_lang=source_lang, target_lang=target_lang)

    return result.text


def translate_file(
    src_json_filename="tables.json", dest_json_filename="bilingual.json"
):
    """
    Read saved and manually adjusted JSON file,
    translate every entry's last item from English to Russian
    and save resulting array to another JSON file.
    """
    bilingual = []

    key_Section = "Section"
    key_Title_En = "Title_En"
    key_Title_Ru = "Title_Ru"
    En = "En"
    Ru = "Ru"

    with open(src_json_filename, "r") as fp_json:
        data_en = json.load(fp_json)
        for section in data_en:
            title_En = section[0][0]
            title_Ru = deepl_translate(title_En)
            EnList = []
            RuList = []

            section_key = ""

            """
            Get section key. In example: "SHIFT", "COPY" or "DJ mode"
            """
            btns = buttons_from_str(title_En)
            if len(btns) > 0:
                section_key = btns[0]
            else:
                modes = shortcuts_in_mode(title_En)
                if len(modes) > 0:
                    section_key = modes[0]
            if len(section_key) == 0:
                raise RuntimeError(f"Failed to get section key from {title_En}")

            """
            Loop through other rows
            """
            last_index = len(section[1]) - 1
            for entry in section[1:]:
                EnList.append(entry[:])
                entry[0] = deepl_translate(entry[0])
                # middle entry is NOT translated in "SHIFT" and "DJ mode" triple cases
                entry[last_index] = deepl_translate(entry[last_index])
                RuList.append(entry)

            bilingual.append(
                {
                    key_Section: section_key,
                    key_Title_En: title_En,
                    key_Title_Ru: title_Ru,
                    En: EnList,
                    Ru: RuList,
                }
            )

    with open(dest_json_filename, "w") as fp_out:
        json.dump(bilingual, fp_out, ensure_ascii=False, indent=2)

    print(f"DeepL calls count: {deepl_count}, sent text length: {deepl_length} bytes")



def fit_lines(str, indent=4, break_on_newline=True):
    """
    Break long text line into multiple lines

    Args:
        str (string) source text
        indent (int) number of spaces to prepend to every reasult line (removing leading whitespace first)
        break_on_newlines (bool) whether to respect newlines in text or treat them as plain whitespace

    Returns:
        list of strings
    """
    max_line_length = 40
    prefix = " " * indent

    if break_on_newline:
        wrapped_lines = []
        for part in str.split("\n"):
            wrapped_lines.extend(textwrap.wrap(part, width=max_line_length))
    else:
        wrapped_lines = textwrap.wrap(
            str,
            width=max_line_length,
        )

    return list(map(lambda s: prefix + s.lstrip(), wrapped_lines))


def test_fit_lines():
    test_01 = "   This is a multiline long text\nthat\nis split\nby some\n   newlines. It also has a     long piece of text that should be cut into multple short lines, I assume."
    result = fit_lines(test_01)
    # print(result)
    for line in result:
        print(line)


def telegraph_update(src_filename="translated.json", locale="Ru"):
    """
    Render Telegra.ph markup from translated JSON
    and update the page.

    Telegra.ph allowed tags:
    a, aside, b, blockquote, br, code, em, figcaption, figure, h3, h4, hr, i, iframe, img, li, ol, p, pre, s, strong, u, ul, video.
    
    API docs: https://telegra.ph/api
    """
    with open(src_filename, "r") as json_src:
        data = json.load(json_src)
        
        content = []
        
        """Add header notes and section links"""
        content.extend(header(data, locale=locale))

        """Render Telegra.ph node tree"""
        for section in data:
            content.append({"tag": "h4", "children": [section["Section"]]})
            content.append({"tag": "p", "children": [section[f"Title_{locale}"]]})

            length = len(section[locale][0])

            rows = []
            for row in section[locale]:
                rows.append("")
                if length == 3:
                    if row[1] == "–":
                        rows.append(f"{row[0]}")
                        rows.extend(fit_lines(row[2]))
                    else:
                        rows.append(f"{row[0]}")
                        rows.append(f"    {row[1]}")
                        rows.extend(fit_lines(row[2]))
                elif length == 2:
                    rows.append(f"{row[0]}")
                    rows.extend(fit_lines(row[1]))

            content.append({"tag": "pre", "children": ["\n".join(rows)]})
            content.append({"tag": "hr"})

        """Add footer notes"""
        content.append(credits(locale=locale))
        content.append(updated_at(locale=locale))

        """Invoke Telegra.ph API to update the page"""
        telegraph = Telegraph(access_token=os.getenv("TELEGRAPH_TOKEN"))

        response = telegraph.edit_page(
            path=os.getenv("TELEGRAPH_PAGE_PATH"),
            author_url="https://t.me/sp404community",
            author_name="sp404community",
            title="Шорткаты SP-404MK2",
            content=content,
        )

        """Final output"""
        print(response["url"])


def main():
    # translate_file()
    telegraph_update(src_filename="translated.json", locale="Ru")


if __name__ == "__main__":
    main()
