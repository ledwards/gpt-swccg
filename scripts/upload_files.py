import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.organization = "org-D2FBgBhwLFkKAOsgtSp86b4i"
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.File.create(file=open("../data/cards.jsonl"), purpose='answers')