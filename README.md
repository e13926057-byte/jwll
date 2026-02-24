# واجهة برمجة تطبيقات متجر المجوهرات الإلكتروني

## نظرة عامة على المشروع

هذا المشروع يمثل واجهة برمجة تطبيقات كاملة ومتخصصة لمتجر مجوهرات إلكتروني متقدم، يتميز بقدرته على تصميم المجوهرات باستخدام تقنيات الذكاء الاصطناعي. تم بناء هذا النظام بأحدث التقنيات وأفضل الممارسات في مجال تطوير البرمجيات، حيث يعتمد على إطار عمل FastAPI الحديث الذي يوفر سرعة عالية في معالجة الطلبات ودعمًا قويًا للتحقق من البيانات. كما يستخدم المشروع قاعدة بيانات MySQL عبر خادم XAMPP المحلي لنظام إدارة العلاقات بين البيانات، ويستخدم SQLAlchemy كطبقة ORM لتسهيل التعامل مع قاعدة البيانات. يدعم النظام أيضًا تكامل Google Gemini API لتمكين المستخدمين من تصميم مجوهرات فريدة من خلال أوصاف نصية بسيطة.

يهدف هذا المشروع إلى توفير منصة شاملة لإدارة جميع جوانب متجر المجوهرات، سواء كان ذلك من حيث إدارة المنتجات وفئات المجوهرات المختلفة، أو معالجة طلبات الشراء والدفع، أو توفير خدمة التصميم بالذكاء الاصطناعي التي تتيح للمستخدمين إنشاء تصاميم مخصصة تلبي أذواقهم ومتطلباتهم الفريدة. تم تصميم النظام ليكون قابلاً للتوسع والتطوير المستقبلي، مع مراعاة أفضل معايير الأمان في تخزين بيانات المستخدمين وكلمات المرور المشفرة.

---

## متطلبات النظام التشغيلية

لم 运行 هذا المشروع بنجاح، يجب توفر المتطلبات التالية على جهازك. هذه المتطلبات ضرورية لضمان عمل جميع مكونات النظام بشكل صحيح ومنسجم.

首先، تحتاج إلى تثبيت Python بإصدار 3.8 أو أعلى على نظامك. يُنصح باستخدام أحدث إصدار مستقر من Python لضمان التوافق مع جميع المكتبات المستخدمة. يمكنك التحقق من إصدار Python المثبت على جهازك عن طريق تنفيذ الأمر `python --version` في سطر الأوامر.

ثانياً، تحتاج إلى تثبيت خادم XAMPP الذي يتضمن خادم MySQL اللازم لتشغيل قاعدة البيانات. يمكنك تحميل XAMPP مجانًا من الموقع الرسمي apachefriends.org. تأكد من تشغيل خدمة MySQL فقط من لوحة تحكم XAMPP دون الحاجة لتشغيل Apache للجزء الخلفي.

أخيراً، ستحتاج إلى مفتاح API من Google Gemini للوصول إلى خدمات الذكاء الاصطناعي. يمكنك الحصول على هذا المفتاح مجانًا من Google AI Studio بعد إنشاء حساب Google.

---

## إعداد قاعدة بيانات MySQL عبر XAMPP

### تثبيت وتشغيل XAMPP

قم بتنزيل برنامج XAMPP من الموقع الرسمي على الرابط https://www.apachefriends.org/index.html واختر الإصدار المناسب لنظام التشغيل الخاص بك. بعد اكتمال التنزيل، شغّل ملف التثبيت واتبع التعليمات التي تظهر على الشاشة. بمجرد اكتمال التثبيت، افتح لوحة تحكم XAMPP من قائمة ابدأ أو من مجلد التثبيت.

في نافذة لوحة التحكم، ستجد قائمة بالخدمات المتاحة. ابحث عن خدمة MySQL في القائمة وانقر على زر Start لتشغيلها. بمجرد بدء الخدمة، سيتحول لون المؤشر إلى الأخضر للإشارة إلى أن الخدمة تعمل بنجاح. بعد ذلك، انقر على زر Admin الموجود بجانب خدمة MySQL لفتح واجهة phpMyAdmin في متصفحك الافتراضي.

