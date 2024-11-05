from typing import Any, Type, Optional
from embedchain.loaders.notion import NotionLoader
from pydantic import BaseModel, Field
from crewai_tools import RagTool
from distutils.util import strtobool
from notion_client import Client
import os

from dotenv import load_dotenv
load_dotenv()


class FixedNotionSearchToolSchema(BaseModel):
    """Input for NotionSearchTool."""

    search_query: str = Field(
        ...,
        description="Mandatory search query you want to use to search the Notion's page content",
    )


class NotionSearchToolSchema(FixedNotionSearchToolSchema):
    """Input for NotionSearchTool."""

    notion_page_id: str = Field(..., description="Mandatory Notion page you want to search")
    recursive: Optional[str] = Field(..., description="\"True\" or \"False\" Whether to recursively include children of the page in the search")


class NotionSearchTool(RagTool):
    name: str = "Search a Notion page content"
    description: str = (
        "A tool that can be used to semantic search a query from a Notion page content. This is not the Notion API, but instead a tool that can provide semantic search capabilities."
    )
    summarize: bool = False

    notion_client: Client = Field(default_factory=lambda: Client(auth=os.getenv("NOTION_INTEGRATION_TOKEN")))

    args_schema: Type[BaseModel] = NotionSearchToolSchema

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like `Client

    def __init__(self, notion_page_id: Optional[str] = None, recursive: Optional[str] = "False", **kwargs):
        super().__init__(**kwargs)        

        if notion_page_id is not None:
            self.add(notion_page_id=notion_page_id, recursive=recursive)
            self.description = f"A tool that can be used to semantic search a query from the {notion_page_id} Notion page content. This is not the Notion API, but instead a tool that can provide semantic search capabilities."
            self.args_schema = FixedNotionSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        print("in add method, kwargs is", kwargs)
        bool_recursive = bool(strtobool(kwargs.get("recursive", "False")))
        print("bool_recursive is", bool_recursive, type(bool_recursive))
        
        if bool_recursive:
            print("inside if")
            # Recursive call to add all children of the Notion page
            self.add_all_pages_recursively(block_id=kwargs['notion_page_id'])
        else:
            print("inside else")
            # Add only the main page content
            super().add(kwargs['notion_page_id'], data_type="notion")


    # Example function to retrieve all children recursively
    def add_all_pages_recursively(
            self,
            block_id: str,
            depth=0, 
            max_depth=None
            ) -> None:
        """Recursively fetch all child blocks up to max depth."""
        if max_depth is not None and depth >= max_depth:
            return []
        
        print(f"{' ' * depth}Page ID: {block_id}")
        super().add(block_id, data_type="notion")

        children = self.notion_client.blocks.children.list(block_id).get("results", [])

        for child in children:
            if child["type"] == "child_page":
                print("child")
                child_page_id = child["id"]
                self.add_all_pages_recursively(child_page_id, depth + 1, max_depth)

    
    def _before_run(
        self,
        query,
        **kwargs: Any,
    ) -> Any:
        print("in _before_run method, kwargs is", kwargs)
        if "notion_page_id" in kwargs:
            self.add(**kwargs)

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        print("in _run method, kwargs is", kwargs)
        return super()._run(query=search_query, **kwargs)
