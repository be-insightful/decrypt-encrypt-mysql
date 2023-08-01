import uvicorn
import secrets
from fastapi import (
    Depends,
    FastAPI,
    Request,
    Form,
    HTTPException,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.db_connect import excute_query


security = HTTPBasic()
app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    query = f"SELECT password FROM user WHERE username='{credentials.username}'"
    result = excute_query(query=query)
    correct_password = secrets.compare_digest(credentials.password, result)
    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("page.html", {"request": request})


@app.post("/encryption", response_class=HTMLResponse)
def encrypt(request: Request, key: str = Form(...), auth: str = Form(...)):

    encrypt_query = f"SELECT HEX(AES_ENCRYPT('{key}','{auth}'));"
    result = excute_query(query=encrypt_query)

    masterkey = excute_query(
        f"SELECT masterkey FROM authentication WHERE id='admin'"
    )
    if auth == masterkey:
        return templates.TemplateResponse(
            "page.html",
            {"request": request, "result": result, "auth": masterkey},
        )
    else:
        result = "Wrong Authentication key"
        return templates.TemplateResponse(
            "auth_result.html", {"request": request, "result": result}
        )


@app.post("/decryption", response_class=HTMLResponse)
def decrypt(request: Request, key: str = Form(...), auth: str = Form(...)):

    decrypt_query = (
        f"SELECT CAST(AES_DECRYPT(UNHEX('{key}'),'{auth}') AS CHAR);"
    )
    result = excute_query(decrypt_query)

    masterkey = excute_query(
        "SELECT masterkey FROM authentication WHERE id='admin'"
    )
    if auth == masterkey:
        return templates.TemplateResponse(
            "page.html",
            {"request": request, "result2": result, "auth2": masterkey},
        )
    else:
        result = "Wrong Authentication key"
        return templates.TemplateResponse(
            "auth_result.html", {"request": request, "result": result}
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
