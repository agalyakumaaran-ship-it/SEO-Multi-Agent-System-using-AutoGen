
import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from tools.SEO_Web_Search import search_seo_information


async def main():

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"]
    )

    try:
        content_writer = AssistantAgent(
            name="SEO_Content_Writer",
            model_client=model_client,

            tools=[search_seo_information],

            reflect_on_tool_use=True,

            system_message="""
            You are an expert SEO Content Writer.

            Your responsibility is to create high-quality,
            SEO-friendly website content for Brickwork India.

            You must research the topic using the web search
            tool before writing content.

            Your writing responsibilities:

            1. Create SEO-friendly page titles.
            2. Write compelling meta descriptions.
            3. Create clear H1, H2 and H3 headings.
            4. Write informative blog articles.
            5. Naturally include relevant target keywords.
            6. Use clear calls to action.
            7. Write for business owners and decision-makers.

            Follow these SEO writing guidelines:

            - Avoid keyword stuffing.
            - Use natural, professional language.
            - Focus on user search intent.
            - Do not invent company facts or statistics.
            - Do not make unsupported claims.
            - Include source URLs wherever available.

            Structure your output as:

            - Content Topic
            - Target Audience
            - Primary and Secondary Keywords
            - SEO Page Title
            - Meta Description
            - H1 and H2 Headings
            - Draft Content
            - Call to Action
            """
        )

        await Console(
            content_writer.run_stream(
                task="""
                Create an SEO-friendly blog article for Brickwork India.

                Topic:
                Benefits of Virtual Assistant Services
                for Small and Medium-Sized Businesses.

                Target audience:
                Business owners, startup founders and executives.

                Include relevant keywords, an SEO title,
                meta description, headings, informative content
                and a suitable call to action.

                Use research to support the content.
                """
            )
        )

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
