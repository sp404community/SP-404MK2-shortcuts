(Ru) Документация на русском языке: [README_RU](README_RU.md)

# Roland SP-404MK2 shortcuts

Parse PDF manual to extract shortcut info, translate, edit and publish as Telegra.ph page.

## How it works

Official Roland [SP-404MK2 Manual](https://www.roland.com/global/support/by_product/sp-404mk2/owners_manuals/) PDF contains tables with all (?) keyboard shortcuts.

This script parses the PDF and translates table entries via [Deepl API](https://www.deepl.com/en/built-with-deepl).

Parsing is done by [jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) Python module.

Translation to any language using DeepL API. Currently was only translated to Russian. Please join to refactor the code and allow easy extending to more languages. Register with DeepL free account to get an API key. Free quota is more than enought to translate all the strings in the shortcut guide.

Publish translated info to a [Telegra.ph](https://telegra.ph/) page for a quick [Instant View](https://instantview.telegram.org/) in Telegram. Script uses [Telegra.ph API](https://telegra.ph/api) for the task.

## Settings
Provided `.env.example` contains the keys expected to be in production `.env` file:
- `DEEPL_API_KEY` - deepl.com API key to translate all strings (once).
- `PROXY` - HTTP proxy settings to access DeepL API from locations where their service is not available.
- `TELEGRAPH_TOKEN` - Telegra.ph account token to create and update the page
- `TELEGRAPH_PAGE_PATH` - Telegra.ph page path to edit. Page needs to be created beforehead.

## Development

I pulled this off as a quick free evening project, so pardon the code quality. Also there was quite a time I last used Python, so bare with me.

You are more than welcome to contribute to the project:
- refactor
- add support for multiple languages
- translate and publish more language translations of the shortcuts.

