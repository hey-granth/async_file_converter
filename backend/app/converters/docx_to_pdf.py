from pypandoc import convert_file


def convert(input_path: str, output_path: str) -> None:
    """
    Convert a DOCX file to PDF format.
    """
    try:
        convert_file(input_path, 'pdf', outputfile=output_path)

    except Exception as e:
        raise RuntimeError(f"Conversion failed: {e}")
