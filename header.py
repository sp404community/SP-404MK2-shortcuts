def header(data, locale="Ru"):
    if locale == "Ru":
        return _Ru(data)
    
def _Ru(data):
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
