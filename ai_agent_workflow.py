import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

# Load the environment variables from the hidden .env file
load_dotenv()

# Verify the key is loaded safely without printing the whole key
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("CRITICAL: OPENAI_API_KEY is missing. Check your .env file!")

# Initialize the scraping tool
scrape_tool = ScrapeWebsiteTool()