from dependency_injector import containers, providers

from src.tools.code_analysis_tool import CodeAnalysisTool 
from src.tools.code_docstring_tool import CodeDocstringTool  
from src.tools.code_formatter_tool import CodeFormatterTool
from src.tools.txt_reader_tool import TextReaderTool 


class MCPContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.routers.agent"])
    code_analysis_tool = providers.Singleton(CodeAnalysisTool)
    code_docstring_tool = providers.Singleton(CodeDocstringTool)
    code_formatter_tool = providers.Singleton(CodeFormatterTool)  
    txt_reader_tool = providers.Singleton(TextReaderTool)