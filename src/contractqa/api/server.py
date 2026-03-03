from fastapi import FastAPI
import gradio as gr

from langserve import add_routes
from langchain_core.runnables import RunnableLambda

from contractqa.extract.extractor import extract_key_items
from contractqa.qa.answer import answer_question
from contractqa.ui.gradio_app import build_demo

app = FastAPI(title="Contract Risk Extractor (RAG)")

chat_runnable = RunnableLambda(lambda x: answer_question(x["question"], x.get("history", [])))
extract_runnable = RunnableLambda(lambda x: extract_key_items())

add_routes(app, chat_runnable, path="/api/chat")
add_routes(app, extract_runnable, path="/api/extract")

demo = build_demo()
app = gr.mount_gradio_app(app, demo, path="/")