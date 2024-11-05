from notion_client import Client
import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

class TestingNotionClient():
    def __init__(self):
        self.notion_client = Client(auth=os.getenv("NOTION_INTEGRATION_TOKEN"))

    def get_all_pages_recursively(self, page_id: str, depth=0, max_depth=None, **kwargs: Any) -> None:
        """Recursively fetch all pages up to max depth."""
        if max_depth is not None and depth >= max_depth:
            return []

        # Retrieve the main page
        # page = self.notion_client.pages.retrieve(page_id=page_id)
        # print(f"{' ' * depth}Page ID: {page_id} - Title: {page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('text', {}).get('content', '')}")
        # If the page has any child pages, recursively retrieve them
        children = self.notion_client.blocks.children.list(page_id).get("results", [])
        print(f"{' ' * depth}Page ID: {page_id}")
        
        for child in children:
            if child["type"] == "child_page":
                child_page_id = child["id"]
                self.get_all_pages_recursively(child_page_id, depth + 1, max_depth)
        


# Call the method with a Notion page URL or ID
TestingNotionClient().get_all_pages_recursively("fcda1dcb7b094c2990d92db662d79426")
