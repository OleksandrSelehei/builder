import os
import shutil
from importlib import resources


class FilesBuilder:

    def __init__(self):
        # Main project directories + files
        self.__folders = {
            "Dtos": None,
            "Utils": {
                "subfolders": {
                    "Config": ["templates/config.py"],
                    "Logs": ["templates/logs.py"]
                }
            },
            "Repositories": {
                "files": ["templates/database.py"],
                "subfolders": {
                    "CRUD": ["templates/crud.py"]
                }
            },
            "Services": None,
            "Routing": None
        }

    @staticmethod
    def __create_folder(path: str) -> None:
        """Creates a folder and adds __init__.py if it does not exist."""

        os.makedirs(path, exist_ok=True)
        init_path = os.path.join(path, "__init__.py")
        if not os.path.exists(init_path):
            open(init_path, "w").close()

    @staticmethod
    def __copy_file(src: str, dest: str) -> None:
        """Copies a file from the package to the specified project directory."""

        package_path = resources.files("fast_builder").joinpath(src)

        # Copy the file from the package to the target project folder
        with package_path.open('rb') as src_file:
            with open(dest, 'wb') as dst_file:
                shutil.copyfileobj(src_file, dst_file)
            print(f"Скопирован {src} -> {dest}")

    def build_files(self) -> None:
        """
        Create the project structure and copy standard files.
        """

        for folder, content in self.__folders.items():
            folder_path = os.path.join(os.getcwd(), folder)
            self.__create_folder(folder_path)

            if content:
                if isinstance(content, dict):  # If there are files + subdirectories
                    if "files" in content:
                        for file in content["files"]:
                            self.__copy_file(file, os.path.join(folder_path, os.path.basename(file)))

                    if "subfolders" in content:  # If there are subdirectories
                        for subfolder, files in content["subfolders"].items():
                            subfolder_path = os.path.join(folder_path, subfolder)
                            self.__create_folder(subfolder_path)

                            for file in files:
                                self.__copy_file(file, os.path.join(subfolder_path, os.path.basename(file)))

                elif isinstance(content, list):  # Just a list of files (root or folder)
                    if folder == "root":
                        for file in content:
                            self.__copy_file(file, os.path.join(os.getcwd(), os.path.basename(file)))
                    for file in content:
                        self.__copy_file(file, os.path.join(os.getcwd(), os.path.basename(file)))
