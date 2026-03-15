import json
import os

from backend.ingestion.schema.document import Document


class OpenAPILoader:

    def load(self, path):

        with open(path) as f:
            spec = json.load(f)

        docs = []

        service = os.path.basename(path).split("_")[0]

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
                        text=text.strip(),
                        source=path,
                        endpoint=endpoint,
                        http_method=method.upper(),
                        service_name=service,
                        document_type="openapi"
                    )
                )

        return docs