from dependency_injector import containers, providers

from src.tools.code_analysis_tool import CodeAnalysisTool 
from src.tools.code_docstring_tool import CodeDocstringTool  
from src.tools.txt_reader_tool import TextReaderTool 
from src.tools.text_summerizer_tool import TextSummarizerTool



class MCPContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.routers.agent"])
    code_analysis_tool = providers.Singleton(CodeAnalysisTool)
    code_docstring_tool = providers.Singleton(CodeDocstringTool)
    txt_reader_tool = providers.Singleton(TextReaderTool)
    text_summarizer_tool = providers.Singleton(TextSummarizerTool)
    
