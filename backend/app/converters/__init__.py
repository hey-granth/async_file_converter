from . import docx_to_pdf

# supported conversion mappings
CONVERTER_MAP = {
    ("docx", "pdf"): docx_to_pdf.convert,
}

def get_converter(input_ext: str, output_ext: str):
    return CONVERTER_MAP.get((input_ext.lower(), output_ext.lower()))
