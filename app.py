from __future__ import annotations

import gradio as gr

from modules.test_suggester import suggest_tests


with gr.Blocks(title="dbt Test Suggester") as demo:
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


if __name__ == "__main__":
    demo.launch()
