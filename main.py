"""
Warden - Main Menu
------------------------------
اجرای متمرکز دو ابزار:
1) Cipher Toolkit (Caesar/XOR + Cracker)
2) Security Header Scanner
"""

import ui
from colorama import Fore
import cipher_toolkit
import header_scanner


def main():
    ui.box(f"Warden v{ui.VERSION} 🛡️", color=Fore.CYAN, width=44)
    ui.info(f"ساخته شده توسط {ui.AUTHOR}")

    while True:
        print()
        ui.menu_item("1", "Cipher Toolkit (رمزنگاری Caesar/XOR)")
        ui.menu_item("2", "Security Header Scanner (چک هدرهای امنیتی سایت)")
        ui.menu_item("0", "خروج")

        choice = ui.prompt("انتخاب کن:").strip()

        if choice == '1':
            cipher_toolkit.main()
        elif choice == '2':
            header_scanner.main()
        elif choice == '0':
            ui.success("خدافظ داداش! 👋")
            break
        else:
            ui.error("گزینه نامعتبره.")


if __name__ == "__main__":
    main()
