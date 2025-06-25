from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from typing import Any, Dict, Optional
from pydantic import PrivateAttr
from src.tools.base_tool import BaseTool


class TextSummarizerTool(BaseTool):
    name: str = "text_summarizer"
    description: str = "Uzun metinleri Ollama LLM ile özetler ve farklı uzunluk seçenekleri sunar."
    parameters: Optional[dict] = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Özetlenecek metin içeriği",
            },
            "summary_length": {
                "type": "string",
                "description": "Özet uzunluğu seçeneği",
                "enum": ["short", "medium", "long"],
                "default": "medium"
            },
            "language": {
                "type": "string",
                "description": "Özet dili",
                "enum": ["tr", "en"],
                "default": "tr"
            }
        },
        "required": ["text"],
    }

    _llm: ChatOllama = PrivateAttr()
    _summarizer_prompt: PromptTemplate = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._llm = ChatOllama(
            model="llama3",
            base_url="http://localhost:11434"
        )
        self._summarizer_prompt = PromptTemplate.from_template("""
        Aşağıdaki metni {language} dilinde özetle.
        Özet uzunluğu: {length_instruction}

        Özetlerken şunlara dikkat et:
        1. Ana konuları ve önemli noktaları koru
        2. Gereksiz detayları çıkar
        3. Akıcı ve anlaşılır ol
        4. Belirtilen uzunluk sınırlarına uy

        Metin:
        {text}

        Özet:
        """)

    async def execute(self, **kwargs) -> Dict[str, Any]:
        text = kwargs.get("text", "")
        summary_length = kwargs.get("summary_length", "medium")
        language = kwargs.get("language", "tr")
        
        if not text.strip():
            return {
                "error": "Özetlenecek metin boş olamaz",
                "success": False
            }
        
        try:
            print(f"Summarizing text with {summary_length} length in {language}...", flush=True)
            
            # Length instructions mapping
            length_instructions = {
                "short": "Çok kısa özet (2-3 cümle)" if language == "tr" else "Very short summary (2-3 sentences)",
                "medium": "Orta uzunlukta özet (1 paragraf)" if language == "tr" else "Medium length summary (1 paragraph)", 
                "long": "Uzun ve detaylı özet (2-3 paragraf)" if language == "tr" else "Long and detailed summary (2-3 paragraphs)"
            }
            
            # Create prompt
            prompt = self._summarizer_prompt.format(
                text=text,
                language="Türkçe" if language == "tr" else "English",
                length_instruction=length_instructions.get(summary_length, length_instructions["medium"])
            )
            
            # Ollama LLM call
            summary = self._llm.predict(prompt)
            
            # Clean summary (remove markdown if any)
            summary = summary.strip()
            if summary.startswith("**") and summary.endswith("**"):
                summary = summary[2:-2].strip()
            
            # Calculate metrics
            original_word_count = len(text.split())
            summary_word_count = len(summary.split())
            compression_ratio = round(summary_word_count / original_word_count, 3) if original_word_count > 0 else 0
            
            return {
                "original_text": text,
                "summary": summary,
                "summary_length": summary_length,
                "language": language,
                "metrics": {
                    "original_word_count": original_word_count,
                    "summary_word_count": summary_word_count,
                    "compression_ratio": compression_ratio,
                    "original_char_count": len(text),
                    "summary_char_count": len(summary)
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "error": f"Metin özetleme hatası: {str(e)}",
                "success": False
            }