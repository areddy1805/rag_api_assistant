import markdown
from backend.ingestion.schema.document import Document


class MarkdownLoader:

    def load(self, path):

        with open(path) as f:

            text = f.read()

        html = markdown.markdown(text)
        service = "kubernetes"
        return [
            Document(
                text=html,
                source=path,
                service_name=service,
                document_type="markdown"
            )
        ]