
import asyncio
import os
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

from tools.SEO_Web_Search import search_seo_information
from tools.SEO_Website_Audit import audit_website


async def main():

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
            system_message="""
            Research Brickwork India's services, target customers,
            SEO keywords, search intent and competitors.
            Use the web search tool.
            Do not invent search volumes or rankings.
            Share your findings clearly.
            """
        )

        # Agent 2: Technical SEO Auditor
        auditor = AssistantAgent(
            name="Technical_SEO_Auditor",
            model_client=model_client,
            tools=[audit_website],
            reflect_on_tool_use=True,
            system_message="""
Audit https://www.brickworkindia.com/
using the website audit tool.

Analyse:
1. HTTP status
2. Page title
3. Meta description
4. Canonical URL
5. H1 and H2 headings
6. Images and missing alt text
7. Internal and external links

Include the actual audit results in your findings.

For the canonical URL, explicitly report:
- Whether it is present or missing.
- The exact canonical URL returned by the audit tool.

Separate verified findings from recommendations.
Do not claim checks were performed if the tool
does not provide the relevant data.
"""
        )

        # Agent 3: Content Strategist
        strategist = AssistantAgent(
            name="Content_Strategist",
            model_client=model_client,
            tools=[search_seo_information],
            reflect_on_tool_use=True,
            system_message="""
            Develop a content strategy for Brickwork India.
            Identify content gaps, blog opportunities,
            service-page improvements and target audiences.
            Use web research and share your findings.
            """
        )

        # Agent 4: SEO Content Writer
        writer = AssistantAgent(
            name="SEO_Content_Writer",
            model_client=model_client,
            tools=[search_seo_information],
            reflect_on_tool_use=True,
            system_message="""
            Create an SEO-friendly blog article for Brickwork India.
            Use the research and strategy shared by previous agents.
            Include SEO title, meta description, keywords,
            headings, article content and a call to action.
            Do not invent facts or statistics.
            """
        )
       
        # Agent 5: SEO Manager
        manager = AssistantAgent(
            name="SEO_Manager",
            model_client=model_client,
            system_message="""
            You are a senior SEO Manager responsible for producing
            an evidence-based SEO report for Brickwork India.

            Website: https://www.brickworkindia.com/

            Review all findings shared by the four specialist agents.

            Prepare the final SEO report with these sections:

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
            - Never use phrases such as "lack of content",
              "missing content" or "identified gaps" unless
              the relevant pages have been inspected.
            - Use the heading "Potential Content Opportunities"
              for suggestions that have not been verified.
            - Recommend current and evergreen blog topics.
            - Every statement about an existing website
              content gap must be supported by an observed
              page or audit result.
            - If evidence is unavailable, use wording such as
              "Potential opportunity to explore" rather than
              "needs", "lacks", "missing" or "requires".
            - Do not infer the condition of the entire blog
              or website from a homepage-only audit.
              Do not suggest outdated year-specific topics.
            - Do not claim backlinks or mobile optimization
              have been audited unless the tools checked them.
              Present these only as future audit recommendations.
            - Label keywords as "Proposed Target Keywords"
              unless actual keyword metrics are available.
            - Never describe keywords as high-volume,
              high-competition or high-value without
              verified keyword data.
            - Clearly distinguish keyword suggestions
              from validated keyword research.
            - Separate verified findings from recommendations.
            - Use actual audit results wherever available.
            - Include the exact canonical URL returned by the
              Technical SEO Auditor. Do not just say it is present
              or properly implemented.
            - Include the exact H1 and H2 headings returned by
              the Technical SEO Auditor. Do not replace them with
              generic summaries.
            - Never invent website traffic, keyword rankings,
              search volumes, conversion rates or statistics.
            - Do not claim a keyword has high search volume
              unless supported by actual keyword data.
            - Do not claim content is missing unless the
              website content has been checked.
            - Clearly mention when only the homepage was audited.
            - Do not claim that page speed, mobile usability,
              backlinks, schema or indexing were tested
              unless the tools actually checked them.
            - Explain why each recommendation is important.
            - Link every technical recommendation to an
              observed finding wherever possible.
            - Mark unverified opportunities as hypotheses.
            - Identify missing data required for further analysis.
            - Do not describe content as missing unless
              the relevant website pages have been checked.
            - Label unverified content gaps as
              "Potential Content Opportunities".
            - Do not claim testimonials, case studies,
              FAQs or industry insights are absent based
              only on the homepage audit.

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
            task="""
            Conduct a complete SEO analysis of Brickwork India.

            Website: https://www.brickworkindia.com/

            Each specialist agent must complete its assigned task
            and share its findings with the team.

            The SEO Manager must prepare the final consolidated
            SEO strategy after reviewing the previous agents'
            findings.
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
            print("\nSEO Manager did not produce a final text report.")

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
