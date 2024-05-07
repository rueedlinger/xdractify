import base64
import binascii
import logging

from fastapi import FastAPI, UploadFile, Request
from starlette.responses import JSONResponse

from xdractify.model import Document, PdfDocument, DataEncoding, Data, Extracts
from xdractify.pdf import extract_pypdf

# get root logger
logger = logging.getLogger("xdractify.api")

app = FastAPI()


@app.exception_handler(binascii.Error)
async def unicorn_exception_handler(request: Request, ex: binascii.Error):
    return JSONResponse(
        status_code=400,
        content={"message": f"bas46 error, {ex}"},
    )


@app.post("/pdf")
async def read_item(doc: PdfDocument) -> Extracts:
    logger.debug(f"processing pdf: {doc.engine}")
    if doc.data.encoding == DataEncoding.base64:
        raw = base64.b64decode(doc.data.content)
        # return extract_pypdfium2(raw)
        return extract_pypdf(raw)
        # logger.debug(raw)
    return {}


@app.post("/base64/encode")
async def input_request(file: UploadFile) -> Document:
    logger.debug(
        f"base64 encode: filename='{file.filename}', size='{file.size}', content_type='{file.content_type}'"
    )
    contents = await file.read()
    encoded = base64.b64encode(contents)
    return Document.parse_obj(
        {
            "name": file.filename,
            "data": Data.parse_obj(
                {"encoding": DataEncoding.base64, "content": encoded}
            ),
        }
    )


"""
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
"""
