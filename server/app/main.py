# main.py
import asyncio
import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import settings
from app.core.config import logger_config
from app.models.data import Data
from app.graph import graph
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from langserve import add_routes


logger = logger_config(__name__)


os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = str(settings.LANGCHAIN_API_KEY)
os.environ["LANGCHAIN_PROJECT"] = str(settings.LANGCHAIN_PROJECT)
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(
    app,
    graph,
    path="/chat",
    input_type=Data
)


# # Streaming Code
@app.post("/test/chat_stream", tags=["Test Config API"])
async def openai_chat_with_bot_streaming():
    try:

        async def generate_response():
#             """Generator that yields only the response text word by word."""
            try:
                config = {"configurable": {"thread_id": "4"}}
                input_message = HumanMessage(content="Tell me about the 49ers NFL team")
                async for event in graph.astream_events({"messages": [input_message]}, config, version="v2"):
                    # Get chat model tokens from a particular node
                    print("Event: ", event["event"])
                    if event["event"] == "on_chat_model_stream":
                        chunk = event["data"].get("chunk", None)
                        print("Chunk: ", chunk)
                        if chunk:
                            yield chunk.content
                            await asyncio.sleep(
                                0.08
                            )  # Non-blocking delay of 0.5 seconds
            except Exception as e:
                logging.error(f"Error processing request: {str(e)}")
                yield f"Error processing request: {str(e)}"

        # Return the response using StreamingResponse
        return StreamingResponse(generate_response(), media_type="text/event-stream")

    except Exception as e:
        logging.error(f"Error initializing response: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error initializing response: {str(e)}"
        )

