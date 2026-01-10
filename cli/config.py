import json
import os
from typing import Any

data = {
        "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        "request_delay": (1.5, 3.5),
        "quantity_pages": 10,
        "path_to_load": os.path.expanduser('~/Downloads')
}



def change_quantity_pages(new_pages: int) -> None:
        """Изменение кол-ва страниц для поиска в json файле"""
        data["quantity_pages"] = new_pages

        with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=8)

def get_value_from_data(key) -> Any:
        """Достаёт необходимое значение из json"""
        global data
        if not os.path.exists("data.json"):
                with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=8)

        with open("data.json", 'r', encoding='utf-8') as f:
                result = json.load(f)
                return result.get(key)




