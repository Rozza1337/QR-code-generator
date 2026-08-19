import argparse
import sys
from pathlib import Path

# Обеспечиваем корректный вывод UTF-8 символов в терминалах Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    import qrcode
    from PIL import Image
except ImportError:
    print("[!] Ошибка: Не установлены необходимые библиотеки.")
    print("Установите их командой: pip install -r requirements.txt")
    sys.exit(1)


def generate_qr(
    data: str,
    output_path: str = "qrcode.png",
    fill_color: str = "black",
    back_color: str = "white",
    box_size: int = 10,
    border: int = 4,
) -> str:
    """
    Генерирует QR-код и сохраняет его в файл.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(output_path)
    return str(Path(output_path).resolve())


def interactive_mode():
    """Интерактивный режим при запуске без аргументов командной строки."""
    print("=" * 45)
    print("     📱 Генератор QR-кодов на Python")
    print("=" * 45)

    data = input("Введите текст или ссылку для QR-кода: ").strip()
    if not data:
        print("[!] Ошибка: Введен пустой текст!")
        return

    filename = input("Имя файла для сохранения (по умолчанию: qrcode.png): ").strip()
    if not filename:
        filename = "qrcode.png"
    elif not filename.endswith(".png"):
        filename += ".png"

    fill = input("Цвет кода (по умолчанию: black): ").strip() or "black"
    bg = input("Цвет фона (по умолчанию: white): ").strip() or "white"

    try:
        saved_file = generate_qr(data, filename, fill, bg)
        print("\n[+] QR-код успешно создан!")
        print(f"📁 Путь к файлу: {saved_file}")
    except Exception as e:
        print(f"\n[!] Произошла ошибка: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Легкий и удобный генератор QR-кодов на Python"
    )
    parser.add_argument(
        "-d", "--data",
        type=str,
        help="Текст или URL-ссылка для кодирования в QR-код"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="qrcode.png",
        help="Имя выходного PNG файла (по умолчанию: qrcode.png)"
    )
    parser.add_argument(
        "--color",
        type=str,
        default="black",
        help="Цвет QR-кода (по умолчанию: black)"
    )
    parser.add_argument(
        "--bg",
        type=str,
        default="white",
        help="Цвет фона (по умолчанию: white)"
    )
    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="Размер точки в пикселях (по умолчанию: 10)"
    )

    args = parser.parse_args()

    # Если аргументы командной строки не переданы — запускаем интерактивный диалог
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        if not args.data:
            parser.error("Укажите данные через аргумент -d / --data или запустите скрипт без аргументов.")
        
        saved_file = generate_qr(
            data=args.data,
            output_path=args.output,
            fill_color=args.color,
            back_color=args.bg,
            box_size=args.size,
        )
        print(f"[+] QR-код сохранен: {saved_file}")


if __name__ == "__main__":
    main()
