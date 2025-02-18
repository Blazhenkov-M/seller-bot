import re

VALID_KEYWORDS_1 = {"Номер поставки", "Предмет", "Код номенклатуры", "дата продажи"}
VALID_KEYWORDS_2 = {"товар", "штрих-код товара"}


def clean_text(text):
    """Очищает текст от пробелов, невидимых символов и приводит к нижнему регистру."""
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)  # Убираем двойные пробелы
    text = text.replace("\xa0", " ")  # Убираем неразрывные пробелы
    return text


def find_header_row(df):
    """Ищет строку, где находятся заголовки."""
    valid_keywords_lower = {kw.lower().strip() for kw in VALID_KEYWORDS_1 | VALID_KEYWORDS_2}

    best_row = -1
    max_hits = 0

    for i in range(min(20, len(df))):  # Проверяем первые 20 строк (на всякий случай)
        row_values = {clean_text(str(val)) for val in df.iloc[i].dropna().values}
        matches = len(valid_keywords_lower & row_values)  # Сколько совпадений

        if matches > max_hits:
            max_hits = matches
            best_row = i

    return best_row if max_hits > 0 else None  # Если вообще ничего не нашли, вернем None


def contains_valid_keywords(df):
    """Проверяет, содержатся ли ключевые слова в заголовках таблицы."""
    headers = {clean_text(col) for col in df.columns}

    valid_keywords_1_lower = {kw.lower().strip() for kw in VALID_KEYWORDS_1}
    valid_keywords_2_lower = {kw.lower().strip() for kw in VALID_KEYWORDS_2}

    found_1 = [kw for kw in valid_keywords_1_lower if kw in headers]
    found_2 = [kw for kw in valid_keywords_2_lower if kw in headers]

    print("Найденные ключевые слова из VALID_KEYWORDS_1:", found_1)
    print("Найденные ключевые слова из VALID_KEYWORDS_2:", found_2)

    return bool(found_1 or found_2)
