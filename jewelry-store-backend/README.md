# Jewelry Store Backend - FastAPI

## المتطلبات الأساسية

1. Python 3.8+
2. MySQL (XAMPP)
3. Google Gemini API Key

## إعداد قاعدة البيانات

1. قم بتشغيل XAMPP وابدأ خدمة MySQL
2. افتح phpMyAdmin على `http://localhost/phpmyadmin`
3. أنشئ قاعدة بيانات جديدة باسم `jewelry_store`

## تثبيت المكتبات

```bash
cd jewelry-store-backend
pip install -r requirements.txt
```

## إعداد متغيرات البيئة

```bash
cp .env.example .env
```

ثم عدل ملف `.env` وأضف:
```
DATABASE_URL=mysql+pymysql://root:@localhost:3306/jewelry_store
GEMINI_API_KEY=your_actual_gemini_api_key
SECRET_KEY=your-secret-key
```

## تشغيل Seeder

```bash
python seeder.py
```

## تشغيل السيرفر

```bash
uvicorn main:app --reload --port 8000
```

الـ API سيكون متاحاً على `http://localhost:8000`

وثائق API: `http://localhost:8000/docs`

## نقاط النهاية الرئيسية

### المصادقة
- `POST /api/auth/register` - تسجيل مستخدم جديد
- `POST /api/auth/login` - تسجيل الدخول
- `GET /api/auth/me` - بيانات المستخدم الحالي

### المنتجات
- `GET /api/products/` - جميع المنتجات (مع فلاتر)
- `GET /api/products/{id}` - منتج محدد
- `POST /api/products/` - إنشاء منتج جديد

### السلة
- `GET /api/carts/` - عرض السلة
- `POST /api/carts/items` - إضافة للسلة
- `DELETE /api/carts/items/{id}` - حذف من السلة

### الطلبات
- `POST /api/orders/` - إنشاء طلب
- `GET /api/orders/` - طلبات المستخدم

### AI تصميم المجوهرات
- `POST /api/ai/generate-design` - توليد تصميم بالذكاء الاصطناعي
- `GET /api/designs` - تصاميم المستخدم
- `POST /api/design-requests` - طلب تصميم مخصص

## دليل الربط مع Frontend

### مثال على تسجيل الدخول:
```javascript
const login = async (username, password) => {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
};
```

### مثال على استدعاء محمي:
```javascript
const getProducts = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/api/products/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};
```

### مثال على توليد تصميم AI:
```javascript
const generateDesign = async (designData) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/api/ai/generate-design', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(designData)
  });
  return await response.json();
};
```