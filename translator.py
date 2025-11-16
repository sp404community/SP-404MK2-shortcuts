import deepl
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()  # reads variables from a .env file to acess via os.environ or os.getenv()

deepl_count = 0
deepl_length = 0

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

