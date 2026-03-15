from dataclasses import dataclass


@dataclass
class Document:

    text: str

    source: str

    page: int | None = None

    service_name: str | None = None

    endpoint: str | None = None

    http_method: str | None = None

    api_version: str | None = None

    section: str | None = None

    document_type: str | None = None