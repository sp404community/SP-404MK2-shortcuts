import json
import os
import pdfplumber


def read_to_json(
    pdf_filename="pdf/SP-404MK2_v5_reference_eng03_W.pdf",
    json_filename="tables.json",
    page_numbers=[144,145,146,147,148]
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
        for page_index in page_numbers:
            page = pdf.pages[page_index]
            tables.extend(page.extract_tables())

    with open(json_filename, "w") as output:
        json.dump(tables, output, ensure_ascii=False, indent=2)


