@echo off
chcp 65001 >nul
echo ========================================
echo   烛龙 - 推送到 GitHub 并触发 Railway 部署
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查 Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Git，请先安装 https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [2/4] 添加更改...
git add .
if errorlevel 1 (
    echo 添加文件失败
    pause
    exit /b 1
)

echo [3/4] 提交...
git commit -m "使用 Dockerfile 修复 Railway 构建" 2>nul
if errorlevel 1 (
    echo 无可提交的更改，或已是最新
) else (
    echo 提交成功
)

echo [4/4] 推送到 GitHub...
git push
if errorlevel 1 (
    echo.
    echo 推送失败，请检查：
    echo   1. 是否已配置 GitHub 用户名和邮箱
    echo   2. 网络是否正常
    echo   3. 如需登录，请按提示输入凭据
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   完成！Railway 将自动重新部署
echo   请到 railway.app 查看部署状态
echo ========================================
pause
