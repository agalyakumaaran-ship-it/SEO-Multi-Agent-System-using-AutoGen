
import streamlit as st
import asyncio
from agents.SEO_Team import main

st.set_page_config(
    page_title="SEO Multi-Agent Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Dashboard title
st.title("🚀 SEO Multi-Agent Control Centre")
st.caption("Manage and monitor your AutoGen SEO agents")

# Initialize agent status
if "seo_agent_running" not in st.session_state:
    st.session_state.seo_agent_running = False

st.divider()

# Start and Stop controls
st.subheader("Agent Controls")

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "▶️ START SEO AGENT",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.seo_agent_running
    ):
        st.session_state.seo_agent_running = True
        st.rerun()

with col2:
    if st.button(
        "⏹️ STOP SEO AGENT",
        type="secondary",
        use_container_width=True,
        disabled=not st.session_state.seo_agent_running
    ):
        st.session_state.seo_agent_running = False
        st.rerun()

# Display service status
st.subheader("Service Status")

if st.session_state.seo_agent_running:
    st.success("🟢 SEO Agent Service is RUNNING")
    st.write("Ready to accept website analysis requests.")
else:
    st.warning("🔴 SEO Agent Service is STOPPED")
    st.write("Press Start SEO Agent to activate the service.")

st.divider()

# Website input
st.subheader("Website Analysis")

website_url = st.text_input(
    "Enter Website URL",
    placeholder="https://www.example.com"
)

if st.button(
    "🚀 RUN SEO ANALYSIS",
    type="primary",
    use_container_width=True,
    disabled=not st.session_state.seo_agent_running
):
    if website_url.strip():

        with st.spinner("🤖 Your five SEO agents are working..."):

            try:
                final_report = asyncio.run(main(website_url))

                if final_report:
                    st.success("SEO analysis completed successfully!")

                    st.subheader("📊 Final SEO Report")
                    st.markdown(final_report)

                    st.download_button(
                        label="📥 Download SEO Report",
                        data=final_report,
                        file_name="SEO_Final_Report.md",
                        mime="text/markdown"
                    )
                else:
                    st.error("The SEO Manager did not generate a report.")

            except Exception as error:
                st.error(f"SEO analysis failed: {error}")

    else:
        st.error("Please enter a website URL.")


# Agent monitoring
st.subheader("Agent Monitoring")

agents = [
    "SEO Researcher",
    "Technical SEO Auditor",
    "Content Strategist",
    "SEO Content Writer",
    "SEO Manager"
]

for agent in agents:
    st.write(f"⏳ {agent} — Waiting for analysis")
