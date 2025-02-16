import argparse
import subprocess

def convert_pbf_to_ffmetadata(pbf_file, ffmetadata_file):
    # Попробуем открыть файл в разных кодировках
    encodings = ['utf-8', 'utf-16', 'latin-1']
    lines = None

    for encoding in encodings:
        try:
            with open(pbf_file, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break  # Если файл успешно прочитан, выходим из цикла
        except UnicodeDecodeError:
            continue

    if lines is None:
        raise ValueError("Не удалось прочитать файл. Возможно, он бинарный или использует неизвестную кодировку.")

    # Обработка глав
    chapters = []
    for line in lines:
        if line.strip() and "=" in line:  # Пропускаем пустые строки
            parts = line.strip().split('=', 1)
            if len(parts) == 2:
                index, data = parts
                if '*' in data:
                    time_ms, title, _ = data.split('*', 2)
                    chapters.append((int(time_ms), title))

    # Запись в ffmetadata
    with open(ffmetadata_file, 'w', encoding='utf-8') as f:
        # Заголовок FFMETADATA
        f.write(";FFMETADATA1\n")
        f.write("title=Пример заголовка\n")  # Замените на нужный заголовок
        f.write("artist=Пример исполнителя\n")  # Замените на нужного исполнителя
        f.write(";Это комментарий\n\n")  # Пример комментария

        # Запись глав
        for i, (start_time, title) in enumerate(chapters):
            end_time = chapters[i + 1][0] if i + 1 < len(chapters) else start_time + 60000  # Последняя глава длится 1 минуту
            f.write("[CHAPTER]\n")
            f.write("TIMEBASE=1/1000\n")
            f.write(f"START={start_time}\n")
            f.write(f"END={end_time}\n")
            f.write(f"title={title}\n\n")

        # Запись раздела [STREAM] (опционально)
        f.write("[STREAM]\n")
        f.write("title=Пример заголовка потока\n")  # Замените на нужный заголовок

def embed_chapters(video_file, ffmetadata_file, output_file):
    # Команда для встраивания глав с помощью ffmpeg
    command = [
        'ffmpeg',
        '-i', video_file,          # Входной видеофайл
        '-i', ffmetadata_file,     # Файл с главами
        '-map_metadata', '1',      # Использовать метаданные из второго файла
        '-codec', 'copy',         # Копировать потоки без перекодирования
        output_file                # Выходной файл
    ]

    # Запуск команды
    try:
        subprocess.run(command, check=True)
        print(f"Главы успешно встроены в файл: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при встраивании глав: {e}")
    except FileNotFoundError:
        print("Ошибка: ffmpeg не найден. Убедитесь, что ffmpeg установлен и доступен в PATH.")

if __name__ == "__main__":
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Конвертирует файл глав .pbf в формат ffmetadata и встраивает главы в видео.")
    parser.add_argument("pbf_file", help="Путь к входному файлу .pbf")
    parser.add_argument("ffmetadata_file", help="Путь к выходному файлу ffmetadata")
    parser.add_argument("--embed", action="store_true", help="Встроить главы в видео")
    parser.add_argument("--video", help="Путь к видеофайлу .mp4 (требуется, если используется --embed)")
    parser.add_argument("--output", help="Путь к выходному видеофайлу (требуется, если используется --embed)")
    args = parser.parse_args()

    # Конвертация pbf в ffmetadata
    convert_pbf_to_ffmetadata(args.pbf_file, args.ffmetadata_file)
    print(f"Конвертация завершена. Файл {args.ffmetadata_file} создан.")

    # Встраивание глав в видео (если указан флаг --embed)
    if args.embed:
        if not args.video or not args.output:
            print("Ошибка: для встраивания глав необходимо указать --video и --output.")
        else:
            embed_chapters(args.video, args.ffmetadata_file, args.output)