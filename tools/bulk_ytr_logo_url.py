"""Replace legacy ytr-logo-reference.svg references with {{ ytr_logo_url }} (context processor)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPLACEMENTS = [
    ("{% static 'images/ytr-logo-reference.svg' %}", "{{ ytr_logo_url }}"),
    ('{% static "images/ytr-logo-reference.svg" %}', "{{ ytr_logo_url }}"),
    ("/static/images/ytr-logo-reference.svg", "{{ ytr_logo_url }}"),
]


def main():
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".html", ".htm"}:
            continue
        if "node_modules" in path.parts or "staticfiles" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for a, b in REPLACEMENTS:
            text = text.replace(a, b)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("updated", path.relative_to(ROOT))
    print("done")


if __name__ == "__main__":
    main()
