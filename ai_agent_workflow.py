import os
from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, FileReadTool, DirectoryReadTool 
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("CRITICAL: OPENAI_API_KEY is missing. Check your .env file")

#initalize some tools for the agents
website_scrape_tool = ScrapeWebsiteTool()
file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool(directory="./match_stats")

# ==========================================
# Define the agents
# ==========================================

# Agent 1: CSV Data Gatherer
data_gatherer = Agent(
    role="data_gatherer",
    goal=(
        "Explore directories, list files, extract complete raw data from csv files, "
        "and reconstruct them into structured tables with readable column headings"
    ),
    backstory=(
        "You are an expert data wrangler. You use your directory reading tool to list "
        "the exact files inside the match_stats directory, and then use your file reading "
        "tool to open them. You reconstruct chaotic rows into organised tables, translating "
        "abbreviated column headers into readable strings."
    ),
    tools = [directory_read_tool, file_read_tool],
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
    verbose=True
)

# Agent 3: Performance Reporter
performance_reporter = Agent(
    role="Performance Intelligence Analyst",
    goal="Synthesize structured stats and match reports into a high-level performance summary text block for elite coaching staff.",
    backstory=(
        "You translate numbers, raw actions and match reports into rugby intelligence."
        "You highlight outstanding trajectories, potential red flags, and exceptional physical "
        "or tactical outputs, ensuring the summary is brief and ready for human-in-the-loop review."
        "You can infer perforamance from the qualitative match report, as well as producing derived metrics"
        " from the structured stats, e.g. metres per carry, tackles per minute, etc."
    ),
    verbose=True,
    memory=True
)


# ==========================================
# DEFINE THE SEQUENTIAL PIPELINE (THE TASKS)
# ==========================================

# Task 1: Compile the CSV data
task_transform = Task(
    description=(
        "1. First, use your directory reading tool to list all the file names inside the 'match_stats' folder. "
        "2. Identify the specific player and game statistics CSV files from that list. "
        "3. Use your file reading tool with the exact discovered file paths to pull the data. "
        "4. Compile a comprehensive set of player match performance statistics with fully readable column headings."
    ),
    expected_output="A clean, structured set of markdown tables that shows specific game data for the players involved in the match.",
    agent=data_gatherer
)

# Task 2: Scrape match report
task_scrape = Task(
    description=(
        "Scrape the match report or article from this URL: {match_url}. "
        "Extract all text relevant to individual player performances."
    ),
    expected_output="A raw text block containing the pulled webpage content about player performances.",
    agent=website_scraper
)

# Task 3: Summarize for Coaching Staff
task_report = Task(
    description=(
        "Using the structured metrics provided by the data gatherer, and the match report "
        "compiled by the sport article scraper, produce a 3-paragraph Talent Performance Summary. "
        "Focus on developmental trajectories, tactical impacts and actionable insights that a "
        "Head Coach would care about. Back up the reasoning by highlighting some key individual performance metrics."
        "Use derived metrics where appropriate, e.g. metres per carry,and ensure the summary is concise, professional,"
        " and ready for human-in-the-loop review."
    ),
    expected_output="A polished, professional markdown intelligence summary ready for a post-match review.",
    agent=performance_reporter,
    output_file="match_performance_report.md" 
)

# ==========================================
# ORCHESTRATE THE AGENTS
# ==========================================
rugby_agents_crew = Crew(
    agents=[data_gatherer, website_scraper, performance_reporter],
    tasks=[task_transform, task_scrape, task_report],
    process=Process.sequential, 
    verbose=True
)

if __name__ == "__main__":
    match_url = "https://www.bbc.co.uk/sport/rugby-union/articles/cwyg4xzpy41o" 
    print(f"### Kicking off multi-agent workflow for: {match_url} ###\n")
    
    result = rugby_agents_crew.kickoff(inputs={"match_url": match_url})
    
    print("\n### WORKFLOW COMPLETE! ###")
    print(result)