### إنشاء قاعدة البيانات

في واجهة phpMyAdmin، ستجد قائمة قواعد البيانات الموجودة على اليسار. في الجزء العلوي الأيسر من الصفحة، ستجد حقلاً نصيًا باسم "Create database". اكتب اسم قاعدة البيانات `jewelry_db` في هذا الحقل، ثم اختر `utf8mb4_general_ci` من قائمة Collation لضمان دعم الأحرف العربية واللغات الأخرى بشكل صحيح. أخيرًا، انقر على زر Create لإنشاء قاعدة البيانات.

يجب أن تظهر قاعدة البيانات الجديدة في قائمة قواعد البيانات على اليسار. انقر عليها لتحديدها، ثم انتقل إلى علامة تبويب Privileges للتحقق من صلاحيات المستخدم. استخدم اسم المستخدم `root` بدون كلمة مرور للاتصال بقاعدة البيانات، وهذا هو الإعداد الافتراضي في XAMPP.

---

## تثبيت المتطلبات والحزم

### إنشاء البيئة الافتراضية

يُنصح بشدة إنشاء بيئة افتراضية معزولة لمشروعك لتجنب تعارض الحزم مع مشاريع أخرى. لإنشاء بيئة افتراضية جديدة، افتح سطر الأوامر في مجلد المشروع ونفذ الأمر التالي الذي سينشئ مجلدًا جديدًا يحتوي على جميع ملفات البيئة المعزولة.

```bash
python -m venv venv
```

بعد إنشاء البيئة الافتراضية، تحتاج إلى تفعيلها. على نظام التشغيل Windows،.execute الأمر التالي في سطر الأوامر.

```bash
venv\Scripts\activate
```

على نظامي Linux أو Mac، execute الأمر التالي بدلاً من ذلك.

```bash
source venv/bin/activate
```

ستلاحظ ظهور اسم البيئة الافتراضية قبل مسار المجلد في سطر الأوامر، وهذا يشير إلى نجاح تفعيل البيئة.

### تثبيت الحزم المطلوبة

الآن بعد تفعيل البيئة الافتراضية، حان الوقت لتثبيت جميع الحزم المطلوبة للمشروع. يتم تخزين قائمة الحزم في ملف requirements.txt، وكل ما عليك فعله هو تنفيذ الأمر التالي الذي سيقوم بتنزيل وتثبيت جميع الحزم تلقائياً.

```bash
pip install -r requirements.txt
```

ستظهر عملية التثبيت في سطر الأوامر، وقد تستغرق بعض الوقت حسب سرعة اتصالك بالإنترنت. بمجرد اكتمال التثبيت، ستكون جميع المتطلبات جاهزة للاستخدام.

---

## إعداد المتغيرات البيئية

### إنشاء ملف المتغيرات

بعد تثبيت الحزم، تحتاج إلى إنشاء ملف المتغيرات البيئية. انسخ ملف المثال المتوفر في المشروع باستخدام الأمر التالي على Windows.

```bash
copy .env.example .env
```

على Linux أو Mac، استخدم الأمر التالي.

```bash
cp .env.example .env
```

### تحرير ملف المتغيرات

افتح ملف .env الذي أنشأته في أي محرر نصي واملأ القيم المطلوبة. الملف يحتوي على المتغيرات التالية التي يجب تعديلهاaccording to إعداداتك.

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/jewelry_db
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

لمفتاح Gemini API، انتقل إلى https://aistudio.google.com/app/apikey وسجّل دخولك بحساب Google. أنشئ مفتاح API جديد وانسخه إلى الملف. هذا المفتاح ضروري لعمل ميزة التصميم بالذكاء الاصطناعي.

---

## تشغيل سكريبت تعبئة البيانات

