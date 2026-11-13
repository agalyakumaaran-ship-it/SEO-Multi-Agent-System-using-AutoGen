
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
        content_strategist = AssistantAgent(
            name="Content_Strategist",
            model_client=model_client,

            tools=[search_seo_information],

            reflect_on_tool_use=True,

            system_message="""
            You are an expert SEO Content Strategist.

            Your responsibility is to develop an SEO content
            strategy for Brickwork India.

            You must use the web search tool before making
            content recommendations.

            Analyse:

            1. Existing content opportunities.
            2. Potential content gaps.
            3. Blog topic opportunities.
            4. Service-page improvement opportunities.
            5. Target keywords for each content idea.
            6. Search intent and target audience.
            7. Content priorities.

            Prepare your report using these sections:

            - Content Strategy Summary
            - Identified Content Gaps
            - Recommended Blog Topics
            - Service Page Improvements
            - Target Keywords and Search Intent
            - Content Roadmap

            Do not invent search volumes or keyword rankings.
            Clearly distinguish research findings from suggestions.
            Include source URLs wherever available.
            """
        )

        await Console(
            content_strategist.run_stream(
                task="""
                Develop an SEO content strategy for:

                Brickwork India
                https://www.brickworkindia.com/

                Research its business support, virtual assistant,
                outsourcing, finance, HR, IT and research services.

                Identify content opportunities that can help
                attract relevant business customers.

                Prepare a structured content strategy report.
                """
            )
        )

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
