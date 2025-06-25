from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from typing import Any, Dict, Optional

from pydantic import PrivateAttr

from src.tools.base_tool import BaseTool  


class CodeFormatterTool(BaseTool):
    name: str = "code_formatter"
    description: str = "Python kodunu PEP8 standartlarına göre formatlar ve temizler."
    parameters: Optional[dict] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Formatlanacak Python kodu",
            },
            "style": {
                "type": "string",
                "description": "Formatla stili (pep8, black, strict)",
                "enum": ["pep8", "black", "strict"],
                "default": "pep8"
            },
        },
        "required": ["code"],
    }

    _llm: ChatOllama = PrivateAttr()
    _formatter_prompt: PromptTemplate = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm = ChatOllama(
            model="llama3",
            base_url="http://localhost:11434"
        )
        self._formatter_prompt = PromptTemplate.from_template("""
        Aşağıdaki Python kodunu {style} standartlarına göre formatla ve temizle.

        Formatlarken şunları yap:
        1. Doğru indentasyon (4 space)
        2. Satır uzunluğu maksimum 88 karakter
        3. Import sıralaması
        4. Gereksiz boşlukları temizle
        5. Fonksiyon ve class'lar arası 2 satır boşluk
        6. PEP8 naming conventions
        7. Gereksiz parantezleri kaldır

        Orijinal Kod:
        {code}

        Sadece formatlanmış kodu döndür, açıklama ekleme.
        """)

    async def execute(self, **kwargs) -> Dict[str, Any]:
        code = kwargs.get("code", "")
        style = kwargs.get("style", "pep8")
        
        if not code.strip():
            return {
                "error": "Formatlanacak kod boş olamaz",
                "success": False
            }
        
        try:
            prompt = self._formatter_prompt.format(code=code, style=style)
            print(f"Formatting code with {style} style...", flush=True)
            
            formatted_result = self._llm.predict(prompt)
            

            formatted_code = formatted_result.strip()
            if formatted_code.startswith("```python"):
                formatted_code = formatted_code[9:]
            if formatted_code.startswith("```"):
                formatted_code = formatted_code[3:]
            if formatted_code.endswith("```"):
                formatted_code = formatted_code[:-3]
            
            formatted_code = formatted_code.strip()
            
            original_lines = len(code.splitlines())
            formatted_lines = len(formatted_code.splitlines())
            
            return {
                "original_code": code,
                "formatted_code": formatted_code,
                "style_used": style,
                "metrics": {
                    "original_lines": original_lines,
                    "formatted_lines": formatted_lines,
                    "lines_changed": abs(original_lines - formatted_lines)
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"Kod formatlama hatası: {str(e)}",
                "success": False
            }