يحتوي المشروع على سكريبت تعبئة بيانات مُعد مسبقًا يقوم بإنشاء بيانات تجريبية لاختبار النظام. يشمل ذلك مستخدمين وصائغين وفئات ومنتجات وهمية.为了让 النظام يعمل فوراً مع بيانات اختبارية، execute الأمر التالي.

```bash
python seeder.py
```

عند نجاح التنفيذ، ستظهر رسائل تؤكد إنشاء كل عنصر. سيتم حذف جميع البيانات الموجودة مسبقاً وإعادة إنشائها من جديد. السكريبت ينشئ 5 مستخدمين و 3 صائغين و 8 فئات و 10 منتجات مجوهرات متنوعة.

---

## تشغيل خادم FastAPI

### تشغيل الخادم

لبدء تشغيل الخادم، يمكنك استخدام أحد الأمرين التاليين. الطريقة الأولى تستخدم Uvicorn مباشرة مع خيار إعادة التحميل التلقائي.

```bash
uvicorn main:app --reload
```

الطريقة الثانية تستخدم Python مباشرة.

```bash
python main.py
```

بمجرد تشغيل الخادم بنجاح، سيمكنك الوصول إلى الخدمة على العنوان http://localhost:8000. سيبدأ الخادم في الاستماع على المنفذ 8000 الافتراضي.

### الوصول إلى التوثيق

FastAPI يوفر توثيقًا تفاعليًا يمكنك استخدامه لاستكشاف واختبار جميع نقاط النهاية. للوصول إلى واجهة Swagger UI، افتح متصفحك وانتقل إلى http://localhost:8000/docs. هذه الواجهة تتيح لك رؤية جميع المسارات المتاحة وإرسال طلبات اختبار مباشرة من المتصفح.

للوصول إلى واجهة ReDoc البديلة، انتقل إلى http://localhost:8000/redoc. توفر هذه الواجهة توثيقًا منظماً بشكل مختلف قد يكون أكثر ملاءمة للبعض.

---

## هيكل المشروع والمجلدات

تم تنظيم المشروع بشكل منطقي لتسهيل التنقل والفهم. يتكون المشروع من المجلدات والملفات التالية التي تؤدي كل منها دوراً محدداً في عمل النظام.

في المستوى الجذر للمشروع، ستجد الملفات الرئيسية مثل main.py الذي يمثل نقطة الدخول الرئيسية للتطبيق، وملف database.py الذي يحتوي على إعدادات الاتصال بقاعدة البيانات. كما ستجد ملف requirements.txt الذي يحتوي على قائمة جميع الحزم المطلوبة، وملف seeder.py الذي负责 تعبئة البيانات الأولية.

داخل مجلد models، ستجد ملف models.py الذي يحتوي على جميع نماذج قاعدة البيانات المُعرَّفة باستخدام SQLAlchemy. تُعرِّف هذه النماذج الجداول والعلاقات في قاعدة البيانات.

داخل مجلد schemas، ستجد ملف schemas.py الذي يحتوي على مخططات Pydantic للتحقق من صحة البيانات الواردة من العملاء وإرجاع الاستجابات بشكل منظم.

داخل مجلد routers، ستجد جميع ملفات نقاط النهاية مقسمة حسب الوظيفة. ملف auth.py يتعامل مع المصادقة وتسجيل الدخول، وملف products.py يدير العمليات المتعلقة بالمنتجات، وملف cart.py يتعامل مع سلة التسوق، وملف orders.py يدير الطلبات، وملف ai.py يوفر وظائف التصميم بالذكاء الاصطناعي، وملف design_requests.py يدير طلبات التصميم المخصص، وأخيراً ملف payment_methods.py يدير طرق الدفع.

داخل مجلد static/generated_designs، يتم تخزين الصور التي يولدها الذكاء الاصطناعي للمستخدمين.

---

## دليل مطور الواجهة الأمامية

### نظرة عامة على الاتصال

