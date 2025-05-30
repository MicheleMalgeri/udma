import multiprocessing
import signal
import sys
import threading
from threading import Event

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from src.client.gradio.gradio_interface import GradioInterface
from src.server.adapter.ai.knn.knn import KNN
from src.server.adapter.database.mysql.repository.census_repository import CensusRepository
from src.server.adapter.rest.factory import ConcreteFactory
from src.server.domain.factory.abstract_factory import AbstractFactory
from src.server.domain.model.entity.user_info import UserInfo
from src.server.domain.model.entity.user_weight import UserWeight

gradio_threads = []

app = FastAPI()


class GradioRequest(BaseModel):
    age: int
    city: str
    codice_fiscale: str


@app.post("/start_gradio")
def launch_gradio(req: GradioRequest):
    population = CensusRepository().get_population_by_city(req.city)
    if population == 0:
        return {
            "status": "Comune non valido (es. 'Catania')",
            "city": req.city
        }
    target_user_info = UserInfo(age=req.age, population=population, cf=req.codice_fiscale)
    weight = KNN.get_instance().evaluate_weight(target_user_info)
    target_user = UserWeight().extend_user_info(target_user_info, weight=weight)

    p = multiprocessing.Process(target=start_gradio, args=(target_user,), name="GradioChat")
    p.start()
    gradio_threads.append(p)

    print(f"[START] Gradio thread started for user {target_user.cf} with PID {p.pid}")

    def watcher(proc, user_cf):
        proc.join()
        print(f"Thread chiuso per l'utente con codice fiscale {user_cf}")

    threading.Thread(target=watcher, args=(p, target_user.cf), daemon=True).start()

    return {
        "status": "Gradio started",
        "thread_name": p.name,
        "pid": p.pid,
        "user": target_user.cf,
        "link": "http://127.0.0.1:7860}"
    }


def initialize_server(factory: AbstractFactory, init_e: Event):
    api_port = factory.create_api_port()
    api_port.get_routes()
    init_e.set()


def start_gradio(user):
    gradio_chat = GradioInterface(user)
    gradio_chat.start()
    return gradio_chat


def start_batch():
    from src.server.domain.usecase.batch import Batch
    batch = Batch.get_instance()
    batch.start()
    return batch


def run(init_e: Event):
    init_e.wait()
    threading.Thread(target=start_server(), daemon=True).start()
    init_e.clear()


def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def handle_sig(sig, event) -> None:
    print("\nReceived Stop signal. Shutting down threads...")
    event.set()
    sys.exit(0)


def signals(stop_e: Event) -> None:
    signal.signal(signal.SIGINT, handle_sig(signal.SIGINT, stop_e))
    signal.signal(signal.SIGTERM, handle_sig(event=stop_e, sig=signal.SIGTERM))


if __name__ == '__main__':
    stop_event = threading.Event()
    init_event = threading.Event()
    threading.Thread(target=initialize_server, args=(ConcreteFactory.get_instance(), init_event,), daemon=True).start()
    threading.Thread(target=start_batch, daemon=True).start()
    run(init_event)
