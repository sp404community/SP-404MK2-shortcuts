:ru: Документация на русском языке: [README_RU](README_RU.md)

# Roland SP-404MK2 shortcuts

Parse PDF manual to extract shortcut info, translate, edit and publish as Telegra.ph page.

Resulting page example: https://telegra.ph/sp404-hotkeys-11-11 (in Russian).

## How it works

Official Roland [SP-404MK2 Manual](https://www.roland.com/global/support/by_product/sp-404mk2/owners_manuals/) PDF contains tables with all (?) keyboard shortcuts. Download fresh manual into the `/pdf` folder and verify the filename in `main.py` to match.

This script parses the PDF by [jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) Python module and saves texts as a JSON file `tables.json` by default.

Saved texts can be translated via [Deepl API](https://www.deepl.com/en/built-with-deepl) to most of the languages. Source texts and the translations are saved to a new JSON file, `bilingual.json` by default.
Register for DeepL free account to get an API key. You;ll need to attach a valid credit card once for verification. Free quota is more than enough to translate all the strings in the shortcut guide.

Please take some time to read through generated translations and manually edit some of the texts.

Finally, publish translated info from the edited JSON file (see `translated.json`) to a [Telegra.ph](https://telegra.ph/) page for a quick [Instant View](https://instantview.telegram.org/) in Telegram. Script uses [Telegra.ph API](https://telegra.ph/api) for the task.

## Settings
Provided `.env.example` contains the keys expected to be in production `.env` file:
- `DEEPL_API_KEY` - deepl.com API key to translate all strings (once).
- `PROXY` - HTTP proxy settings to access DeepL API from locations where their service is not available.
- `TELEGRAPH_TOKEN` - Telegra.ph account token to create and update the page
- `TELEGRAPH_PAGE_PATH` - Telegra.ph page path to edit. Page needs to be created beforehead.

## Development

DISCLAIMER. I pulled this off as a quick free evening project, so pardon the code quality. Also there was quite a time I last used Python, bare with me.

You are more than welcome to [contribute to the project](https://github.com/sp404community/SP-404MK2-shortcuts):
- refactor
- add support for multiple languages
- translate and publish more language translations of the shortcuts.

Looking forward to see your pull requests!
