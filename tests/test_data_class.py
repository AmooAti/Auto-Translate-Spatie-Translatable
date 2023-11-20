import unittest
import pandas as pd
import os

from jsonschema import validate

from main import Data


class TestData(unittest.TestCase):
    def setUp(self):
        data = {
            'id': [1, 2, 3],
            'name': ['John', 'Jane', 'Joe'],
            'description': ['A person', 'Another person', 'Yet another person']
        }
        self.df = pd.DataFrame(data)

        self.csv_file_path = 'test_data.csv'
        self.df.to_csv(self.csv_file_path, index=False)

        self.data = Data(self.csv_file_path)

    def tearDown(self):
        # remove all csv files in the directory
        for file in os.listdir():
            if file.endswith('.csv'):
                os.remove(file)

    def test_get_headers(self):
        expected_headers = ['id', 'name', 'description']
        self.assertEqual(self.data.get_headers(), expected_headers)

    def test_translate(self):
        source_language = 'en'
        destination_languages = ['de', 'fr']
        columns = ['name', 'description']

        translated_data = self.data.translate_columns_with_open_ai(columns, source_language, destination_languages,
                                                                   # TODO: read from env variable
                                                                   'OPENAI_KEY',
                                                                   'gpt-3.5-turbo')

        output_schema = {'en': "string", 'de': "string", 'fr': "string"}
        try:
            validate(instance=translated_data.iloc[0]['name'], schema=output_schema)
            validate(instance=translated_data.iloc[0]['description'], schema=output_schema)
        except Exception as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()
