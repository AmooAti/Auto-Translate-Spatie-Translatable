import pandas as pd

from openai import OpenAI, AuthenticationError,APIConnectionError
import json


class Data:
    def __init__(self, csv_file_path):
        self.df = pd.read_csv(csv_file_path)

    def get_headers(self):
        return self.df.columns.tolist()

    def translate_columns_with_open_ai(self, columns, source_language, destination_languages, openai_api_key, model, only_missing_langs = False):
        openai_client = OpenAI(
            api_key=openai_api_key
        )
        for index, row in self.df.iterrows():
            for column in columns:
                column_translated = dict()
                # first put the source language in the dictionary
                if only_missing_langs:
                    org_data = json.loads(row[column])
                    for s_lang in org_data:
                        column_translated[s_lang] = org_data[s_lang]
                else:
                    column_translated[source_language] = row[column]
                for lang in destination_languages:
                    try:
                        if only_missing_langs:
                            raw_text = json.loads(row[column])[source_language]
                        else:
                            raw_text = row[column]
                        translated_text = openai_client.chat.completions.create(
                            model=model,
                            messages=[
                                {
                                    "role": "system",
                                    "content": f"You will be provided with a sentence in {source_language}, and your task is to translate it into {lang}. If provided sentence equals to null, output null."
                                },
                                {
                                    "role": "user",
                                    "content": raw_text
                                }
                            ],
                            temperature=0,
                            max_tokens=500,
                        ).choices[0].message.content
                    except AuthenticationError:
                        raise OpenAIException("Invalid OpenAI API key")
                    except APIConnectionError:
                        raise OpenAIException("Connection Error")
                    column_translated[lang] = translated_text
                self.df.at[index, column] = json.dumps(column_translated)

        return self.df


class OpenAIException(Exception):
    pass
