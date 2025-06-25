from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from src.models.text_read_request import TextReaderRequest  
from src.container import MCPContainer
from src.models.codel_request import CodeRequest 
from src.tools.code_analysis_tool import CodeAnalysisTool 
from src.tools.code_docstring_tool import CodeDocstringTool  
from src.tools.code_formatter_tool import CodeFormatterTool 
from src.tools.txt_reader_tool import TextReaderTool  

router = APIRouter()

@router.post("/code-review", operation_id="code-review",
             description="Bu endpoint gönderilen kodu analiz eder ve kod incelemesi yapar.")
@inject
async def code_review(
    request: CodeRequest,
    code_analysis_tool: CodeAnalysisTool = Depends(Provide[MCPContainer.code_analysis_tool])
):
    result = await code_analysis_tool(**request.parameters)
    return {"result": result}

@router.post("/code-docstring", operation_id="code-docstring",
             description="Bu endpoint gönderilen kod parçacığı için docstring üretir.")
@inject
async def code_docstring(req: CodeRequest,
             code_docstring_tool: CodeDocstringTool = Depends(Provide[MCPContainer.code_docstring_tool])):
    result = await code_docstring_tool(**req.parameters)
    return {"result": result}

@router.post("/code-formatter", operation_id="code-formatter",
             description="Bu endpoint gönderilen Python kodunu PEP8 standartlarına göre formatlar.")
@inject
async def code_formatter(req: CodeRequest,
             code_formatter_tool: CodeFormatterTool = Depends(Provide[MCPContainer.code_formatter_tool])):
    result = await code_formatter_tool(**req.parameters)
    return {"result": result}

@router.post("/text-reader", operation_id="text-reader",
             description="Bu endpoint text dosyasini okur.")
@inject
async def text_reader(req: TextReaderRequest,
             txt_reader_tool: TextReaderTool = Depends(Provide[MCPContainer.txt_reader_tool])):
    result = await txt_reader_tool(**req.parameters)
    return {"result": result}