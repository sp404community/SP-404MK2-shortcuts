import json
from .telegraph import fit_lines


def markdown_render(src_filename="translated.json", dst_filename="shortcuts.md", locale="Ru"):
    with open(src_filename, "r") as src_fp:
        data = json.load(src_fp)
    
    content = [] # lines of Markdown file
    
    # TODO: add header string
    
    for section in data:
        content.append(f"#### {section["Section"]}")
        content.append(section[f"Title_{locale}"])

        length = len(section[locale][0])

        rows = []
        for row in section[locale]:
            rows.append("")
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

        content.append("\n```")
        content.append("\n".join(rows))
        content.append("```")
        content.append("-----\n")
    

    with open(dst_filename, "w") as dst_fp:
        dst_fp.write("\n".join(content))
        
    print(f"Markdown written to {dst_filename}")

