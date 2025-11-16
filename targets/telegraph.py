import json
from datetime import datetime
import os
import textwrap
from telegraph import Telegraph
from dotenv import load_dotenv

load_dotenv()  # reads variables from a .env file and sets them in os.environ


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


def _test_fit_lines():
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


def updated_at(locale="Ru"):
    local_datetime = datetime.now().astimezone()
    formatted_datetime = local_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")

    return {"tag": "p", "children": ["Обновлено: ", formatted_datetime, "."]}

def credits(locale="Ru"):
    if locale == "Ru":
        return _sp404community()

def _sp404community():
    return {
        "tag": "p",
        "children": [
            "Информация из ",
            {
                "tag": "a",
                "attrs": {
                    "href": "https://www.roland.com/global/support/by_product/sp-404mk2/owners_manuals/"
                },
                "children": ["официального мануала"],
            },
            " Roland для SP-404MK2 переведена с помощью ",
            {
                "tag": "a",
                "children": ["DeepL"],
                "attrs": {"href": "https://www.deepl.com/"},
            },
            " и отредактирована вручную. Исходный код и тексты в JSON ",
            {
                "tag": "a",
                "attrs": {"href": "https://github.com/sp404community/SP-404MK2-shortcuts"},
                "children": ["на GitHub"],
            },
            ". Для русскоязычного сообщества ",
            {
                "tag": "a",
                "attrs": {"href": "https://t.me/sp404community"},
                "children": ["@sp404community"],
            },
            " сделал ",
            {
                "tag": "a",
                "attrs": {"href": "https://t.me/sergiks"},
                "children": ["@sergiks"],
            },
            ". База знаний по линейке Roland SP-404: ",
            {
                "tag": "a",
                "attrs": {"href": "https://sp404.ru/"},
                "children": ["sp404.ru"],
            },
        ],
    }


def header(data, locale="Ru"):
    if locale == "Ru":
        return header_Ru(data)
    
def header_Ru(data):
    section_ids = list(
        map(
            lambda section: {
                "tag": "a",
                "attrs": {"href": f"#{section["Section"]}"},
                "children": [section["Section"]],
            },
            data,
        )
    )
    
    for i in range(len(section_ids) - 1, 0, -1):
        section_ids.insert(i, ", ")
        
    section_ids.insert(0, "Сочетания с кнопками: ")

    return [
        {
            "tag": "p",
            "children": [
                "Горячие клавиши сэмплера Roland SP-404MK2 с прошивкой версии ",
                {"tag": "code", "children": ["v.5.0.1"]},
            ],
        },
        {"tag": "p", "children": section_ids},
    ]
