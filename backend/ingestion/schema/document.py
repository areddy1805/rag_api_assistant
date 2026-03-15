from dataclasses import dataclass
from typing import Optional


@dataclass
class Document:

    text: str
    source: str

    page: Optional[int] = None

    service_name: Optional[str] = None
    endpoint: Optional[str] = None
    http_method: Optional[str] = None
    document_type: Optional[str] = None