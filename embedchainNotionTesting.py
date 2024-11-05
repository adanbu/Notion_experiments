from embedchain import App
from dotenv import load_dotenv
import os
from embedchain.loaders.notion import NotionLoader

load_dotenv()

app = App()

app.add("https://www.notion.so/minorio/Bisan-s-CrewAI-project-11d28c284b8f802f9efcde3634db5b05", data_type="notion")


summary= app.query("What did Bisan do in the RAG space?")

print(summary)
