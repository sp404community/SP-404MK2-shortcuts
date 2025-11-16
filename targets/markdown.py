import json
from .telegraph import fit_lines


def markdown_render(src_filename="translated.json", dst_filename="shortcuts.md", locale="Ru"):
    with open(src_filename, "r") as src_fp:
        sections = json.load(src_fp)
    
    content = [] # lines of Markdown file
    
    """Add the header"""
    content.extend(header(sections=sections, locale="Ru"))
    
    for section in sections:
        content.append(f"## {section["Section"]}")
        content.append(section[f"Title_{locale}"])

        length = len(section[locale][0])

        rows = []
        for row in section[locale]:
            if length == 3:
                if row[1] == "–":
                    rows.append(f"{row[0]}")
                    rows.append(f"    {row[2]}")
                    # rows.extend(fit_lines(row[2]))
                else:
                    rows.append(f"{row[0]}")
                    rows.append(f"    {row[1]}")
                    rows.append(f"    {row[2]}")
                    # rows.extend(fit_lines(row[2]))
            elif length == 2:
                rows.append(f"{row[0]}")
                rows.extend(fit_lines(row[1]))
            
            rows.append("")

        content.append("```")
        content.append("\n".join(rows))
        content.append("```")
        content.append("-----\n")
    
    """Add the footer"""
    content.extend(footer(sections=sections, locale="Ru"))

    """Save to file"""
    with open(dst_filename, "w") as dst_fp:
        dst_fp.write("\n".join(content))
        
    print(f"Markdown written to {dst_filename}")


def header(sections=[], locale="Ru"):
    if locale == "Ru":
        return _header_Ru(sections)
    
def _header_Ru(sections=[]):
    result = [
        "Горячие клавиши сэмплера Roland SP-404MK2 с прошивкой версии `v.5.0.1`\n",
    ]
    
    def section_anchor(section):
        title = section["Section"]
        id = title.lower().replace(' ', '-')
        return f"[{title}](#{id})"
    
    if len(sections) > 0:
        keys = ", ".join(map(section_anchor, sections))
        
        result.append(f"Сочетания с кнопками: {keys}\n")

    return result
    
def footer(sections=[], locale="Ru"):
    if locale == "Ru":
        return _footer_Ru(sections)

def _footer_Ru(sections):
    result = [
        "Информация из [официального мануала](https://www.roland.com/global/support/by_product/sp-404mk2/owners_manuals/)",
        "Roland для SP-404MK2 переведена с помощью ",
        "[DeepL](https://www.deepl.com/)",
        "и отредактирована вручную.",
        "",
        "Исходный код и тексты в JSON ",
        "[на GitHub](https://github.com/sp404community/SP-404MK2-shortcuts).",
        "",
        "Для русскоязычного сообщества ",
        "[@sp404community](https://t.me/sp404community)",
        " сделал [@sergiks](https://t.me/sergiks).",
        "",
        "База знаний по линейке Roland SP-404: [sp404.ru](https://sp404.ru/)",
    ]
    
    return result

