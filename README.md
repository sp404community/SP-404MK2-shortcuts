# Roland SP-404MK2 shortcuts

Official Roland [SP-404MK2 Manual](https://www.roland.com/global/support/by_product/sp-404mk2/owners_manuals/) PDF contains a few tables with all (?) keyboard shortcuts.

This script parses the PDF and translates table entries via [Deepl API](https://www.deepl.com/en/built-with-deepl).

Parsing is done by [jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) Python module.

### Next

Publish translated info to a [Telegra.ph](https://telegra.ph/) page for a quick [Instant View](https://instantview.telegram.org/) access in Telegram. Use [Telegra.ph API](https://telegra.ph/api) for this task.

### Open source?
Source script is based on my previous experiment of parsing invoice PDFs using the . Code is far from clean, so I am not yet ready to make this project public.

### Settings
Provided `.env.example` contains the keys expected to be in `.env` file:
- `DEEPL_API_KEY` - deepl.com API key to translate all strings (once).
- `PROXY` - HTTP proxy settings to access DeepL API from locations where their service is not available.
- `TELEGRAPH_TOKEN` - Telegra.ph account token to create and update the page
- `TELEGRAPH_PAGE_PATH` - Telegra.ph page path to edit. Page needs to be created beforehead.
