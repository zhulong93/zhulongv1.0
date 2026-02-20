# 烛龙后台部署到 Railway

## 一、前置条件

1. **GitHub 账号**
2. **Railway 账号** - 访问 [railway.app](https://railway.app) 注册（可用 GitHub 登录）
3. **将项目推送到 GitHub**（若尚未推送）

---

## 二、推送代码到 GitHub

在项目根目录执行：

```bash
cd C:\Users\jiangyc\zhulong
git init
git add .
git commit -m "烛龙 v1.0"
```

在 GitHub 创建新仓库（如 `zhulong`），然后：

```bash
git remote add origin https://github.com/你的用户名/zhulong.git
git branch -M main
git push -u origin main
```

---

## 三、在 Railway 部署

### 1. 创建项目

1. 登录 [railway.app](https://railway.app)
2. 点击 **New Project**
3. 选择 **Deploy from GitHub repo**
4. 授权 Railway 访问 GitHub，选择仓库 `zhulong`

### 2. 设置根目录（重要）

1. 在项目内点击 **后端服务**
2. 进入 **Settings** → **Source**
3. **将 Root Directory 留空或删除**（不要设为 backend）
4. 项目根目录的 Dockerfile 会被使用，绕过 Railpack

### 3. 配置变量（可选）

在 **Variables** 中添加：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `PORT` | 由 Railway 自动注入，无需手动设置 | - |
| `DATABASE_URL` | 使用 PostgreSQL 时由 Railway 自动注入 | - |

### 4. 添加 PostgreSQL（推荐，数据持久化）

1. 在 Railway 项目页点击 **+ New**
2. 选择 **Database** → **PostgreSQL**
3. Railway 会自动创建数据库并注入 `DATABASE_URL`
4. 重新部署服务

> 不添加 PostgreSQL 时，将使用 SQLite，**重启或重新部署后数据会丢失**。

### 5. 生成公网地址

1. 进入服务 **Settings** → **Networking**
2. 点击 **Generate Domain**
3. 获得类似 `xxx.up.railway.app` 的地址

---

## 四、验证部署

访问 `https://你的域名.up.railway.app`，应看到：

```json
{
  "name": "烛龙",
  "version": "1.0.0",
  "message": "AI数字分身 API"
}
```

API 文档：`https://你的域名.up.railway.app/docs`

---

## 五、前端连接云端 API

修改 `frontend/vite.config.js` 中的 proxy，或新建 `frontend/.env.production`：

```env
VITE_API_BASE=https://你的域名.up.railway.app
```

并在 `frontend/src/api.js` 中根据环境变量选择 baseURL（见下方说明）。

---

## 六、费用说明

- Railway 提供约 **$5 免费额度/月**
- 后端 + PostgreSQL 在低流量下通常可免费运行
- 超出额度后按量计费，可在 Dashboard 查看用量

---

## 七、常见问题

**Q: 部署失败？**  
检查 Root Directory 是否设置为 `backend`。

**Q: 数据库连接错误？**  
若使用 PostgreSQL，确认已添加 Database 服务并完成一次重新部署。

**Q: 冷启动较慢？**  
Railway 免费层在闲置后会休眠，首次访问可能需要 30 秒左右。
