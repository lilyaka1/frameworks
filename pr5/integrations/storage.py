"""JSON export for the Django implementation."""

import json
from pathlib import Path

from .services import serialize_integrations, serialize_requests


def save_json(filename, data):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export_data(directory):
    directory = Path(directory)
    save_json(directory / "integrations.json", serialize_integrations())
    save_json(directory / "api_requests.json", serialize_requests())