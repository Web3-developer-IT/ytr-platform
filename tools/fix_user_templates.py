"""One-off: normalize user-provided HTML templates for Django (urls + static)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

REPLACEMENTS = [
    ('href="index.html"', 'href="{% url \'home\' %}"'),
    ('href="browse.html"', 'href="{% url \'browse\' %}"'),
    ('href="how-it-works.html"', 'href="{% url \'how_it_works\' %}"'),
    ('href="about.html"', 'href="{% url \'about\' %}"'),
    ('href="contact.html"', 'href="{% url \'contact\' %}"'),
    ('href="login.html"', 'href="{% url \'login\' %}"'),
    ('href="register.html"', 'href="{% url \'register\' %}"'),
    ('href="signup.html"', 'href="{% url \'register\' %}"'),
    ('href="list-your-car.html"', 'href="{% url \'add_listing\' %}"'),
    ('href="list-vehicle.html"', 'href="{% url \'add_listing\' %}"'),
    ('href="insurance.html"', 'href="{% url \'insurance\' %}"'),
    ('href="terms.html"', 'href="{% url \'terms\' %}"'),
    ('href="privacy.html"', 'href="{% url \'privacy\' %}"'),
    ('href="faq.html"', 'href="{% url \'faq\' %}"'),
    ('href="careers.html"', 'href="{% url \'careers\' %}"'),
    ('href="partners.html"', 'href="{% url \'partners\' %}"'),
    ('href="cookies.html"', 'href="{% url \'cookies\' %}"'),
    ('href="help.html"', 'href="{% url \'help_center\' %}"'),
    ('href="safety.html"', 'href="{% url \'trust_safety\' %}"'),
    ('href="trust-safety.html"', 'href="{% url \'trust_safety\' %}"'),
    ('href="feedback.html"', 'href="{% url \'feedback\' %}"'),
]


def ensure_load_static(text: str) -> str:
    if text.lstrip().startswith("{% load static %}"):
        return text
    return "{% load static %}\n" + text


def fix_about_static(text: str) -> str:
    text = text.replace('href="css/style.css"', 'href="{% static \'css/style.css\' %}"')
    text = text.replace('href="css/components.css"', 'href="{% static \'css/components.css\' %}"')
    text = text.replace('src="js/main.js"', 'src="{% static \'js/main.js\' %}"')
    # Missing local images → bundled logo
    text = text.replace(
        'href="./images/chatgpt-20image-20jan-2013-2c-202026-2c-2009-46-57-20am.png"',
        'href="{% static \'images/ytr-logo-reference.svg\' %}"',
    )
    text = text.replace(
        'src="./images/chatgpt-20image-20jan-2013-2c-202026-2c-2009-46-57-20am.png"',
        'src="{% static \'images/ytr-logo-reference.svg\' %}"',
    )
    return text


def fix_howitworks_favicon(text: str) -> str:
    text = text.replace(
        'href="./images/chatgpt-20image-20jan-2013-2c-202026-2c-2009-46-57-20am.png"',
        'href="{% static \'images/ytr-logo-reference.svg\' %}"',
    )
    return text


def inject_enterprise_shell(text: str, *, include_nav: bool, include_footer: bool) -> str:
    """Replace first custom navbar-ytr block (trust-safety) with shared nav + CSS."""
    if include_nav and "navbar-ytr" in text and "ytrE-nav" not in text[:2000]:
        nav_start = text.find('<nav class="navbar-ytr">')
        nav_end = text.find("</nav>", nav_start)
        if nav_start != -1 and nav_end != -1:
            nav_end += len("</nav>")
            inject = (
                '<link rel="stylesheet" href="{% static \'css/ytr-enterprise-nav.css\' %}">\n'
                '<link rel="stylesheet" href="{% static \'css/ytr-public-shell.css\' %}">\n'
                '<body class="ytr-public-body">\n'
                "{% include 'partials/ytr_enterprise_nav.html' %}\n"
            )
            # body opens after </head> — trust file has <body> then nav; strip duplicate <body> if we inject wrong
            text = text[:nav_start] + inject + text[nav_end:]
    if include_footer and '<footer class="footer">' in text:
        f_start = text.find('<footer class="footer">')
        f_end = text.rfind("</footer>")
        if f_start != -1 and f_end != -1:
            f_end += len("</footer>")
            text = text[:f_start] + "{% include 'partials/public_footer.html' %}\n" + text[f_end:]
    return text


def main():
    ts = (TEMPLATES / "user_trust_safety.html").read_text(encoding="utf-8")
    ts = ensure_load_static(ts)
    for a, b in REPLACEMENTS:
        ts = ts.replace(a, b)
    ts = ts.replace(
        'href="https://i.imgur.com/YfZxG7E.png"',
        'href="{% static \'images/ytr-logo-reference.svg\' %}"',
    )
    ts = inject_enterprise_shell(ts, include_nav=True, include_footer=True)
    # Remove stray double body tag if inject added body before nav while file had <body>
    ts = ts.replace("<body class=\"ytr-public-body\">\n<body>", "<body class=\"ytr-public-body\">")
    ts = ts.replace("<body>\n<body class=\"ytr-public-body\">", "<body class=\"ytr-public-body\">")
    (TEMPLATES / "user_trust_safety.html").write_text(ts, encoding="utf-8")

    hi = (TEMPLATES / "user_howitworks.html").read_text(encoding="utf-8")
    hi = ensure_load_static(hi)
    hi = fix_howitworks_favicon(hi)
    for a, b in REPLACEMENTS:
        hi = hi.replace(a, b)
    (TEMPLATES / "user_howitworks.html").write_text(hi, encoding="utf-8")

    ab = (TEMPLATES / "user_about.html").read_text(encoding="utf-8")
    ab = ensure_load_static(ab)
    ab = fix_about_static(ab)
    for a, b in REPLACEMENTS:
        ab = ab.replace(a, b)
    # Add enterprise nav CSS once after first bootstrap link if not present
    if "ytr-enterprise-nav.css" not in ab:
        ab = ab.replace(
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">',
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">\n'
            '    <link rel="stylesheet" href="{% static \'css/ytr-enterprise-nav.css\' %}">\n'
            '    <link rel="stylesheet" href="{% static \'css/ytr-public-shell.css\' %}">\n',
            1,
        )
    (TEMPLATES / "user_about.html").write_text(ab, encoding="utf-8")

    print("OK: user_trust_safety.html, user_howitworks.html, user_about.html")


if __name__ == "__main__":
    main()
