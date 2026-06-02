# dbt-lab

dbt-lab is an open-source Gradio toolkit for data engineers to learn and build with dbt faster using AI assistance.

## Features

- **dbt Model Generator** (implemented): paste raw SQL and generate:
  - dbt `model.sql`
  - `schema.yml` with docs and tests
  - `sources.yml` when raw sources are detected
- **dbt Test Suggester** (roadmap)
- **Jinja Explainer** (roadmap)
- **SQL Refactor Tool** (roadmap)

## Tech Stack

- Python 3.10+
- Gradio
- Anthropic Claude API
- dbt-core
- pandas

## Project Structure

```text
dbt-lab/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── modules/
│   ├── __init__.py
│   ├── model_generator.py
│   ├── test_suggester.py
│   ├── jinja_explainer.py
│   └── sql_refactor.py
├── prompts/
│   ├── model_generator.txt
│   ├── test_suggester.txt
│   ├── jinja_explainer.txt
│   └── sql_refactor.txt
└── utils/
    ├── __init__.py
    └── llm_client.py
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your Anthropic key:
   ```bash
   cp .env.example .env
   ```
4. Run the app:
   ```bash
   python app.py
   ```

## Usage

1. Open the dbt Model Generator tab.
2. Paste raw SQL.
3. Click **Generate dbt Artifacts**.
4. Copy generated `model.sql`, `schema.yml`, and `sources.yml` into your dbt project.

## Features Roadmap

- [x] Scaffold project and implement Model Generator
- [ ] Implement dbt Test Suggester with schema test block output
- [ ] Implement Jinja Explainer with line-by-line explanation and gotchas
- [ ] Implement SQL Refactor Tool with staging vs marts guidance
- [ ] Add dbt project-aware context and validation helpers
