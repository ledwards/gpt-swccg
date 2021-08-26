import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.organization = "org-D2FBgBhwLFkKAOsgtSp86b4i"
openai.api_key = os.getenv("OPENAI_API_KEY")

questions = [
    "What attribute does Never Tell Me the Odds summate to cause Force Loss?",
    "How many Light Side system cards are there?",

]

for question in questions:
    answer = openai.Answer.create(
        search_model="ada", 
        model="ada", 
        question=question, 
        file="file-TZ7IZkBHPEHgJS8kMFeHK9sa", 
        examples_context="Captain Jean-Luc Picard is a Light Side character card. Captain Jean-Luc Picard is a Federation human. Captain Jean-Luc Picard has power 5. Will Riker is a humam. Will Riker has power 6. Data is an android. Data has power 10.", 
        examples=[
            ["What Power is Jean-Luc Picard?", "Captain Jean Luc Picard is Power 5"],
            ["Which side of the Force is Picard?", "Picard is a Light Side card."],
            ["What race is Captain Jean-Luc Picard?", "Captain Jean-Luc Picard is human."],
            ["Is Jean-Luc Picard a Federation human?", "Yes"],
            ["Is Jean-Luc Picard a Dominion Changeling?", "No"]
            ["Which human has the highest power?", "Captain Jean-Luc Picard"]
            ["Which Federation character has the highest power?", "Data"]
        ], 
        max_rerank=10,
        max_tokens=5,
        stop=["\n", "<|endoftext|>"]
    )
    print(question)
    print(f'> {answer["answers"][0]}')