import os
import shutil
import re

from src.core.config import UPLOAD_DIR, ALLOWED_IMAGE_EXTENSIONS


def sanitize_filename(name: str) -> str:
    name = name.replace(' ', '-')
    # Удаляем все символы, кроме букв, цифр, дефиса, подчеркивания и точки
    return re.sub(r'[^a-zA-Zа-яА-Я0-9\-_.]', '', name)


async def upload_file(file, filename: str | None, file_type: str) -> str:
    extension = os.path.splitext(file.filename)[1].lower()

    if file_type == "image":
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(
                f"Недопустимый формат изображения. Поддерживаемые форматы: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            )

        base_name = filename if filename else file.filename
        base_name = os.path.splitext(base_name)[0]  # Убираем расширение
        sanitized_name = sanitize_filename(base_name)
        new_name = f"{sanitized_name}.jpg"
        file_location = UPLOAD_DIR / f"images/{new_name}"

    elif file_type == "document":
        if extension != ".pdf":
            raise ValueError("Допускается только формат PDF")

        base_name = filename if filename else file.filename
        base_name = os.path.splitext(base_name)[0]
        sanitized_name = sanitize_filename(base_name)
        new_name = f"{sanitized_name}.pdf"
        file_location = UPLOAD_DIR / f"documents/{new_name}"

    else:
        raise ValueError("Недопустимый тип файла")

    with file_location.open("wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return new_name
