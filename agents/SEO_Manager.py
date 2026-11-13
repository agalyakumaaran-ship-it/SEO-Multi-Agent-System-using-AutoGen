
import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from tools.SEO_Web_Search import search_seo_information
from tools.SEO_Website_Audit import audit_website


async def main():

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"]
    )

    try:
        seo_manager = AssistantAgent(
            name="SEO_Manager",
            model_client=model_client,

            tools=[
                search_seo_information,
                audit_website
            ],

            reflect_on_tool_use=True,

            system_message="""
            You are the SEO Manager responsible for coordinating
            the SEO strategy for Brickwork India.

            You must use the research and website audit tools
            before preparing your final recommendations.

            Review these five areas:

            1. SEO research and keyword opportunities.
            2. Technical SEO audit findings.
            3. Content gaps and content strategy.
            4. SEO-friendly content recommendations.
            5. Overall SEO priorities and implementation roadmap.

            Prepare a consolidated report with these sections:

            - Executive Summary
            - Business and SEO Overview
            - Keyword Strategy
            - Technical SEO Findings
            - Content Strategy
            - Content Recommendations
            - Priority Actions
            - 90-Day SEO Roadmap
            - Success Metrics

            Guidelines:

            - Separate verified findings from recommendations.
            - Do not invent keyword search volumes or rankings.
            - Do not invent website audit findings.
            - Do not claim that other agents were executed
              during this run.
            - Identify areas requiring further investigation.
            - Provide practical recommendations for Brickwork India.
            """
        )

        await Console(
            seo_manager.run_stream(
                task="""
                Prepare a consolidated SEO strategy report
                for Brickwork India.

                Website:
                https://www.brickworkindia.com/

                Use the website audit tool to inspect the website.
                Use web research to understand the company's
                services and SEO opportunities.

                Incorporate these previously generated specialist
                findings as preliminary inputs:

                SEO Researcher:
                Identified opportunities around virtual assistance,
                business support, outsourcing, digital marketing,
                executive support and research services.

                Technical SEO Auditor:
                Homepage returned HTTP 200, has a page title,
                meta description, one H1, nine H2 headings,
                40 images with no missing alt text, and 77
                internal links.

                Content Strategist:
                Suggested detailed service pages, case studies,
                educational blogs and industry-specific content.

                SEO Content Writer:
                Produced a draft article about the benefits
                of virtual assistant services for SMEs.

                Evaluate these findings and prepare an actionable
                consolidated SEO report with a 90-day roadmap.
                """
            )
        )

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
