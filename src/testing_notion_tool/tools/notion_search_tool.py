from typing import Any, List, Optional, Type

from embedchain.loaders.notion import NotionLoader
from pydantic import BaseModel, Field

from crewai_tools import RagTool


class FixedNotionSearchToolSchema(BaseModel):
    """Input for NotionSearchTool."""

    search_query: str = Field(...,
        description="Mandatory search query you want to use to search the Notion's page content",
    )


class NotionSearchToolSchema(FixedNotionSearchToolSchema):
    """Input for NotionSearchTool."""


    notion_page_id: str = Field(..., description="Mandatory Notion page you want to search")
    recursive: bool = Field(False, description="Whether to recursively include children of the page in the search")
    # content_types: List[str] = Field(
    #     ...,
    #     description="Mandatory content types you want to be included search, options: [code, repo, pr, issue]",
    # )


class NotionSearchTool(RagTool):
    name: str = "Search a Notion repo's content"
 
    description: str = (
        "A tool that can be used to semantic search a query from a Notion page's content. This is not the Notion API, but instead a tool that can provide semantic search capabilities."
    ) 
     
    
    summarize: bool = False
    args_schema: Type[BaseModel] = NotionSearchToolSchema

    # content_types: List[str]

    def __init__(self, notion_page_id: Optional[str] = None, **kwargs):

        super().__init__(**kwargs)
        if notion_page_id is not None:
    
            kwargs["data_type"] = "notion"
       
            kwargs["loader"] = NotionLoader()
        

            self.add(notion_page_id=notion_page_id)
        
            self.description = f"A tool that can be used to semantic search a query from the {notion_page_id} Notion page content. This is not the Notion
         API, but instead a tool that can provide semantic search capabilities."
        
         
            self.args_schema = FixedNotionSearchToolSchema
        
            self._generate_description()

    def add(
        self,
        notion_page_id: str,
        **kwargs: Any,
    ) -> None:
        super().add(kwargs=kwargs)

    def _before_run(
        self,
        **kwargs: Any,
    ) -> Any:
        if "notion_page_id" in kwargs:
            self.add( notion_page_id=kwargs["notion_page_id"])
               
    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
