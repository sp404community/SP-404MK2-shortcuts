from datetime import datetime

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
