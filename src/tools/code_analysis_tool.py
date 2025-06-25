from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from typing import Any, Dict, Optional

from pydantic import PrivateAttr

from src.tools.base_tool import BaseTool


class CodeAnalysisTool(BaseTool):
    name: str = "code_analysis_cot"
    description: str = "Python kodunu satır satır analiz edip adım adım açıklar."
    parameters: Optional[dict] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Analiz edilecek Python kodu",
            },
        },
        "required": ["code"],
    }

    _llm: ChatOllama = PrivateAttr()
    _analysis_prompt: PromptTemplate = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm = ChatOllama(
            model="llama3",
            base_url="http://localhost:11434"
        )
        self._analysis_prompt = PromptTemplate.from_template("""
         Aşağıdaki Python kodunu satır satır analiz et ve ne yaptığını adım adım açıkla.

         Kod:
         {code}

         Lütfen şu şekilde ilerle:
         1. Her satır için ne yaptığını açıkla.
         2. Kodun genel işlevini özetle.
         3. Eğer varsa, dikkat edilmesi gereken noktaları belirt.
         """)

    async def execute(self, **kwargs) -> Dict[str, Any]:
        code = kwargs.get("code", "")
        prompt = self._analysis_prompt.format(code=code)
        print(prompt)
        result = self._llm.predict(prompt)
        return {"analysis": result}