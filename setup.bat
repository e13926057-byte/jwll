@echo off
echo ========================================
echo اعداد مشروع متجر المجوهرات
echo ========================================

echo.
echo [1/3] جاري تثبيت المتطلبات...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo خطأ في تثبيت المتطلبات!
    pause
    exit /b 1
)

echo.
echo [2/3] جاري تشغيل الـ Seeder...
python seeder.py

if %errorlevel% neq 0 (
    echo خطأ في تشغيل الـ Seeder!
    pause
    exit /b 1
)

echo.
echo [3/3] تم الاعداد بنجاح!
echo.
echo يمكنك الآن تشغيل الخادم باستخدام start.bat
echo.
pause
