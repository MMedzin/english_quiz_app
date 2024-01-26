# make console app with click
# read txt file provided with arguments
# file contains words/phrases separated by new line
# use openai api with gpt-4-turbo-preview model to generate three questions for each word/phrase
# use chat-completion api with initial prompt that explains that:
# questios should be sentences that contain this word/phrase, but hte word is replaced with blank
# only first letter of the phrase is shown before the blank
# save questions in json file in the format of {word: [question1, question2, question3]}
import click
import openai
import json
from pathlib import Path
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def change_word_to_blank(text, word, keep_first_letter=True):
    if keep_first_letter:
        return text.replace(word, f"{word[0]}{'_' * (len(word) - 1)}")
    else:
        return text.replace(word, "_" * len(word))


@click.command()
@click.option("--input", "-i", type=click.Path(exists=True), required=True, help="Path to the input file")
@click.option("--output", "-o", type=click.Path(), required=True, help="Path to the output file")
def generate_questions(input, output):
    with open(input, "r") as f:
        words = f.read().splitlines()
    if Path(output).exists():
        with open(output, "r") as f:
            questions = json.load(f)
    else:
        questions = {}
    for word in tqdm(words):
        if word in questions:
            continue
        messages = [
            {
                "role": "user",
                "content": f'Write three sentences using the phrase "{word}".'
                + ' Each sentence in a new line. No ordinal numbers. Always end sentence with a dot ".".'
                + ' Right after the sentence, in the same line put the "{" symbol and the exact phrase extracted from this sentence (no additional words).',
            }
        ]
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            seed=23,
            messages=messages,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        questions[word] = [
            answer.split("{") for answer in response.choices[0].message.content.split("\n") if answer.strip()
        ]
        print(questions[word])
        questions[word] = [
            (
                change_word_to_blank(question.strip(), word.strip().replace("{", "").replace("}", "")),
                word.strip().replace("{", "").replace("}", ""),
            )
            for question, word in questions[word]
        ]
        with open(output, "w") as f:
            json.dump(questions, f, indent=4)


if __name__ == "__main__":
    generate_questions()
