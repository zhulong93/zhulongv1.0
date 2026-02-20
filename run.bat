@echo off
chcp 65001 >nul
echo 烛龙 - AI数字分身
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 请先安装 Python 3.10+
    pause
    exit /b 1
)

REM 安装后端依赖
cd backend
if not exist ".venv" (
    echo 创建虚拟环境...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt -q

REM 启动后端
echo 启动后端 API (端口 8000)...
start "烛龙-后端" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate.bat && python main.py"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 安装并启动前端
cd ..\frontend
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)
echo 启动前端 (端口 5173)...
start "烛龙-前端" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo 后端: http://localhost:8000
echo 前端: http://localhost:5173
echo.
echo 按任意键打开浏览器...
pause >nul
start http://localhost:5173
