# ⚡ Volt Language (Alpha Release)

**Volt** هي لغة برمجة مبسطة ومفتوحة المصدر مصممة خصيصاً لتسهيل بناء وإدارة أجهزة إنترنت الأشياء (IoT) والسيرفرات المحلية عادية الأداء بأسلوب غاية في الخفة والسرعة.

## 🚀 فكرة اللغة (Concept)
تأخذ **Volt** الكود النظيف والمبسط (المستوحى من سهولة البايثون) وتقوم بتحويله وتوليده (Transpilation) إلى كود C++ خالص عالي الأداء، ثم تجميع النظام برمجياً لإنتاج ملف تنفيذي ثنائي (Binary) يعمل مباشرة على المعالج والذاكرة بأقصى سرعة ممكنة دون الحاجة لسيرفر خارجي أو بيئة تشغيل معقدة.

---

## 💻 مثال على الكود (Code Example)

بإمكان المطور كتابة هذا الكود البسيط في ملف `app.vl`:

```text
# ترحيب وتعريف المتغيرات لغة فولت
print "--- Welcome to Volt Environment ---"

traffic_load = 45.8

if traffic_load > 40.0:
    print "Status: Threshold breached! Deploying server via Volt..."
    start_server 8080
else:
    print "Status: Optimal load."
🛠️ طريقة التشغيل والاستخدام (How to Run)
​1. المتطلبات الأساسية (Prerequisites)
​تأكد من تثبيت بايثون ومترجم C++ على جهازك:
​على الحاسوب: g++ (GCC Compiler)
​على الأندرويد (Termux): pkg install python clang -y
​2. تشغيل المترجم (Compile)
​قم بتشغيل ملف المحرك ليقوم بقراءة وترجمة كود اللغه تلقائياً: python volt.py

3. تنفيذ البرنامج الناتج (Run Executable)
على أنظمة Linux/Android: ./volt_app
على أنظمة Windows: volt_app.exe
👤 المطور الرئيسي (Lead Architect)
علي أحمد عبد الحسين زركي (Ali Ahmed Abdul Hussein Zarki)
يوزر الانستكرام: ialidev
الكلية: طالب هندسة حاسوب - جامعة الإمام الكاظم (ع)، أقسام ميسان.
