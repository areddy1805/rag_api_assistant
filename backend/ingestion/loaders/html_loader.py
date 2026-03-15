from bs4 import BeautifulSoup
from backend.ingestion.schema.document import Document


class HTMLLoader:

    def load(self, path):

        with open(path) as f:
            soup = BeautifulSoup(f, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        text = " ".join(text.split())

        return [
            Document(
                text=text,
                source=path,
                document_type="html"
            )
        ]