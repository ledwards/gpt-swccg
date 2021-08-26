import os
from dotenv import load_dotenv
import openai
dirname = os.path.dirname(__file__)

load_dotenv()

openai.organization = "org-D2FBgBhwLFkKAOsgtSp86b4i"
openai.api_key = os.getenv("OPENAI_API_KEY")

cards_file = os.path.join(dirname, '../data/cards.jsonl')
openai.File.create(file=open(cards_file), purpose='answers')