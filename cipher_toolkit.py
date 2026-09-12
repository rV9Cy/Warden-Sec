"""
Cipher Toolkit - Caesar & XOR Cipher + Cracker
------------------------------------------------
یه ابزار آموزشی برای رمزنگاری و شکستن رمزهای ساده‌ی کلاسیک.
هدف: فهم اینکه چرا رمزهای ساده (بدون کلید تصادفی و طولانی) امن نیستن.
"""

import string
import ui
from colorama import Fore, Style

ENGLISH_LETTER_FREQ = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
    's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
    'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07
}


# ---------------------- Caesar Cipher ----------------------

def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


def _score_text(text: str) -> float:
    """
    امتیازدهی به متن بر اساس شباهت فراوانی حروف به زبان انگلیسی.
    نکته‌ی مهم: امتیاز رو در نسبت (حروف/کل کاراکترها) ضرب می‌کنیم تا
    متن‌هایی که بیشترشون کاراکتر بی‌معنی/غیرقابل‌چاپه (نتیجه‌ی کلید غلط)
    امتیاز مصنوعی بالا نگیرن.
    """
    if not text:
        return 0.0
    letters = [c.lower() for c in text if c.isalpha()]
    if not letters:
        return 0.0

    printable = sum(1 for c in text if c.isprintable())
    letter_density_penalty = printable / len(text)  # جریمه‌ی کاراکترهای غیرقابل‌چاپ
    letter_density = len(letters) / len(text)
    freq_score = sum(ENGLISH_LETTER_FREQ.get(ch, 0) for ch in letters) / len(letters)
    return freq_score * letter_density * letter_density_penalty


def caesar_crack(ciphertext: str, top_n: int = 3):
    """بروت‌فورس روی 26 حالت ممکن + رتبه‌بندی با فراوانی حروف."""
    candidates = []
    for shift in range(26):
        decoded = caesar_decrypt(ciphertext, shift)
        score = _score_text(decoded)
        candidates.append((shift, score, decoded))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[:top_n]


# ---------------------- XOR Cipher ----------------------

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return xor_encrypt(data, key)  # XOR با همون کلید برعکس میشه


def xor_crack_single_byte(ciphertext: bytes, top_n: int = 3):
    """
    فرض: کلید فقط یک بایته (single-byte XOR).
    همه‌ی 256 حالت رو امتحان می‌کنیم و بر اساس فراوانی حروف امتیاز میدیم.
    """
    candidates = []
    for key_byte in range(256):
        try:
            decoded = xor_decrypt(ciphertext, bytes([key_byte])).decode('utf-8', errors='ignore')
        except Exception:
            continue
        score = _score_text(decoded)
        candidates.append((key_byte, score, decoded))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[:top_n]


# ---------------------- Demo / CLI ----------------------

def _menu():
    ui.menu_item("3", "Caesar Crack (بدون دونستن کلید)")
    ui.menu_item("4", "XOR Encrypt/Decrypt")
    ui.menu_item("5", "XOR Crack (single-byte key)")
    ui.menu_item("0", "خروج")


def main():
    while True:
        ui.box(f"Cipher Toolkit v{ui.VERSION} 🔐", color=Fore.CYAN)
        ui.menu_item("1", "Caesar Encrypt")
        ui.menu_item("2", "Caesar Decrypt")
        _menu()
        choice = ui.prompt("انتخاب کن:").strip()

        if choice == '1':
            text = ui.prompt("متن ساده:")
            shift = int(ui.prompt("مقدار شیفت (0-25):"))
            ui.section("نتیجه")
            ui.kv("متن رمزشده", caesar_encrypt(text, shift))

        elif choice == '2':
            text = ui.prompt("متن رمزشده:")
            shift = int(ui.prompt("مقدار شیفت (0-25):"))
            ui.section("نتیجه")
            ui.kv("متن ساده", caesar_decrypt(text, shift))

        elif choice == '3':
            text = ui.prompt("متن رمزشده برای کرک:")
            results = caesar_crack(text)
            ui.section("بهترین حدس‌ها")
            for shift, score, decoded in results:
                print(f"  {Fore.CYAN}shift={shift:2d}{Style.RESET_ALL}  "
                      f"{Fore.YELLOW}score={score:5.2f}{Style.RESET_ALL}  -> {decoded}")

        elif choice == '4':
            text = ui.prompt("متن (utf-8):")
            key = ui.prompt("کلید (رشته):")
            out = xor_encrypt(text.encode(), key.encode())
            ui.section("نتیجه")
            ui.kv("خروجی (hex)", out.hex())
            ui.info("برای برگردوندن، همین hex رو با همون کلید دوباره XOR کن.")

        elif choice == '5':
            hex_input = ui.prompt("متن رمزشده به صورت hex:").strip()
            try:
                data = bytes.fromhex(hex_input)
            except ValueError:
                ui.error("hex نامعتبره!")
                continue
            results = xor_crack_single_byte(data)
            ui.section("بهترین حدس‌ها")
            for key_byte, score, decoded in results:
                print(f"  {Fore.CYAN}key=0x{key_byte:02x}{Style.RESET_ALL}  "
                      f"{Fore.YELLOW}score={score:5.2f}{Style.RESET_ALL}  -> {decoded!r}")

        elif choice == '0':
            ui.success("خدافظ داداش!")
            break
        else:
            ui.error("گزینه نامعتبره.")


if __name__ == "__main__":
    main()
