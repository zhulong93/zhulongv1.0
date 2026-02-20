# 烛龙 (Zhulong) - AI数字分身

> 源自《山海经》，为蒋延春定制的AI数字分身助手

## 软件定位
AI数字分身，专注于信息提炼、消息过滤、备忘录与自我学习优化。

## 主要功能

### 1. 信息提炼
- 从互联网抓取对本人有帮助/有兴趣的新闻、文章、视频
- 每天主动推送10篇内容
- 结合底层逻辑与0~5档反馈打分，持续优化推荐
- 直观简洁的呈现方式

### 2. 微信消息过滤
- 三档分类：紧急（马上处理）、一般（1小时内）、常规（当天处理）
- 减少打扰，优先处理重要消息

### 3. 备忘录
- 随时记录
- 任务时间主动提醒
- 随时查看

### 4. 自我学习与优化
- 根据反馈持续优化推荐算法
- 学习用户偏好，提升服务有效性

## 技术架构

```
zhulong/
├── backend/          # Python FastAPI 后端
├── frontend/         # Web 前端 (Vue/React)
├── mobile/           # Android 应用 (可选 PWA)
├── desktop/          # Windows Electron 桌面端
└── shared/           # 共享配置与类型定义
```

## 快速开始

### 方式一：一键启动 (Windows)
双击运行 `run.bat`，将自动启动后端和前端，并打开浏览器。

### 方式二：手动启动

**后端**（需先安装 Python 3.10+）:
```bash
cd backend
pip install -r requirements.txt
python main.py
```
后端运行在 http://localhost:8000

**前端**（需先安装 Node.js）:
```bash
cd frontend
npm install
npm run dev
```
前端运行在 http://localhost:5173

### 桌面端 (Windows)
```bash
cd desktop
npm install
npm run start
```
（需先启动前端开发服务器，桌面端将加载 http://localhost:5173）

## 用户底层逻辑 (蒋延春)
- **身份**: 捷视飞通创始人、董事长、CEO；创业者
- **出世追求**: 佛陀追随者，终极使命：觉悟者，行菩萨道
- **入世追求**: 入世修行；创造价值与财富；科技+商业；无为法

## 交互方式
- **平台**: Android 手机、Windows PC
- **输入**: 语音或文字，自然语言
- **输出**: 提醒模式（主动推送）、查看模式（主动查看）
