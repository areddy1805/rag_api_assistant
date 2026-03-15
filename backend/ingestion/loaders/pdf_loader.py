from pypdf import PdfReader
from backend.ingestion.schema.document import Document


class PDFLoader:

    def load(self, path):

        reader = PdfReader(path)

        docs = []

        for i, page in enumerate(reader.pages):

            text = page.extract_text()

            if text:

                docs.append(
                    Document(
                        text=text,
                        page=i + 1,
                        source=path,
                        document_type="pdf"
                    )
                )

        return docs