الواجهة الأمامية تتصل بالـ Backend من خلال واجهة REST API بسيطة ومباشرة. يدعم النظام طلبات CORS من أي أصل، مما يعني أنه يمكنك تطوير الواجهة الأمامية على أي نطاق أو نطاق محلي دون مشاكل.

جميع الطلبات التي تتطلب بيانات شخصية أو إجراءات خاصة تحتاج إلى مصادقة. يتم المصادقة من خلال JSON Web Token الذي يُعاد بعد تسجيل الدخول بنجاح.

---

### نظام المصادقة

#### تسجيل مستخدم جديد

للتسجيل في النظام، أرسل طلب POST إلى مسار /api/auth/register مع بيانات المستخدم المطلوبة. فيما يلي مثال بلغة JavaScript يوضح كيفية إجراء هذا الطلب باستخدام fetch.

```javascript
async function register(userData) {
    const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    return response.json();
}

// مثال على الاستخدام
register({
    username: 'john_doe',
    email: 'john@example.com',
    password: 'password123',
    first_name: 'John',
    last_name: 'Doe',
    phone: '+966501234567',
    gender: 'male'
});
```

#### تسجيل الدخول

للتسجيل في النظام والحصول على رمز المصادقة، أرسل طلب POST إلى مسار /api/auth/login مع اسم المستخدم وكلمة المرور. يحفظ الرمز المستلم في التخزين المحلي لاستخدامه في الطلبات اللاحقة.

```javascript
async function login(username, password) {
    const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    
    if (data.access_token) {
        localStorage.setItem('token', data.access_token);
    }
    return data;
}
```

#### تضمين رمز المصادقة

بعد تسجيل الدخول بنجاح، يجب تضمين رمز المصادقة في ترويسات جميع الطلبات التي تتطلب تسجيل الدخول. الدالة التالية تُنشئ الترويسات المطلوبة تلقائياً.

```javascript
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}
```

---

### العمليات التجارية الأساسية

#### عرض المنتجات

للحصول على قائمة بجميع المنتجات، يمكنك استخدام طلب GET إلى مسار /api/products. يدعم هذا المسار معاملات اختيارية للفلترة حسب الفئة أو المادة أو نطاق السعر.

```javascript
async function getProducts(categoryId = null, material = null, minPrice = null, maxPrice = null) {
    let url = 'http://localhost:8000/api/products?';
    
    if (categoryId) url += `category_id=${categoryId}&`;
    if (material) url += `material=${material}&`;
    if (minPrice) url += `min_price=${minPrice}&`;
    if (maxPrice) url += `max_price=${maxPrice}&`;
    
    const response = await fetch(url);
    return response.json();
}

// مثال: الحصول على خواتم ذهب
getProducts(categoryId=1, material='Gold');
```

#### عرض منتج واحد

للحصول على تفاصيل منتج محدد، استخدم طلب GET مع معرف المنتج في المسار.

