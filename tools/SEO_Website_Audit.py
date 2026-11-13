
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def audit_website(url: str) -> str:
    """
    Inspect a website page for basic technical SEO issues.
    """

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # Page title
        title = soup.title.string.strip() if soup.title and soup.title.string else "Missing"

        # Meta description
        meta = soup.find("meta", attrs={"name": "description"})
        description = meta.get("content", "").strip() if meta else "Missing"

        # Canonical URL
        canonical_tag = soup.find(
            "link",
            attrs={"rel": lambda value: value and "canonical" in value}
        )

        canonical_url = (
            urljoin(url, canonical_tag.get("href", ""))
            if canonical_tag and canonical_tag.get("href")
            else "Missing"
        )

        # Headings
        h1_tags = [
    tag.get_text(" ", strip=True)
    for tag in soup.find_all("h1")
]

        h2_tags = [
    tag.get_text(" ", strip=True)
    for tag in soup.find_all("h2")
]

        # Images without alt text
        images = soup.find_all("img")
        missing_alt = [
            img.get("src", "Unknown image")
            for img in images
            if not img.get("alt", "").strip()
        ]

        # Internal and external links
        internal_links = []
        external_links = []

        domain = urlparse(url).netloc

        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            link_domain = urlparse(full_url).netloc

            if link_domain == domain:
                internal_links.append(full_url)
            elif link_domain:
                external_links.append(full_url)

        report = f"""
TECHNICAL SEO AUDIT

Website: {url}
HTTP Status: {response.status_code}

PAGE TITLE:
{title}

META DESCRIPTION:
{description}

CANONICAL URL:
{canonical_url}

H1 HEADINGS:
{h1_tags}

H2 HEADINGS:
{h2_tags}

TOTAL IMAGES:
{len(images)}

IMAGES MISSING ALT TEXT:
{missing_alt}

INTERNAL LINKS: {len(internal_links)}
EXTERNAL LINKS: {len(external_links)}

SAMPLE INTERNAL LINKS:
{internal_links[:10]}
"""

        return report

    except requests.RequestException as error:
        return f"Website audit failed: {error}"
