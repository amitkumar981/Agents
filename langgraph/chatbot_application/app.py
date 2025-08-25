import gradio as gr
import asyncio
import uuid
from node import Sidekick  # or from chatbot import Chatbot if renamed

# --- Core functions ---

async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick

async def process_message(sidekick_state, message, success_criteria, chat_history):
    # Ensure message history is in proper format
    if not chat_history:
        chat_history = []
    # Run superstep
    updated_history = await sidekick_state.run_superstep(
        message, success_criteria, chat_history
    )
    return updated_history, sidekick_state

async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return [], "", None, new_sidekick

def free_resources(sidekick_state):
    print("Cleaning up")
    try:
        if sidekick_state:
            sidekick_state.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")

# --- Gradio UI ---

with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Personal Co-Worker")
    
    sidekick_state = gr.State(delete_callback=free_resources)
    
    with gr.Row():
        chat_window = gr.Chatbot(label="Sidekick", height=300, type="messages")
    
    with gr.Group():
        with gr.Row():
            user_input = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria_input = gr.Textbox(show_label=False, placeholder="Success criteria")
    
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")
    
    # Load backend chatbot
    ui.load(setup, [], [sidekick_state])
    
    # Bind events
    user_input.submit(process_message, [sidekick_state, user_input, success_criteria_input, chat_window], [chat_window, sidekick_state])
    success_criteria_input.submit(process_message, [sidekick_state, user_input, success_criteria_input, chat_window], [chat_window, sidekick_state])
    go_button.click(process_message, [sidekick_state, user_input, success_criteria_input, chat_window], [chat_window, sidekick_state])
    reset_button.click(reset, [], [chat_window, user_input, success_criteria_input, sidekick_state])

ui.launch(inbrowser=True)
