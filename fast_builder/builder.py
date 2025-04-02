import os
import shutil
from importlib import resources


def create_folder(path):
    """Создает папку и добавляет __init__.py, если его нет."""
    os.makedirs(path, exist_ok=True)
    init_path = os.path.join(path, "__init__.py")
    if not os.path.exists(init_path):
        open(init_path, "w").close()


def copy_file(src, dest):
    """Копирует файл, если он существует в пакете."""
    # Получаем путь к библиотеке, которая установлена в виртуальном окружении
    package_path = resources.files("fast_builder").joinpath(src)

    # Копируем файл из пакета в целевую папку
    with package_path.open('rb') as src_file:
        with open(dest, 'wb') as dst_file:
            shutil.copyfileobj(src_file, dst_file)
        print(f"Скопирован {src} -> {dest}")


def build_files():
    """
    Создание структуры проекта и копирование стандартных файлов.
    """
    # Указываем корень проекта вручную
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # Это будет папка проекта

    # Основные директории проекта + файлы
    folders = {
        "Dtos": None,
        "Utils": {
            "subfolders": {
                "Config": ["templates/config.py"],
                "Logs": ["templates/logs.py"]
            }
        },
        "Repositories": {
            "files": ["templates/database.py"],  # Файл в Repositories
            "subfolders": {
                "CRUD": ["templates/crud.py"]
            }
        },
        "Services": None,
        "Routing": None
    }

    for folder, content in folders.items():
        folder_path = os.path.join(root_path, folder)  # Путь в корне проекта
        create_folder(folder_path)

        if content:  # Если есть файлы или подкаталоги
            if isinstance(content, dict):  # Если есть файлы + подкаталоги
                if "files" in content:  # Копируем файлы в текущую папку
                    for file in content["files"]:
                        copy_file(file, os.path.join(folder_path, os.path.basename(file)))

                if "subfolders" in content:  # Если есть подкаталоги
                    for subfolder, files in content["subfolders"].items():
                        subfolder_path = os.path.join(folder_path, subfolder)
                        create_folder(subfolder_path)

                        for file in files:
                            copy_file(file, os.path.join(subfolder_path, os.path.basename(file)))

            elif isinstance(content, list):  # Просто список файлов (корень или папка)
                if folder == "root":
                    for file in content:
                        copy_file(file, os.path.join(root_path, os.path.basename(file)))
                for file in content:
                    copy_file(file, os.path.join(folder_path, os.path.basename(file)))

    print("✅ Проект успешно создан!")


if __name__ == "__main__":
    build_files()
