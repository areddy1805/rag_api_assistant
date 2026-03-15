from backend.ingestion.loaders.pdf_loader import PDFLoader
from backend.ingestion.loaders.markdown_loader import MarkdownLoader
from backend.ingestion.loaders.html_loader import HTMLLoader
from backend.ingestion.loaders.openapi_loader import OpenAPILoader


def get_loader(path):

    if path.endswith(".pdf"):

        return PDFLoader()

    if path.endswith(".md"):

        return MarkdownLoader()

    if path.endswith(".html"):

        return HTMLLoader()

    if path.endswith(".yaml") or path.endswith(".json"):

        return OpenAPILoader()

    raise ValueError("Unsupported file type")