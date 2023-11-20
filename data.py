import pandas as pd

from openai import OpenAI, AuthenticationError
import json


class Data:
    def __init__(self, csv_file_path):
        self.df = pd.read_csv(csv_file_path)

    def get_headers(self):
        return self.df.columns.tolist()

    def translate_columns_with_open_ai(self, columns, source_language, destination_languages, openai_api_key, model):
        openai_client = OpenAI(
            api_key=openai_api_key
        )
        for index, row in self.df.iterrows():
            for column in columns:
                column_translated = dict()
                # first put the source language in the dictionary
                column_translated[source_language] = row[column]
                for lang in destination_languages:
                    try:
                        translated_text = openai_client.chat.completions.create(
                            model=model,
                            messages=[
                                {
                                    "role": "system",
                                    "content": f"You will be provided with a sentence in {source_language}, and your task is to translate it into {lang}."
                                },
                                {
                                    "role": "user",
                                    "content": row[column]
                                }
                            ],
                            temperature=0,
                            max_tokens=500,
                        ).choices[0].message.content
                    except AuthenticationError:
                        raise OpenAIException("Invalid OpenAI API key")
                    column_translated[lang] = translated_text
                self.df.at[index, column] = json.dumps(column_translated)

        return self.df


class OpenAIException(Exception):
    pass
