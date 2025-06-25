import os
from typing import Any, Dict, Optional

from pydantic import PrivateAttr

from src.tools.base_tool import BaseTool


class TextReaderTool(BaseTool):
    name: str = "text_reader"
    description: str = "Assets klasöründeki bir .txt dosyasını okuyup içeriğini döner."
    parameters: Optional[dict] = {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "Okunacak txt dosyasının adı (örnek: ornek.txt)",
            },
        },
        "required": ["filename"],
    }

    _assets_dir: str = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._assets_dir = os.path.join(os.getcwd(), "Assets")


    async def execute(self, **kwargs) -> Dict[str, Any]:
        filename = kwargs.get("filename", "")
        file_path = os.path.join(self._assets_dir, filename)

        if not filename.endswith(".txt"):
            return {"error": "Yalnızca .txt uzantılı dosyalar desteklenmektedir."}

        if not os.path.exists(file_path):
            return {"error": f"{filename} dosyası Assets klasöründe bulunamadı."}

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            return {"content": content}
        except Exception as e:
            return {"error": f"Dosya okunurken hata oluştu: {str(e)}"}