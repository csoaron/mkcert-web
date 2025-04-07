这就给你补上一个自述文件（README），适合直接放在你的项目根目录里，命名为：`README.md`

---

### ✅ `README.md` 内容如下：

```markdown
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

## 📜 License

MIT License
```

---


