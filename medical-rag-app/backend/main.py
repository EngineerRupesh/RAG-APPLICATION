"""
================================================================================
 MAIN APPLICATION ENTRY POINT
--------------------------------------------------------------------------------
 Creates the FastAPI app, wires up CORS, and registers each route module.
 This is a pure JSON API - the UI lives in the separate Next.js app under
 ../frontend, which talks to this server over HTTP.

 This file only does wiring - all business logic lives in services/, and
 all HTTP handling lives in routes/.
================================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from routes import health_routes, document_routes, chat_routes, evaluation_routes

# ---------------------------------------------------------------------------
# App + middleware
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Medical Assistant RAG API",
    description="A Retrieval-Augmented-Generation API for answering questions "
    "grounded in user-uploaded medical PDFs. Consumed by the Next.js frontend.",
    version="2.1.0",
)

# The Next.js dev server runs on a different port (3000) than the API (8000),
# so CORS must be enabled for the frontend to call these endpoints.
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes - one router per topic (see routes/)
# ---------------------------------------------------------------------------
app.include_router(health_routes.router)
app.include_router(document_routes.router)
app.include_router(chat_routes.router)
app.include_router(evaluation_routes.router)


@app.get("/", tags=["System"])
def root():
    """Points people at the interactive API docs instead of a blank page."""
    return {"message": "MedGrounded API is running.", "docs": "/docs", "health": "/health"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=config.APP_HOST, port=config.APP_PORT, reload=True)
