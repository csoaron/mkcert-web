# mkcert Web 管理服务

这是一个基于 FastAPI 和 mkcert 的本地 HTTPS 证书生成管理服务，提供一个网页界面用于：

- ✅ 创建本地受信任的 HTTPS 证书
- ✅ 支持多域名（SAN）配置
- ✅ 删除证书
- ✅ 下载 `.pem` / `.key` 文件
- ✅ 提供根证书下载（可导入至其他设备）

---

## 📦 安装依赖

推荐使用虚拟环境：

```bash
sudo apt install python3-venv mkcert libnss3-tools -y

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 初始化本地根证书
mkcert -install
```

---

## 🚀 启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

打开浏览器访问：

```
http://localhost:8000
```

或使用局域网 IP：

```
http://192.168.x.x:8000
```

---

## 🐳 Docker 构建方式（可选）

你也可以使用 Docker：

```bash
docker build -t mkcert-web .
docker run -d -p 8000:8000 \
  -v $(pwd)/certs:/app/certs \
  -v $(pwd)/templates:/app/templates \
  mkcert-web
```

---

## 🧾 项目结构

```
local_ssl/
├── main.py                # FastAPI 后端
├── templates/index.html   # 网页界面
├── certs/                 # 生成的证书文件夹
├── setup.sh               # 一键部署脚本
├── requirements.txt
├── README.md              # 当前文件
```

---

## 📎 注意事项

- 所有证书仅本地受信任，适合开发 / 局域网环境
- 根证书需导入其他设备，才能让浏览器信任
- 根证书在页面顶部提供下载链接
- 配置通用证书时需注意
  - 主域名正常填写
  - 备用域名（逗号分隔）这里填写 *.主域名

---


## 🧭 总览：各系统根证书安装位置/方式

| 系统       | 安装方式 / 放置路径                                                |
|------------|---------------------------------------------------------------------|
| **Windows** | 自动安装到系统信任库（mkcert 会调用 `certutil`）<br>手动：MMC 控制台或 `certutil` |
| **CentOS**  | `/etc/pki/ca-trust/source/anchors/` → `update-ca-trust`              |
| **Ubuntu**  | `/usr/local/share/ca-certificates/`（需 `.crt` 扩展） → `update-ca-certificates` |
| **Arch / Manjaro** | `/etc/ca-certificates/trust-source/anchors/` → `trust extract-compat`     |
| **macOS**   | 自动安装到“系统钥匙串”或“登录钥匙串”<br>手动：钥匙串访问工具 or `security` 命令 |

---

## 🔍 详细说明：

---

### 🪟 **Windows**

- **自动安装（mkcert）**：
  ```bash
  mkcert -install
  ```
  会自动使用 `certutil` 安装到系统信任证书库。

- **手动路径（MMC 控制台）**：
  - Win + R → `mmc`
  - 添加管理单元：证书 → 计算机帐户
  - 导入到 “受信任的根证书颁发机构” 中

- **命令行安装**：
  ```bash
  certutil -addstore -f "Root" rootCA.pem
  ```

---

### 🐧 **CentOS / RHEL**

```bash
sudo cp rootCA.pem /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```

---

### 🐧 **Ubuntu / Debian**

```bash
sudo cp rootCA.pem /usr/local/share/ca-certificates/my-root.crt
sudo update-ca-certificates
```

> ✅ 注意文件扩展名要是 `.crt`

---

### 🐧 **Arch / Manjaro**

```bash
sudo cp rootCA.pem /etc/ca-certificates/trust-source/anchors/
sudo trust extract-compat
```

---

### 🍎 **macOS**

- **自动安装（mkcert）**：
  ```bash
  mkcert -install
  ```

- **手动安装（图形界面）**：
  - 打开“钥匙串访问”
  - 拖拽 `rootCA.pem` 到 “系统” 或 “登录” 钥匙串
  - 双击 → 设置为“始终信任”

- **命令行方式**：
  ```bash
  sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain rootCA.pem
  ```

---

## 💡 小提示

- 安装完后，**重启浏览器** 或某些守护进程（如 `curl`/`wget`）才会识别新证书；
- 建议将根证书保存在服务端，比如 `/certs/rootCA.pem`，客户端可下载后执行导入脚本；
---

## 📜 License

MIT License

---
