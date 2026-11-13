
import asyncio
import os
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

from tools.SEO_Web_Search import search_seo_information
from tools.SEO_Website_Audit import audit_website


async def main(website_url="https://www.brickworkindia.com/"):

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"]
    )

    try:

        # Agent 1: SEO Researcher
        researcher = AssistantAgent(
            name="SEO_Researcher",
            model_client=model_client,
            tools=[search_seo_information],
            reflect_on_tool_use=True,
            system_message=f"""
            You are an SEO Research Specialist.

            Research the following website:
            {website_url}

            Research:
            1. Services and target customers
            2. Proposed SEO keywords
            3. Search intent
            4. Relevant competitors
            5. Industry search trends

            Use the web search tool.
            Do not invent search volumes, rankings or statistics.
            Clearly separate verified findings from suggestions.
            Share your findings with the SEO team.
            """
        )

        # Agent 2: Technical SEO Auditor
        auditor = AssistantAgent(
            name="Technical_SEO_Auditor",
            model_client=model_client,
            tools=[audit_website],
            reflect_on_tool_use=True,
            system_message=f"""
            You are a Technical SEO Auditor.

            Audit this website:
            {website_url}

            Use the website audit tool.

            Analyse:
            1. HTTP status
            2. Page title
            3. Meta description
            4. Canonical URL
            5. H1 and H2 headings
            6. Images and missing alt text
            7. Internal and external links

            Include actual audit results in your findings.

            Explicitly report:
            - Whether the canonical URL is present or missing.
            - The exact canonical URL returned by the audit.
            - The actual H1 and H2 headings.

            This tool performs a homepage-level audit only.
            Do not claim that the entire website was audited.
            Do not claim that page speed, mobile usability,
            backlinks, schema or indexing were checked.

            Separate verified findings from recommendations.
            Share your findings with the SEO team.
            """
        )

        # Agent 3: Content Strategist
        strategist = AssistantAgent(
            name="Content_Strategist",
            model_client=model_client,
            tools=[search_seo_information],
            reflect_on_tool_use=True,
            system_message=f"""
            You are an SEO Content Strategist.

            Develop a content strategy for:
            {website_url}

            Research:
            1. Potential content opportunities
            2. Blog topic suggestions
            3. Service-page improvement opportunities
            4. Target audiences
            5. Search intent

            Use web research and share your findings.

            Do not claim that content is missing unless
            the relevant pages have actually been inspected.

            Clearly distinguish verified findings from hypotheses.
            """
        )

        # Agent 4: SEO Content Writer
        writer = AssistantAgent(
            name="SEO_Content_Writer",
            model_client=model_client,
            tools=[search_seo_information],
            reflect_on_tool_use=True,
            system_message=f"""
            You are an SEO Content Writer.

            Create an SEO-friendly blog article for:
            {website_url}

            Use the research and strategy shared by previous agents.

            Include:
            1. SEO title
            2. Meta description
            3. Proposed target keywords
            4. H1 and H2 headings
            5. Article content
            6. Call to action

            Do not invent facts, statistics or company information.
            Share your article with the SEO team.
            """
        )

        # Agent 5: SEO Manager
        manager = AssistantAgent(
            name="SEO_Manager",
            model_client=model_client,
            system_message=f"""
            You are a Senior SEO Manager.

            Prepare an evidence-based SEO report for:
            {website_url}

            Review all findings shared by the four specialist agents.

            Prepare the final report with these sections:

            1. Executive Summary
            2. Keyword Strategy
            3. Technical SEO Findings
            4. Content Strategy
            5. Content Recommendations
            6. Priority Actions
            7. 90-Day SEO Roadmap
            8. Success Metrics
            9. Missing Information and Limitations

            IMPORTANT REPORTING RULES:

            - The homepage audit does not establish whether
              content is missing across the full website.
            - Never claim content is missing unless the
              relevant pages have been inspected.
            - Use "Potential Content Opportunities" for
              suggestions that have not been verified.
            - Recommend current and evergreen blog topics.
            - Do not infer the condition of the entire website
              from a homepage-only audit.
            - Do not claim backlinks or mobile optimization
              have been audited unless the tools checked them.
            - Label keywords as "Proposed Target Keywords"
              unless actual keyword metrics are available.
            - Never invent search volumes, rankings, traffic,
              conversion rates or statistics.
            - Include the exact canonical URL returned by
              the Technical SEO Auditor.
            - Include the actual H1 and H2 headings.
            - Clearly mention that only the homepage was audited.
            - Do not claim page speed, mobile usability,
              schema or indexing were tested.
            - Explain why each recommendation is important.
            - Link technical recommendations to observed findings.
            - Clearly identify missing data required for
              further analysis.
            - Separate verified findings from recommendations.

            Use professional business-report formatting.
            Produce a practical and prioritized SEO strategy.
            """
        )

        # Create the five-agent team
        seo_team = RoundRobinGroupChat(
            participants=[
                researcher,
                auditor,
                strategist,
                writer,
                manager
            ],
            max_turns=5
        )

        # Start the coordinated SEO workflow
        result = await seo_team.run(
            task=f"""
            Conduct an SEO analysis of the following website:

            Website: {website_url}

            Each specialist agent must complete its assigned task
            and share its findings with the team.

            The SEO Manager must prepare the final consolidated
            SEO strategy after reviewing the previous agents'
            findings.

            Use only verified information and clearly identify
            limitations in the available research.
            """
        )

        # Get the SEO Manager's final response
        final_report = ""

        for message in reversed(result.messages):

            if message.source == "SEO_Manager":

                if isinstance(message.content, str):
                    final_report = message.content
                    break

        # Save the final report
        if final_report:

            report_folder = Path("reports")
            report_folder.mkdir(parents=True, exist_ok=True)

            report_path = report_folder / "SEO_Final_Report.md"

            report_path.write_text(
                final_report,
                encoding="utf-8"
            )

            print(
                f"\nSEO report saved successfully: {report_path}"
            )

        else:
            print(
                "\nSEO Manager did not produce a final text report."
            )

        # Return report to Streamlit
        return final_report

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
