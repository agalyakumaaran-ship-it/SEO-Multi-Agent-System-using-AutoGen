
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
        seo_researcher = AssistantAgent(
            name="SEO_Researcher",
            model_client=model_client,

            tools=[search_seo_information],

            reflect_on_tool_use=True,

            system_message="""
            You are an expert SEO Researcher specialising in
            business support and outsourcing companies.

            You must use the web search tool to collect information
            before preparing your SEO research report.

            Research Brickwork India:
            https://www.brickworkindia.com/

            Your responsibilities:
            1. Research the company's services.
            2. Identify its target customers.
            3. Find primary and secondary SEO keywords.
            4. Analyse search intent.
            5. Identify competitor opportunities.
            6. Recommend SEO content opportunities.

            Do not invent keyword search volumes or rankings.
            Include source URLs wherever available.

            Present findings in clear sections and bullet points.
            """
        )

        await Console(
            seo_researcher.run_stream(
                task="""
                Conduct SEO research for Brickwork India.

                Search the web for its business support services,
                outsourcing services, target industries and
                relevant SEO keyword opportunities.

                Prepare an initial SEO research report.
                """
            )
        )

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