```javascript
async function getProduct(productId) {
    const response = await fetch(`http://localhost:8000/api/products/${productId}`);
    return response.json();
}
```

#### إضافة منتج للسلة

لإضافة منتج إلى سلة التسوق، أرسل طلب POST إلى مسار /api/cart/items مع معرف المنتج والكمية المطلوبة.

```javascript
async function addToCart(productId, quantity = 1) {
    const response = await fetch('http://localhost:8000/api/cart/items', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ product_id: productId, quantity })
    });
    return response.json();
}
```

#### عرض محتويات السلة

للحصول على محتويات سلة التسوق الحالية للمستخدم، استخدم طلب GET إلى مسار /api/cart مع ترويسات المصادقة.

```javascript
async function getCart() {
    const response = await fetch('http://localhost:8000/api/cart', {
        headers: getAuthHeaders()
    });
    return response.json();
}
```

#### إزالة عنصر من السلة

لإزالة عنصر من السلة، استخدم طلب DELETE إلى مسار /api/cart/items/{معرف العنصر}.

```javascript
async function removeFromCart(itemId) {
    const response = await fetch(`http://localhost:8000/api/cart/items/${itemId}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    });
    return response.json();
}
```

#### إنشاء طلب جديد

لتحويل محتويات السلة إلى طلب شراء، أرسل طلب POST إلى مسار /api/orders مع بيانات الشحن وطريقة الدفع.

```javascript
async function createOrder(paymentMethodId, shippingAddress, transferReceipt = null) {
    const response = await fetch('http://localhost:8000/api/orders', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
            payment_method_id: paymentMethodId,
            shipping_address: shippingAddress,
            transfer_receipt: transferReceipt
        })
    });
    return response.json();
}
```

#### عرض طلبات المستخدم

للحصول على قائمة بجميع طلبات المستخدم الحالي، استخدم طلب GET إلى مسار /api/orders.

```javascript
async function getOrders() {
    const response = await fetch('http://localhost:8000/api/orders', {
        headers: getAuthHeaders()
    });
    return response.json();
}
```

---

### ميزة التصميم بالذكاء الاصطناعي

هذه هي الميزة الأكثر أهمية في المشروع، حيث تتيح للمستخدمين إنشاء تصاميم مجوهرات فريدة باستخدام الذكاء الاصطناعي. يرسل المستخدم مواصفات التصميم المطلوبة، ويعيد النظام صورة مولدة بالذكاء الاصطناعي.

#### إنشاء تصميم جديد

لإنشاء تصميم مجوهرات بالذكاء الاصطناعي، أرسل طلب POST إلى مسار /api/ai/generate-design مع بيانات التصميم المطلوبة. يجب أن يكون المستخدم مسجلاً للدخول.

```javascript
async function generateJewelryDesign(designOptions) {
    const response = await fetch('http://localhost:8000/api/ai/generate-design', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
            type: 'Ring',              // نوع المجوهرات: Ring, Necklace, Earring, Bracelet
            color: 'Gold',             // اللون: Gold, Silver, Rose Gold
            shape: 'Oval',             // الشكل: Oval, Round, Square, Heart
            material: 'Gold',          // المادة: Gold, Silver, Platinum
            karat: '21k',              // العيار: 18k, 21k, 24k, 925
            gemstone_type: 'Diamond',  // نوع الحجر: Diamond, Ruby, Emerald, Sapphire, None
            gemstone_color: 'White'     // لون الحجر: White, Blue, Red, Green
        })
    });
    
    const data = await response.json();
    return data;
}

// مثال على الاستخدام
generateJewelryDesign({
    type: 'Ring',
    color: 'Gold',
    shape: 'Heart',
    material: 'Gold',
    karat: '21k',
    gemstone_type: 'Diamond',
    gemstone_color: 'White'
}).then(design => {
    console.log('تم إنشاء التصميم:', design.generated_image_url);
    console.log('معرف التصميم:', design.id);
    
    // عرض الصورة في الصفحة
    const img = document.createElement('img');
    img.src = 'http://localhost:8000' + design.generated_image_url;
    document.body.appendChild(img);
});
```

#### نموذج HTML كامل للتصميم

فيما يلي نموذج كامل بلغة HTML و JavaScript يوضح كيفية بناء واجهة مستخدم كاملة للتصميم بالذكاء الاصطناعي.

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تصميم مجوهرات بالذكاء الاصطناعي</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .design-form { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #d4af37; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; }
        select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        button { width: 100%; background: #d4af37; color: white; padding: 15px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; transition: background 0.3s; }
        button:hover { background: #b8962e; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        #result { margin-top: 20px; text-align: center; }
        #result img { max-width: 100%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .loading { color: #666; font-style: italic; }
    </style>
</head>
<body>
    <div class="design-form">
        <h1>✨ صمم مجوهراتك بالذكاء الاصطناعي</h1>
        
        <div class="form-group">
            <label>نوع المجوهرات</label>
            <select id="type">
                <option value="Ring">خاتم</option>
                <option value="Necklace">قلادة</option>
                <option value="Earring">أقراط</option>
                <option value="Bracelet">سوار</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>اللون</label>
            <select id="color">
                <option value="Gold">ذهبي</option>
                <option value="Silver">فضي</option>
                <option value="Rose Gold">وردي ذهبي</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>الشكل</label>
            <select id="shape">
                <option value="Oval">بيضاوي</option>
                <option value="Round">دائري</option>
                <option value="Square">مربع</option>
                <option value="Heart">قلب</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>المادة</label>
            <select id="material">
                <option value="Gold">ذهب</option>
                <option value="Silver">فضة</option>
                <option value="Platinum">بلاتين</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>العيار</label>
            <select id="karat">
                <option value="18k">18 قيراط</option>
                <option value="21k">21 قيراط</option>
                <option value="24k">24 قيراط</option>
                <option value="925">925</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>نوع الحجر الكريم</label>
            <select id="gemstone_type">
                <option value="Diamond">ألماس</option>
                <option value="Ruby">ياقوت</option>
                <option value="Emerald">زمرد</option>
                <option value="Sapphire">ياقوت أزرق</option>
                <option value="None">بدون حجر</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>لون الحجر الكريم</label>
            <select id="gemstone_color">
                <option value="White">أبيض</option>
                <option value="Blue">أزرق</option>
                <option value="Red">أحمر</option>
                <option value="Green">أخضر</option>
            </select>
        </div>
        
        <button onclick="generateDesign()" id="generateBtn">إنشاء تصميم</button>
        
        <div id="result"></div>
    </div>

    <script>
        const API_BASE = 'http://localhost:8000';
        
        function getAuthHeaders() {
            const token = localStorage.getItem('token');
            return {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            };
        }
        
        async function generateDesign() {
            const btn = document.getElementById('generateBtn');
            const result = document.getElementById('result');
            
            btn.disabled = true;
            btn.textContent = 'جاري إنشاء التصميم... ⏳';
            
            const designData = {
                type: document.getElementById('type').value,
                color: document.getElementById('color').value,
                shape: document.getElementById('shape').value,
                material: document.getElementById('material').value,
                karat: document.getElementById('karat').value,
                gemstone_type: document.getElementById('gemstone_type').value,
                gemstone_color: document.getElementById('gemstone_color').value
            };
            
            try {
                const response = await fetch(`${API_BASE}/api/ai/generate-design`, {
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: JSON.stringify(designData)
                });
                
                if (!response.ok) {
                    throw new Error('فشل في إنشاء التصميم');
                }
                
                const data = await response.json();
                
                result.innerHTML = `
                    <h3>تم إنشاء التصميم بنجاح! 🎉</h3>
                    <img src="${API_BASE}${data.generated_image_url}" alt="التصميم Generated">
                    <p><strong>معرف التصميم:</strong> ${data.id}</p>
                `;
            } catch (error) {
                result.innerHTML = `<p style="color: red;">خطأ: ${error.message}</p>`;
            } finally {
                btn.disabled = false;
                btn.textContent = 'إنشاء تصميم';
            }
        }
    </script>
</body>
</html>
```

---

### استخدام مكتبة Axios

إذا كنت تفضل استخدام مكتبة Axios بدلاً من fetch، فيما يلي مثال على كيفية إعدادها بشكل صحيح مع المصادقة التلقائية.

```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE,
    headers: {
        'Content-Type': 'application/json'
    }
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

async function login(username, password) {
    const response = await api.post('/api/auth/login', { username, password });
    if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
}

async function generateDesign(designOptions) {
    const response = await api.post('/api/ai/generate-design', designOptions);
    return response.data;
}
```

---

## مرجع شامل لنقاط النهاية

يوضح الجدول التالي جميع نقاط النهاية المتاحة في النظام، مع تحديد الطريقة HTTP المطلوبة والمسار ووصف الوظيفة وما إذا كانت تتطلب مصادقة.

| الطريقة | المسار | الوصف | المصادقة |
|---------|--------|-------|----------|
| POST | /api/auth/register | تسجيل مستخدم جديد | لا |
| POST | /api/auth/login | تسجيل الدخول والحصول على رمز | لا |
| GET | /api/auth/me | الحصول على بيانات المستخدم الحالي | نعم |
| GET | /api/products | قائمة المنتجات مع خيارات الفلترة | لا |
| GET | /api/products/{id} | تفاصيل منتج واحد | لا |
| POST | /api/products | إضافة منتج جديد | نعم |
| PUT | /api/products/{id} | تحديث منتج موجود | نعم |
| DELETE | /api/products/{id} | حذف منتج | نعم |
| GET | /api/categories | قائمة الفئات | لا |
| POST | /api/categories | إضافة فئة جديدة | نعم |
| DELETE | /api/categories/{id} | حذف فئة | نعم |
| GET | /api/cart | عرض محتويات السلة | نعم |
| POST | /api/cart/items | إضافة منتج للسلة | نعم |
| DELETE | /api/cart/items/{id} | حذف منتج من السلة | نعم |
| PUT | /api/cart/items/{id} | تحديث كمية منتج | نعم |
| DELETE | /api/cart | إفراغ السلة بالكامل | نعم |
| GET | /api/orders | قائمة طلبات المستخدم | نعم |
| GET | /api/orders/{id} | تفاصيل طلب محدد | نعم |
| POST | /api/orders | إنشاء طلب جديد من السلة | نعم |
| GET | /api/payment-methods | قائمة طرق الدفع المتاحة | لا |
| POST | /api/ai/generate-design | إنشاء تصميم بالذكاء الاصطناعي | نعم |
| GET | /api/ai/designs | قائمة تصاميم المستخدم | نعم |
| GET | /api/ai/designs/{id} | تفاصيل تصميم محدد | نعم |

---

## حل المشكلات الشائعة

### مشكلة عدم الاتصال بقاعدة البيانات

إذا واجهت مشكلة في الاتصال بقاعدة البيانات، تحقق أولاً من تشغيل خدمة MySQL في XAMPP. ثم تأكد من صحة اسم قاعدة البيانات ومعلومات الاتصال في ملف .env. أخيراً، تحقق من أن المنفذ 3306 غير مستخدم من تطبيق آخر.

### مشكلة عدم العثور على الحزم

إذاظهرت رسالة خطأ تفيد بعدم العثور على وحدة معينة، فتأكد من تفعيل البيئة الافتراضية وأن جميع الحزم مثبتة. يمكنك إعادة تثبيت الحزم بتنفيذ الأمر pip install -r requirements.txt مرة أخرى.

### مشكلة CORS

إذا واجهت أخطاء CORS رغم أن الخادم مكون للسماح من جميع المصادر، فتأكد من أن الطلبات تتضمن الترويسات الصحيحة，尤其是Authorization header عند الحاجة.

### مشكلة في Gemini API

إذا فشلت طلبات التصميم بالذكاء الاصطناعي، فتأكد من صحة مفتاح API في ملف .env وتحقق من أن لديك رصيد كافٍ في Google Cloud. قد تحتاج أيضاً إلى التحقق من حدود الاستخدام اليومية.

---

## معلومات المشروع

تم تطوير هذا المشروع ليكون قاعدة متينة لمتجر المجوهرات الإلكتروني. الإصدار الحالي يوفر الوظائف الأساسية المطلوبة لتشغيل المتجر، مع إمكانية التوسع في المستقبل لإضافة ميزات جديدة وتحسينات.

---

هذا الدليل يوفر لك كل ما تحتاجه للبدء في استخدام وتطوير هذا المشروع. للمطورين الذين يعملون على الواجهة الأمامية، فإن الأمثلة المقدمة تغطي جميع العمليات الرئيسية التي ستحتاجها لبناء تطبيق متكامل.
