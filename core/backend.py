import os
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from agent_workflow.main import process
from core.logging_helpers import logger
from database.database_manager import create_graph
from database.document_retriever import process_pdf, process_arxiv

app = FastAPI(title="AI research assistant")

@app.post("/chat")
async def process_input(text: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    if file is not None:
        file_bytes = await file.read()

        # Create a full file path in the current working directory using the original filename
        save_path = os.path.join(os.getcwd(), file.filename)

        # Write the file to disk in binary write mode
        with open(save_path, "wb") as f:
            f.write(file_bytes)

        documents = process_pdf(save_path)
        is_graph = create_graph(documents)
        if not is_graph:
            logger.info("Unable to create the graph")
            return

        response = process()
        return response

    elif text:
        documents = process_arxiv(text)
        is_graph = create_graph(documents)
        if not is_graph:
            logger.info("Unable to create the graph")
            return

        response = process()
        return response
    else:
        raise HTTPException(status_code=400, detail="No text or file provided")
