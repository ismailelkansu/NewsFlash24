from config import TRUSTED_SOURCES

def is_trusted_source(source_url: str, source_name: str) -> bool:
    combined = (source_url + source_name).lower()
    return any(trusted in combined for trusted in TRUSTED_SOURCES)
