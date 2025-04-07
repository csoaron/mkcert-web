import os
import shutil
from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from subprocess import run
from pathlib import Path

app = FastAPI()

# 文件存储路径
CERTS_DIR = Path("certs")
CERTS_DIR.mkdir(exist_ok=True)

# 根证书路径（默认 mkcert 安装在这个位置）
ROOT_CA_PATH = Path.home() / ".local/share/mkcert/rootCA.pem"

# 静态文件和模板
app.mount("/certs", StaticFiles(directory=str(CERTS_DIR)), name="certs")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    certs = []
    for item in CERTS_DIR.iterdir():
        if item.is_dir():
            domain = item.name
            cert_path = item / f"{domain}.pem"
            key_path = item / f"{domain}-key.pem"
            if cert_path.exists() and key_path.exists():
                certs.append({
                    "domain": domain,
                    "cert": f"/certs/{domain}/{domain}.pem",
                    "key": f"/certs/{domain}/{domain}-key.pem"
                })
    root_ca_exists = ROOT_CA_PATH.exists()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "certs": certs,
        "root_ca_url": "/ca/rootCA.pem" if root_ca_exists else None
    })


@app.get("/ca/rootCA.pem")
def get_root_ca():
    if ROOT_CA_PATH.exists():
        return FileResponse(ROOT_CA_PATH, filename="rootCA.pem")
    return HTMLResponse("<h1>Root CA not found</h1>", status_code=404)


@app.post("/create")
def create_cert(domain: str = Form(...), alt_names: str = Form("")):
    domain = domain.strip()
    san_list = [domain] + [d.strip() for d in alt_names.split(",") if d.strip()]
    output_dir = CERTS_DIR / domain
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    # 创建证书
    run(["mkcert", "-cert-file", f"{domain}.pem", "-key-file", f"{domain}-key.pem"] + san_list, cwd=output_dir)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete")
def delete_cert(domain: str = Form(...)):
    folder = CERTS_DIR / domain
    if folder.exists():
        shutil.rmtree(folder)
    return RedirectResponse(url="/", status_code=303)
