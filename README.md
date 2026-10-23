# Rugby Stats

An experiment in using CrewAI agents to combine rugby match statistics with a match report and produce a coaching-focused performance summary.

## Repository contents

- `ai_agent_workflow.py` runs the main workflow. Three sequential agents read the local statistics, scrape a rugby article, and synthesize a three-paragraph performance report.
- `match_stats/` contains the input CSVs: attacking, defending, discipline, scoring, and a glossary of abbreviated column names.
- `match_performance_report.md` is the report output. The checked-in sample covers Wales' 31-17 win over Italy; running the workflow replaces its contents.
- `requirements.txt` lists the pinned Python dependencies.
- `sportradar_api_test.py` is a separate trial API request; it is not called by the CrewAI workflow.

## Reproduce the performance report

The main workflow uses the CSV files in `match_stats/` and the BBC article URL currently set in `ai_agent_workflow.py`. Run it from the repository root because the CSV directory is configured as the relative path `./match_stats`.

1. Use Python 3.12 and create/activate a virtual environment (Linux/macOS):

	```bash
	python3.12 -m venv .venv
	source .venv/bin/activate
	```

2. Install the pinned dependencies:

	```bash
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	```

3. Create a `.env` file in the repository root with an OpenAI API key:

	```dotenv
	OPENAI_API_KEY=your_openai_api_key
	```

	`ai_agent_workflow.py` loads this file with `python-dotenv` and stops with an error if `OPENAI_API_KEY` is missing. Keep the real key private; `.env` is ignored by Git. The model/API usage may incur charges.

4. Start the workflow from the repository root:

	```bash
	python ai_agent_workflow.py
	```

	The script prints CrewAI's verbose progress and final result, scrapes the article from its configured URL, and writes the generated summary to `match_performance_report.md`. The article must be reachable, and the CSVs should describe the same match. To analyze a different article, change `match_url` near the bottom of `ai_agent_workflow.py`; the URL is currently hard-coded rather than supplied as a command-line argument.

## Environment variables

| Variable | Used by | Required for | Purpose |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | `ai_agent_workflow.py` | Main report workflow | Authenticates model calls; loaded from `.env` in the repository root. |

