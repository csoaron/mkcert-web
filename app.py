import shutil
from pathlib import Path
from subprocess import run

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
            remark_path = item / "remark.txt"
            if cert_path.exists() and key_path.exists():
                info = get_cert_info(cert_path)
                remark = remark_path.read_text(encoding="utf-8").strip() if remark_path.exists() else ""
                certs.append({
                    "domain": domain,
                    "cert": f"/certs/{domain}/{domain}.pem",
                    "key": f"/certs/{domain}/{domain}-key.pem",
                    "not_before": info["not_before"],
                    "not_after": info["not_after"],
                    "remark": remark
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
def create_cert(
        domain: str = Form(...),
        alt_names: str = Form(""),
        remark: str = Form("")
):
    domain = domain.strip()
    san_list = [domain] + [d.strip() for d in alt_names.split(",") if d.strip()]
    output_dir = CERTS_DIR / domain
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # 创建证书
    run(["mkcert", "-cert-file", f"{domain}.pem", "-key-file", f"{domain}-key.pem"] + san_list, cwd=output_dir)

    # 保存备注（可选）
    if remark.strip():
        with open(output_dir / "remark.txt", "w", encoding="utf-8") as f:
            f.write(remark.strip())

    return RedirectResponse(url="/", status_code=303)


@app.post("/delete")
def delete_cert(domain: str = Form(...)):
    folder = CERTS_DIR / domain
    if folder.exists():
        shutil.rmtree(folder)
    return RedirectResponse(url="/", status_code=303)


@app.get("/instructions", response_class=HTMLResponse)
def root_cert_instructions(request: Request):
    return templates.TemplateResponse("root_cert_instructions.html", {"request": request})

def get_cert_info(cert_path: Path):
    try:
        with open(cert_path, "rb") as f:
            cert_data = f.read()
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        return {
            "not_before": cert.not_valid_before.strftime("%Y-%m-%d %H:%M:%S"),
            "not_after": cert.not_valid_after.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception:
        return {"not_before": "未知", "not_after": "未知"}
