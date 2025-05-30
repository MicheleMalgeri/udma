import os
import tempfile
import threading

import gradio as gr

from pkg.lib.utils import create_test_user
from src.server.adapter.ai.llama.iteration_state import IterationState
from src.server.config.config import ApplicationConfig


class GradioInterface:
    welcome_message = None
    chat_history = []
    unknown_response = None

    def __init__(self, user=None):
        if user is None:
            user = create_test_user()
        self.user = user
        self.iteration_state = IterationState.get_instance(user)
        self.welcome_message = (
            "Ciao! Sono qui per aiutarti a recuperare la tua cartella clinica in modo semplice "
            "e veloce attraverso alcune domande mirate. Quando vuoi, possiamo iniziare!"
        )
        self.chat_history.append({"role": "assistant", "content": self.welcome_message})
        self.unknown_response = ApplicationConfig.get_instance().get_unknown_response()
        self.launch = None
        self.timeout_timer = None
        self.chat_interface = None
        self.inactivity_timeout = ApplicationConfig.get_instance().get_inactivity_timeout()

    def start_chat(self, chat_history, state):
        self.reset_inactivity_timer()
        result = self.iteration_state.evaluate_medical_records_length()
        if result is not None:
            message, files = result
            if "Termine: nessun record trovato." in message:
                chat_history.append({
                    "role": "assistant",
                    "content": "Non sono riuscito a trovare nessuna cartella clinica riferita a questo codice fiscale."
                })
                new_state = {"active": False}
                return (
                    chat_history,
                    new_state,
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=False)
                )
            elif "Termine: cartella clinica trovata!" in message:
                chat_history.append({
                    "role": "assistant",
                    "content": "Ho trovato una cartella clinica!"
                })
                new_state = {"active": True}
                tmp_paths = self.retrieve_files(files)
                return (
                    chat_history,
                    new_state,
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=True, value=tmp_paths)
                )
            else:
                chat_history.append({
                    "role": "assistant",
                    "content": "Ho trovato le seguenti cartelle cliniche!"
                })
                new_state = {"active": False}
                tmp_paths = self.retrieve_files(files)
                return (
                    chat_history,
                    new_state,
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=True, value=tmp_paths)
                )

        is_lms_active = self.iteration_state.check_connection()
        if is_lms_active:
            first_question = self.iteration_state.generate_question()
            chat_history.append({"role": "assistant", "content": first_question})
            new_state = {"active": True}
            return (
                chat_history,
                new_state,
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )
        else:
            chat_history.append({
                "role": "assistant",
                "content": "Errore! Non riesco a contattare il server LMS."
            })
            new_state = {"active": False}
            return (
                chat_history,
                new_state,
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )

    @staticmethod
    def retrieve_files(files):
        tmp_paths = []
        for filename, file_bytes in files:
            tmp = tempfile.NamedTemporaryFile(delete=False, prefix=os.path.splitext(filename)[0] + "___",
                                              suffix=os.path.splitext(filename)[1])
            for d in file_bytes.stream():
                tmp.write(d)
            tmp.close()
            tmp_paths.append(tmp.name)
        return tmp_paths

    def chat_flow(self, user_message, chat_history, state):
        self.reset_inactivity_timer()
        response = self.iteration_state.process_answer(user_answer=user_message)
        if isinstance(response, tuple):
            message_text, files = response
        else:
            message_text = response
            files = None

        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": message_text})

        if files:
            tmp_paths = self.retrieve_files(files)
            return (
                gr.update(visible=False),
                chat_history,
                state,
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=True, value=tmp_paths)
            )

        if "Termine" in message_text:
            return (
                gr.update(visible=False),
                chat_history,
                state,
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )

        return (
            "",
            chat_history,
            state,
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    def no_recall(self, chat_history, state):
        return self.chat_flow(self.unknown_response, chat_history, state)

    def reset_inactivity_timer(self):
        if self.timeout_timer:
            self.timeout_timer.cancel()

        self.timeout_timer = threading.Timer(self.inactivity_timeout, self.handle_inactivity_timeout)
        self.timeout_timer.daemon = True
        self.timeout_timer.start()

    def handle_inactivity_timeout(self):
        print(f"[TIMEOUT] Closing Gradio thread for user inactivity - {self.user.cf}")
        self.chat_history.append({
            "role": "assistant",
            "content": "Sessione chiusa per inattività."
        })

        self.chat_interface.close()

    def close_interface(self):
        print(f"[STOP] Closing Gradio thread for user {self.user.cf}")
        self.chat_interface.close()

    def start(self):
        with gr.Blocks(theme=gr.themes.Soft()) as chat_interface:
            self.chat_interface = chat_interface
            self.reset_inactivity_timer()
            with gr.Row():
                with gr.Column(scale=10):
                    gr.Markdown(f"### UDMA - Chat per il recupero di record medici - user {self.user.cf}")
                with gr.Column(scale=2):
                    gr.Markdown("**v.1.0.0 - powered by Alfameg**")

            chatbot = gr.Chatbot(
                self.chat_history,
                type='messages',
                show_label=False
            )
            state = gr.State()

            with gr.Row():
                start_button = gr.Button("START")
                termina_button = gr.Button("TERMINA", visible=False, variant="primary")

            with gr.Row():
                with gr.Column(scale=2):
                    no_button = gr.Button(self.unknown_response, visible=False, variant="secondary")
                with gr.Column(scale=10):
                    txt = gr.Textbox(
                        show_label=False,
                        placeholder="Scrivi la tua risposta qui...",
                        visible=False
                    )

            file_download = gr.Files(
                label="Download Cartelle",
                visible=False,
                type="filepath"
            )

            start_button.click(
                fn=self.start_chat,
                inputs=[chatbot, state],
                outputs=[chatbot, state, txt, no_button, start_button, termina_button, file_download],
            )

            txt.submit(
                fn=self.chat_flow,
                inputs=[txt, chatbot, state],
                outputs=[txt, chatbot, state, no_button, termina_button, file_download],
            )

            no_button.click(
                fn=self.no_recall,
                inputs=[chatbot, state],
                outputs=[txt, chatbot, state, no_button, termina_button, file_download],
            )

            termina_button.click(
                fn=self.close_interface,
                inputs=[],
                outputs=[],
                js="window.close()",
            )

        self.launch = chat_interface.launch(prevent_thread_lock=False)