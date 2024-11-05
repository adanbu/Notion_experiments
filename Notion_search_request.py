import requests

# Replace with your actual Notion API key
notion_api_key = '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'

# Headers for authorization and content type
headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Data payload for the search request
data = {

    "sort": {
        "direction": "ascending",
        "timestamp": "last_edited_time"
    }
}

# Send POST request to the Notion API
response = requests.post("https://api.notion.com/v1/search", headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the response JSON
    results = response.json()
    print("Search Results:", results)
else:
    print("Error:", response.status_code, response.text)
