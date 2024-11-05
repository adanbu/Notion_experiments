import requests

def get_notion_page_content(api_token, page_id):
    # url = f"https://api.notion.com/v1/pages/{page_id}"
    block_id=page_id
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Notion-Version": "2022-06-28"  # Check Notion docs for the latest version
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve page content. Status code: {response.status_code}")
        print(response.json())
        return None

# Replace 'your_api_token' with your Notion API token
# Replace 'your_page_id' with the ID of the Notion page you want to retrieve
api_token = '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'
page_id = '12828c284b8f8000829bd8e545e980dd'

page_content = get_notion_page_content(api_token, page_id)
if page_content:
    print(page_content)
