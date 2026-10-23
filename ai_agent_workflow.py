import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Verify the key is loaded safely without printing it
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("CRITICAL: OPENAI_API_KEY is missing. Check your .env file")

# Initialize the scraping tool
website_scrape_tool = ScrapeWebsiteTool()

# ==========================================
# Define the agents
# ==========================================

# Agent 1: CSV Data Gatherer
csv_data_gatherer = Agent(
    role="csv_data_gatherer",
    goal=(
        "Extract the complete, raw data from the csv files contained in the wales v italy folder"
        "inside the match_stats folder."
    ),
    backstory=(
        "You are an expert data wrangler. You take raw data from csv files and reconstruct them into"
        "organised tables. You use the glossary file to translate the abbreviated column headers into"
        "readable strings."
    )
    verbose=True
)

# Agent 2: Website Report Scraper
website_scraper = Agent(
    role="sport_article_text_scraper",
    goal="Extract raw match text, statistics, and commentary from targetted rugby URLs.",
    backstory=(
        "You are an expert data harvester. Your job is to extract raw text content from "
        "match reports and sports websites, ignoring unrelated HTML fluff like ads and navbars."
    ),
    tools=[website_scrape_tool],
    verbose=True,
    memory=True
)

# Agent 3: Performance Reporter
talent_reporter = Agent(
    role="Performance Intelligence Analyst",
    goal="Synthesize structured stats and match reports into a high-level performance summary text block for elite coaching staff.",
    backstory=(
        "You translate numbers, raw actions and match reports into rugby intelligence. You highlight outstanding "
        "trajectories, potential red flags, and exceptional physical or tactical outputs, ensuring "
        "the summary is brief and ready for human-in-the-loop review."
    ),
    verbose=True
)