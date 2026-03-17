from pypdf import PdfReader
import nltk
from tqdm import tqdm
import tiktoken


def load_doc(path):

    reader = PdfReader(path)

    pages = []

    for page_num, page in enumerate(tqdm(reader.pages, desc="Reading PDF pages")):

        content = page.extract_text()

        if content:
            content = content.replace("PAGE", "")
            pages.append({
                "text": content,
                "page": page_num + 1,
                "source": path
            })

    return pages

def build_parent_child_chunks(
    pages,
    parent_tokens=1000,
    child_tokens=300,
    overlap=80
):

    enc = tiktoken.get_encoding("cl100k_base")

    parents = []
    children = []

    parent_buffer = []
    parent_token_count = 0

    parent_id = 0
    chunk_id = 0

    # flatten document sentences across pages
    sentences = []

    for page in pages:

        sents = nltk.sent_tokenize(page["text"])

        for s in sents:
            sentences.append((s, page))

    for sentence, page in tqdm(sentences, desc="Building chunks"):

        token_len = len(enc.encode(sentence))

        if parent_token_count + token_len > parent_tokens:

            parent_text = " ".join(parent_buffer)

            parents.append({
                "parent_id": parent_id,
                "text": parent_text,
                "page": page["page"],
                "source": page["source"]
            })

            child_sentences = nltk.sent_tokenize(parent_text)

            current_chunk = []
            token_count = 0

            for s in child_sentences:

                t_len = len(enc.encode(s))

                if token_count + t_len > child_tokens:

                    chunk_text = " ".join(current_chunk)

                    children.append({
                        "chunk_id": chunk_id,
                        "parent_id": parent_id,
                        "text": chunk_text,
                        "page": page["page"],
                        "source": page["source"]
                    })

                    chunk_id += 1

                    overlap_tokens = chunk_text.split()[-overlap:]

                    current_chunk = [" ".join(overlap_tokens)]
                    token_count = len(overlap_tokens)

                current_chunk.append(s)
                token_count += t_len

            if current_chunk:

                children.append({
                    "chunk_id": chunk_id,
                    "parent_id": parent_id,
                    "text": " ".join(current_chunk),
                    "page": page["page"],
                    "source": page["source"]
                })

                chunk_id += 1

            parent_id += 1
            parent_buffer = []
            parent_token_count = 0

        parent_buffer.append(sentence)
        parent_token_count += token_len

    # final flush
    if parent_buffer:

        parent_text = " ".join(parent_buffer)

        parents.append({
            "parent_id": parent_id,
            "text": parent_text,
            "page": pages[-1]["page"],
            "source": pages[-1]["source"]
        })

        child_sentences = nltk.sent_tokenize(parent_text)

        current_chunk = []
        token_count = 0

        for s in child_sentences:

            t_len = len(enc.encode(s))

            if token_count + t_len > child_tokens:

                chunk_text = " ".join(current_chunk)

                children.append({
                    "chunk_id": chunk_id,
                    "parent_id": parent_id,
                    "text": chunk_text,
                    "page": pages[-1]["page"],
                    "source": pages[-1]["source"]
                })

                chunk_id += 1

                overlap_tokens = chunk_text.split()[-overlap:]

                current_chunk = [" ".join(overlap_tokens)]
                token_count = len(overlap_tokens)

            current_chunk.append(s)
            token_count += t_len

        if current_chunk:

            children.append({
                "chunk_id": chunk_id,
                "parent_id": parent_id,
                "text": " ".join(current_chunk),
                "page": pages[-1]["page"],
                "source": pages[-1]["source"]
            })

            chunk_id += 1

    return parents, children
