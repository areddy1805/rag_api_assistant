import markdown
from backend.ingestion.schema.document import Document


class MarkdownLoader:

    def load(self, path):

        with open(path) as f:

            text = f.read()

        html = markdown.markdown(text)

        return [
            Document(
                text=html,
                source=path,
                document_type="markdown"
            )
        ]