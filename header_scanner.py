"""
Security Header Scanner
-------------------------
یه ابزار ساده برای چک کردن هدرهای امنیتی یه وبسایت.
⚠️ فقط روی سایت‌هایی استفاده کن که خودت مالکشی یا اجازه‌ی تست داری.

هدرهای امنیتی مهمی که چک می‌کنیم:
- Strict-Transport-Security (HSTS)
- Content-Security-Policy (CSP)
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy
"""

import requests
from urllib.parse import urlparse
import ui
from colorama import Fore, Style

SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "description": "اجبار به استفاده از HTTPS (جلوگیری از downgrade attack)",
        "severity": "بالا",
    },
    "Content-Security-Policy": {
        "description": "جلوگیری از حملات XSS با محدود کردن منابع مجاز",
        "severity": "بالا",
    },
    "X-Content-Type-Options": {
        "description": "جلوگیری از MIME-sniffing (باید مقدار nosniff باشه)",
        "severity": "متوسط",
    },
    "X-Frame-Options": {
        "description": "جلوگیری از حملات clickjacking",
        "severity": "متوسط",
    },
    "Referrer-Policy": {
        "description": "کنترل اطلاعاتی که در هدر Referer فرستاده میشه",
        "severity": "پایین",
    },
    "Permissions-Policy": {
        "description": "کنترل دسترسی به قابلیت‌های مرورگر (کمرا، مکان و غیره)",
        "severity": "پایین",
    },
}


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def scan_headers(url: str, timeout: int = 10) -> dict:
    """
    درخواست HEAD/GET به سایت میزنه و هدرهای امنیتی رو چک می‌کنه.
    خروجی: دیکشنری شامل نتیجه‌ی هر هدر.
    """
    url = normalize_url(url)
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("آدرس سایت نامعتبره.")

    try:
        resp = requests.get(url, timeout=timeout, allow_redirects=True)
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"اتصال به سایت ناموفق بود: {e}")

    results = {
        "url": resp.url,
        "status_code": resp.status_code,
        "headers_found": {},
        "headers_missing": [],
        "score": 0,
    }

    for header, info in SECURITY_HEADERS.items():
        value = resp.headers.get(header)
        if value:
            results["headers_found"][header] = value
            results["score"] += 1
        else:
            results["headers_missing"].append(header)

    results["total_checked"] = len(SECURITY_HEADERS)
    return results


def print_report(results: dict):
    ui.box(f"گزارش امنیتی: {results['url']}", color=Fore.MAGENTA)
    ui.kv("کد وضعیت", str(results["status_code"]))

    score = results["score"]
    total = results["total_checked"]
    score_color = Fore.GREEN if score == total else (Fore.YELLOW if score >= total / 2 else Fore.RED)
    print(f"  {Fore.WHITE}{ui.fa('امتیاز')}:{Style.RESET_ALL} {score_color}{score}/{total}{Style.RESET_ALL}")

    if results["headers_found"]:
        ui.section("هدرهای موجود ✅", color=Fore.GREEN)
        for header, value in results["headers_found"].items():
            short_value = value if len(value) <= 80 else value[:77] + "..."
            print(f"  {Fore.GREEN}{header}{Style.RESET_ALL}: {short_value}")

    if results["headers_missing"]:
        ui.section("هدرهای گمشده ❌ (پیشنهاد میشه اضافه بشن)", color=Fore.RED)
        for header in results["headers_missing"]:
            info_ = SECURITY_HEADERS[header]
            sev_color = Fore.RED if info_["severity"] == "بالا" else Fore.YELLOW
            severity_label = ui.fa(f"اهمیت: {info_['severity']}")
            print(f"  {Fore.RED}{header}{Style.RESET_ALL}  "
                  f"[{sev_color}{severity_label}{Style.RESET_ALL}]")
            print(f"      {ui.fa(info_['description'])}")

    print()


def main():
    ui.box(f"Security Header Scanner v{ui.VERSION} 🛰️", color=Fore.MAGENTA)
    ui.warning("فقط روی سایت‌های متعلق به خودت یا با اجازه تست کن.")
    url = ui.prompt("آدرس سایت (مثلاً example.com):").strip()
    try:
        results = scan_headers(url)
        print_report(results)
    except (ValueError, ConnectionError) as e:
        ui.error(f"خطا: {e}")


if __name__ == "__main__":
    main()
