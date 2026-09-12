"""
UI Helpers
-----------
ابزارهای مشترک برای خوشگل کردن خروجی ترمینال:
- رندر درست متن فارسی/عربی (شکل‌دهی حروف + جهت راست‌به‌چپ)
- رنگ‌بندی با colorama
- چاپ باکس و جدول ساده
"""

import shutil
import arabic_reshaper
from bidi.algorithm import get_display
from colorama import Fore, Style, init

init(autoreset=True)  # ریست خودکار رنگ بعد از هر print

VERSION = "1.0.0"
AUTHOR = "rV8Sy"


def fa(text: str) -> str:
    """
    متن فارسی رو برای نمایش درست در ترمینال آماده می‌کنه.
    (بدون این کار، حروف به هم نمی‌چسبن و جهت متن برعکس نشون داده میشه)
    فقط برای رشته‌های خالص فارسی/عربی استفاده کن، نه ترکیب فارسی+انگلیسی زیاد.
    """
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text  # اگه شکست خورد، حداقل خود متن خام نشون داده بشه


def _term_width(default: int = 60) -> int:
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default


def box(title: str, color: str = Fore.CYAN, width: int = None) -> None:
    """چاپ یه باکس عنوان‌دار برای تیترهای اصلی."""
    w = width or min(_term_width(), 60)
    line = "─" * (w - 2)
    print(f"{color}╭{line}╮{Style.RESET_ALL}")
    padded = fa(title).center(w - 2)
    print(f"{color}│{Style.RESET_ALL}{padded}{color}│{Style.RESET_ALL}")
    print(f"{color}╰{line}╯{Style.RESET_ALL}")


def section(title: str, color: str = Fore.YELLOW) -> None:
    """چاپ یه زیرعنوان با خط جداکننده."""
    print(f"\n{color}▸ {fa(title)}{Style.RESET_ALL}")
    print(f"{color}{'─' * min(_term_width(), 40)}{Style.RESET_ALL}")


def success(text: str) -> None:
    print(f"{Fore.GREEN}✔ {fa(text)}{Style.RESET_ALL}")


def error(text: str) -> None:
    print(f"{Fore.RED}✘ {fa(text)}{Style.RESET_ALL}")


def warning(text: str) -> None:
    print(f"{Fore.YELLOW}⚠ {fa(text)}{Style.RESET_ALL}")


def info(text: str) -> None:
    print(f"{Fore.BLUE}ℹ {fa(text)}{Style.RESET_ALL}")


def menu_item(number: str, label: str) -> None:
    print(f"  {Fore.CYAN}{number}{Style.RESET_ALL}) {fa(label)}")


def prompt(text: str) -> str:
    return input(f"{Fore.MAGENTA}› {fa(text)}{Style.RESET_ALL} ")


def kv(key: str, value: str, key_color: str = Fore.WHITE) -> None:
    """چاپ یه جفت کلید-مقدار با تراز خوب."""
    print(f"  {key_color}{fa(key)}:{Style.RESET_ALL} {value}")
