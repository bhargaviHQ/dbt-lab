"""Main Gradio app entry point for dbt-lab."""

from __future__ import annotations

import gradio as gr
from dotenv import load_dotenv

from modules.model_generator import generate_model_artifacts
from modules.test_suggester import suggest_tests


load_dotenv()


def run_model_generator(raw_sql: str) -> tuple[str, str, str]:
    """Generate dbt model artifacts from user SQL input."""
    result = generate_model_artifacts(raw_sql)
    return result["model_sql"], result["schema_yml"], result["sources_yml"]


def not_implemented(_: str) -> str:
    """Return a placeholder message for upcoming features."""
    return "This feature is coming soon in the next iteration."


with gr.Blocks(title="dbt-lab") as demo:
    gr.Markdown("# dbt-lab\nAI toolkit for learning and building with dbt faster.")

    with gr.Tabs():
        with gr.Tab("dbt Model Generator"):
            sql_input = gr.Textbox(
                label="Paste raw SQL",
                lines=14,
                placeholder="SELECT * FROM raw.orders ...",
            )
            run_btn = gr.Button("Generate dbt Artifacts")
            model_sql_output = gr.Code(label="model.sql", language="sql")
            schema_yml_output = gr.Code(label="schema.yml", language="yaml")
            sources_yml_output = gr.Code(label="sources.yml", language="yaml")
            run_btn.click(
                fn=run_model_generator,
                inputs=[sql_input],
                outputs=[model_sql_output, schema_yml_output, sources_yml_output],
            )

        with gr.Tab("dbt Test Suggester"):
            gr.Markdown("Paste a dbt model SQL query to generate a ready-to-paste schema.yml test block.")
            model_sql_input = gr.Code(
                label="Paste your dbt model SQL",
                language="sql",
                lines=14,
            )
            suggested_tests_output = gr.Code(
                label="Suggested dbt Tests (schema.yml)",
                language="yaml",
                lines=18,
            )
            with gr.Row():
                suggest_btn = gr.Button("Suggest Tests", variant="primary")
                clear_btn = gr.Button("Clear")

            suggest_btn.click(fn=suggest_tests, inputs=model_sql_input, outputs=suggested_tests_output)
            clear_btn.click(fn=lambda: ("", ""), inputs=None, outputs=[model_sql_input, suggested_tests_output])

        with gr.Tab("Jinja Explainer"):
            jinja_input = gr.Textbox(label="Paste Jinja or macro code", lines=12)
            jinja_btn = gr.Button("Explain Jinja")
            jinja_output = gr.Textbox(label="Explanation", lines=10)
            jinja_btn.click(fn=not_implemented, inputs=[jinja_input], outputs=[jinja_output])

        with gr.Tab("SQL Refactor Tool"):
            refactor_input = gr.Textbox(label="Paste SQL", lines=12)
            refactor_btn = gr.Button("Refactor SQL")
            refactor_output = gr.Textbox(label="Refactored SQL", lines=10)
            refactor_btn.click(fn=not_implemented, inputs=[refactor_input], outputs=[refactor_output])


if __name__ == "__main__":
    demo.launch()
