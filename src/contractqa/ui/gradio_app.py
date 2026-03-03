import gradio as gr
from contractqa.indexing.ingest import ingest_contract
from contractqa.extract.extractor import extract_key_items
from contractqa.qa.answer import answer_question


def build_demo() -> gr.Blocks:
    with gr.Blocks() as demo:
        gr.Markdown("# Contract Risk & Obligation Extractor (RAG)\nNot legal advice.")

        ingested = gr.State(False)

        with gr.Tab("Upload & Extract"):
            file_in = gr.File(label="Upload PDF/DOCX", file_types=[".pdf", ".docx"])
            ingest_btn = gr.Button("Ingest (Index into Vector DB)")
            ingest_out = gr.JSON(label="Ingestion Result")

            extract_btn = gr.Button("Extract Obligations / Deadlines / Penalties")
            extract_out = gr.JSON(label="Extraction Output")

            def do_ingest(f):
                if f is None:
                    return {"error": "Upload a file first."}, False
                try:
                    info = ingest_contract(f.name)
                    return info, True
                except Exception as exc:
                    # print full traceback to terminal for debugging
                    import traceback
                    print("[ERROR] do_ingest exception:")
                    traceback.print_exc()
                    return {"error": str(exc)}, False

            ingest_btn.click(do_ingest, inputs=[file_in], outputs=[ingest_out, ingested])

            def do_extract(ok):
                if not ok:
                    return {"error": "Ingest a contract first."}
                return extract_key_items()

            extract_btn.click(do_extract, inputs=[ingested], outputs=[extract_out])

        with gr.Tab("Chat Q&A"):
            chatbot = gr.Chatbot(label="Ask about the uploaded contract")
            msg = gr.Textbox(label="Your question")
            send = gr.Button("Send")
            clear = gr.Button("Clear Chat")

            def respond(user_message, chat_history):
                reply = answer_question(user_message, chat_history)
                return "", chat_history + [(user_message, reply)]

            send.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
            msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
            clear.click(lambda: [], outputs=[chatbot])

    return demo