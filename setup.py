from setuptools import setup, find_packages

setup(
    name="fast_builder",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={"fast_builder": ["templates/*"]},  # Добавляем файлы из templates/
    entry_points={
        "console_scripts": [
            "build-my-project=my_package.builder:build_files",  # Добавляем CLI-команду
        ],
    },
)