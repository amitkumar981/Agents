import gradio as gr
from dotenv import load_dotenv
import asyncio
from main import ResearchManager

# Load env vars once
load_dotenv(override=True)

manager = ResearchManager()

async def run(query: str):
    """Async generator that streams status + final report"""
    async for chunk in manager.run(query):
        yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# 🔍 Deep Research Assistant")

    with gr.Row():
        query_textbox = gr.Textbox(
            label="What topic would you like to research?",
            placeholder="Enter your research question...",
            scale=4
        )
        run_button = gr.Button("Run", variant="primary", scale=1)

    status_box = gr.Textbox(
        label="Research Progress",
        interactive=False,
        lines=10,
        placeholder="Progress updates will appear here..."
    )

    report_box = gr.Markdown(
        label="Final Report",
        elem_id="final-report"
    )

    # Stream updates into the status box (not just final report)
    run_button.click(fn=run, inputs=query_textbox, outputs=status_box)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=status_box)

ui.launch(inbrowser=True)
