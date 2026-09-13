# Warden 🛡️

نسخه : 1.0.0
سازنده : rV8Cy

یه پروژه‌ی آموزشی پایتونی شامل دو ابزار امنیتی:

## 1. Cipher Toolkit (`cipher_toolkit.py`)
رمزنگاری و شکستن رمزهای کلاسیک:
- **Caesar Cipher**: رمزنگاری/رمزگشایی + کرک با آنالیز فراوانی حروف (بروت‌فورس روی ۲۶ حالت)
- **XOR Cipher**: رمزنگاری/رمزگشایی + کرک تک‌بایتی با همون روش آماری

هدف: نشون دادن اینکه چرا رمزهای بدون entropy کافی به‌راحتی شکسته میشن.

## 2. Security Header Scanner (`header_scanner.py`)
چک کردن وجود هدرهای امنیتی مهم HTTP روی یه وبسایت:
- `Strict-Transport-Security`
- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`
- `Permissions-Policy`

⚠️ **فقط روی سایت‌هایی استفاده کن که خودت مالکشی یا اجازه‌ی تست صریح داری.**

## اجرا

```bash
git clone https://github.com/rV9Cy/Warden-Sec.git
pip install requests
pip install arabic-reshaper
pip install python-bidi
pip install colorama
python3 main.py
```

### چرا این کتابخونه‌های اضافه؟
- `arabic-reshaper` + `python-bidi`: متن فارسی رو در ترمینال درست (چسبیده و راست‌به‌چپ) نمایش میدن.
  بدون این‌ها، خیلی از ترمینال‌ها حروف فارسی رو بریده‌بریده و برعکس نشون میدن.
- `colorama`: رنگ‌بندی خروجی (باکس‌ها، پیام موفقیت/خطا/هشدار) رو در ویندوز/لینوکس/مک یکسان می‌کنه.

از منوی اصلی می‌تونی هر کدوم از دو ابزار رو انتخاب کنی، یا مستقیم:

```bash
python3 cipher_toolkit.py
python3 header_scanner.py
```

## ساختار پروژه
```
warden/
├── main.py              # منوی اصلی
├── ui.py                 # رنگ، باکس و رندر درست فارسی
├── cipher_toolkit.py     # Caesar/XOR + Cracker
├── header_scanner.py     # اسکنر هدرهای امنیتی
└── README.md
```
با عشق تقدیم به شما توسط rV8Cy
