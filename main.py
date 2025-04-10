from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from weasyprint import HTML
import docx
import os
from typing import Optional

app = FastAPI()

# Book configuration model
class BookRequest(BaseModel):
    content: str
    format: str  # "pdf", "docx", or "epub"
    trim_size: Optional[str] = "6x9"  # Default size
    font_family: Optional[str] = "Literata"  # Your selected font

@app.post("/generate-book/")
async def generate_book(request: BookRequest):
    try:
        filename = f"output.{request.format}"
        
        if request.format == "pdf":
            # PDF Generation (using WeasyPrint)
            html = f"""
            <style>
                @page {{ size: {request.trim_size}; margin: 0.75in; }}
                body {{ font-family: '{request.font_family}'; line-height: 1.5; }}
            </style>
            <div>{request.content}</div>
            """
            HTML(string=html).write_pdf(filename)
            
        elif request.format == "docx":
            # DOCX Generation
            doc = docx.Document()
            doc.add_paragraph(request.content)
            doc.save(filename)
            
        elif request.format == "epub":
            # EPUB Generation (simplified)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(request.content)
            # Note: We'll enhance this later with Pandoc
            
        return FileResponse(filename)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
