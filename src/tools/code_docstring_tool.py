from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from typing import Any, Dict, Optional

from pydantic import PrivateAttr

from src.tools.base_tool import BaseTool

class CodeDocstringTool(BaseTool):
    name: str = "code_docstring_generator"
    description: str = "Python koduna uygun docstring ekler."
    parameters: Optional[dict] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Docstring eklenecek Python kodu",
            },
        },
        "required": ["code"],
    }

    _llm: ChatOllama = PrivateAttr()
    _docstring_prompt: PromptTemplate = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm = ChatOllama(
            model="llama3",
            base_url="http://localhost:11434"
        )
        self._docstring_prompt = PromptTemplate.from_template("""
            Aşağıdaki Python koduna uygun ve detaylı docstring ekle. Docstring formatı Google tarzında olsun. Kodun içine uygun yerlere yerleştir.
            
            Kod:
            {code}
            
            Çıktı sadece docstring eklenmiş kod olsun.
        """)

    async def execute(self, **kwargs) -> Dict[str, Any]:
        code = kwargs.get("code", "")
        prompt = self._docstring_prompt.format(code=code)
        print(prompt)
        result = self._llm.predict(prompt)
        return {"docstring_added_code": result}