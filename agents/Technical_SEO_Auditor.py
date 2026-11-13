
import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from tools.SEO_Website_Audit import audit_website


async def main():

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"]
    )

    try:
        technical_auditor = AssistantAgent(
            name="Technical_SEO_Auditor",
            model_client=model_client,

            tools=[audit_website],

            reflect_on_tool_use=True,

            system_message="""
            You are an expert Technical SEO Auditor.

            Your responsibility is to inspect Brickwork India's
            website and identify technical SEO improvements.

            You must use the website audit tool before making
            recommendations.

            Analyse:

            1. Page title and its relevance.
            2. Meta description quality.
            3. H1 and H2 heading structure.
            4. Missing image alt attributes.
            5. Internal linking opportunities.
            6. Website response status.
            7. Opportunities to improve page SEO.

            Provide findings in these sections:

            - Audit Summary
            - Issues Identified
            - SEO Recommendations
            - Priority Level (High, Medium, Low)

            Do not claim that an issue exists unless the audit
            data supports it.
            Clearly identify checks that were not performed.
            """
        )

        await Console(
            technical_auditor.run_stream(
                task="""
                Perform a technical SEO audit of:

                https://www.brickworkindia.com/

                Analyse the website audit results and prepare
                a structured technical SEO report.
                """
            )
        )

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
git status
