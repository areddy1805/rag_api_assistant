import yaml
from backend.ingestion.schema.document import Document


class OpenAPILoader:

    def load(self, path):

        with open(path) as f:
            spec = yaml.safe_load(f)

        docs = []

        paths = spec.get("paths", {})

        for endpoint, methods in paths.items():

            for method, data in methods.items():

                summary = data.get("summary", "")
                description = data.get("description", "")

                text = f"""
Endpoint: {endpoint}
Method: {method}

Summary:
{summary}

Description:
{description}
"""

                docs.append(
                    Document(
                        text=text,
                        source=path,
                        endpoint=endpoint,
                        http_method=method,
                        document_type="openapi"
                    )
                )

        return docs