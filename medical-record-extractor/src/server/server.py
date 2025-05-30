from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(fastapi):
    # threading.Thread(target="", daemon=True).start() #todo: inserire i processi necessari attivi
    yield
    # todo: implement graceful shutdown
    print("Gracefully shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost", "http://127.0.0.1"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
