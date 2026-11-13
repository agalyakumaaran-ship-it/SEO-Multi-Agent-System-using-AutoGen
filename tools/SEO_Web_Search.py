
from ddgs import DDGS


def search_seo_information(query: str) -> str:
    """
    Search the web for SEO research information.
    """

    try:
        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return "No search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
                Result {index}
                Title: {result.get('title', '')}
                URL: {result.get('href', '')}
                Summary: {result.get('body', '')}
                """
            )

        return "\n".join(formatted_results)

    except Exception as error:
        return f"Web search failed: {error}"
