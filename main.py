import csv

from PyQt6 import QtCore
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QVBoxLayout, \
    QFileDialog, QHBoxLayout, QListWidget, QListWidgetItem, QRadioButton, QCheckBox, QGridLayout, QDialog, QMessageBox
import sys

from data import Data, OpenAIException

languages = [
    {"Afrikaans": "af"},
    {"Albanian": "sq"},
    {"Amharic": "am"},
    {"Arabic": "ar"},
    {"Armenian": "hy"},
    {"Assamese": "as"},
    {"Aymara": "ay"},
    {"Azerbaijani": "az"},
    {"Bambara": "bm"},
    {"Basque": "eu"},
    {"Belarusian": "be"},
    {"Bengali": "bn"},
    {"Bhojpuri": "bho"},
    {"Bosnian": "bs"},
    {"Bulgarian": "bg"},
    {"Catalan": "ca"},
    {"Cebuano": "ceb"},
    {"Chinese (Simplified)": "zh-CN"},
    {"Chinese (Traditional)": "zh-TW"},
    {"Corsican": "co"},
    {"Croatian": "hr"},
    {"Czech": "cs"},
    {"Danish": "da"},
    {"Dhivehi": "dv"},
    {"Dogri": "doi"},
    {"Dutch": "nl"},
    {"English": "en"},
    {"Esperanto": "eo"},
    {"Estonian": "et"},
    {"Ewe": "ee"},
    {"Filipino (Tagalog)": "fil"},
    {"Finnish": "fi"},
    {"French": "fr"},
    {"Frisian": "fy"},
    {"Galician": "gl"},
    {"Georgian": "ka"},
    {"German": "de"},
    {"Greek": "el"},
    {"Guarani": "gn"},
    {"Gujarati": "gu"},
    {"Haitian Creole": "ht"},
    {"Hausa": "ha"},
    {"Hawaiian": "haw"},
    {"Hebrew": "he or iw"},
    {"Hindi": "hi"},
    {"Hmong": "hmn"},
    {"Hungarian": "hu"},
    {"Icelandic": "is"},
    {"Igbo": "ig"},
    {"Ilocano": "ilo"},
    {"Indonesian": "id"},
    {"Irish": "ga"},
    {"Italian": "it"},
    {"Japanese": "ja"},
    {"Javanese": "jv or jw"},
    {"Kannada": "kn"},
    {"Kazakh": "kk"},
    {"Khmer": "km"},
    {"Kinyarwanda": "rw"},
    {"Konkani": "gom"},
    {"Korean": "ko"},
    {"Krio": "kri"},
    {"Kurdish": "ku"},
    {"Kurdish (Sorani)": "ckb"},
    {"Kyrgyz": "ky"},
    {"Lao": "lo"},
    {"Latin": "la"},
    {"Latvian": "lv"},
    {"Lingala": "ln"},
    {"Lithuanian": "lt"},
    {"Luganda": "lg"},
    {"Luxembourgish": "lb"},
    {"Macedonian": "mk"},
    {"Maithili": "mai"},
    {"Malagasy": "mg"},
    {"Malay": "ms"},
    {"Malayalam": "ml"},
    {"Maltese": "mt"},
    {"Maori": "mi"},
    {"Marathi": "mr"},
    {"Meiteilon (Manipuri)": "mni-Mtei"},
    {"Mizo": "lus"},
    {"Mongolian": "mn"},
    {"Myanmar (Burmese)": "my"},
    {"Nepali": "ne"},
    {"Norwegian": "no"},
    {"Nyanja (Chichewa)": "ny"},
    {"Odia (Oriya)": "or"},
    {"Oromo": "om"},
    {"Pashto": "ps"},
    {"Persian": "fa"},
    {"Polish": "pl"},
    {"Portuguese (Portugal, Brazil)": "pt"},
    {"Punjabi": "pa"},
    {"Quechua": "qu"},
    {"Romanian": "ro"},
    {"Russian": "ru"},
    {"Samoan": "sm"},
    {"Sanskrit": "sa"},
    {"Scots Gaelic": "gd"},
    {"Sepedi": "nso"},
    {"Serbian": "sr"},
    {"Sesotho": "st"},
    {"Shona": "sn"},
    {"Sindhi": "sd"},
    {"Sinhala (Sinhalese)": "si"},
    {"Slovak": "sk"},
    {"Slovenian": "sl"},
    {"Somali": "so"},
    {"Spanish": "es"},
    {"Sundanese": "su"},
    {"Swahili": "sw"},
    {"Swedish": "sv"},
    {"Tagalog (Filipino)": "tl"},
    {"Tajik": "tg"},
    {"Tamil": "ta"},
    {"Tatar": "tt"},
    {"Telugu": "te"},
    {"Thai": "th"},
    {"Tigrinya": "ti"},
    {"Tsonga": "ts"},
    {"Turkish": "tr"},
    {"Turkmen": "tk"},
    {"Twi (Akan)": "ak"},
    {"Ukrainian": "uk"},
    {"Urdu": "ur"},
    {"Uyghur": "ug"},
    {"Uzbek": "uz"},
    {"Vietnamese": "vi"},
    {"Welsh": "cy"},
    {"Xhosa": "xh"},
    {"Yiddish": "yi"},
    {"Yoruba": "yo"},
    {"Zulu": "zu"},
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = None
        self.selected_headers = []
        self.include_header_in_output = False
        self.only_missing_langs = False;
        self.gpt_mode_state = 'gpt-3.5-turbo'

        self.setWindowTitle("Prepare your database for spatie/laravel-translatable")
        self.resize(500, 500)

        vbox = QVBoxLayout()
        open_ai_hbox = QHBoxLayout()

        open_ai_hbox.addWidget(QLabel('OpenAI Apikey:'))
        self.open_ai_line_edit = QLineEdit()
        open_ai_hbox.addWidget(self.open_ai_line_edit)

        # choose open AI model
        open_ai_model_hbox = QHBoxLayout()
        self.gpt3_button = QRadioButton('GPT 3.5')
        self.gpt3_button.setChecked(True)
        self.gpt3_button.toggled.connect(lambda: self.select_gpt_mode(self.gpt3_button))
        open_ai_model_hbox.addWidget(self.gpt3_button)
        self.gpt4_button = QRadioButton('GPT 4')
        self.gpt4_button.toggled.connect(lambda: self.select_gpt_mode(self.gpt4_button))
        open_ai_model_hbox.addWidget(self.gpt4_button)
        self.gpt_4_preview_button = QRadioButton('GPT 4 Turbo')
        self.gpt_4_preview_button.toggled.connect(lambda: self.select_gpt_mode(self.gpt_4_preview_button))
        open_ai_model_hbox.addWidget(self.gpt_4_preview_button)
        

        vbox.addLayout(open_ai_hbox)
        vbox.addLayout(open_ai_model_hbox)

        file_hbox = QHBoxLayout()
        # File Labal
        file_label = QLabel("CSV File Path")
        file_hbox.addWidget(file_label)

        # File Line Edit
        self.file_line_edit = QLineEdit()
        file_hbox.addWidget(self.file_line_edit)

        # Browse Button
        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.open_file_dialog)
        file_hbox.addWidget(browse_button)

        vbox.addLayout(file_hbox)
        # Header List
        header_list_label = QLabel("Select the columns you want to translate")
        self.header_list = QListWidget()
        self.header_list.itemChanged.connect(self.on_header_list_item_selection_changed)
        # set a fixed height for the list widget with scroll
        self.header_list.setMaximumHeight(200)
        vbox.addWidget(header_list_label)
        vbox.addWidget(self.header_list)

        # Select source language
        source_language_label = QLabel("Select the source language")
        self.source_language_list = QListWidget()
        for language in languages:
            item = QListWidgetItem(list(language.keys())[0])
            self.source_language_list.addItem(item)
        self.source_language_list.setMaximumHeight(200)
        vbox.addWidget(source_language_label)
        vbox.addWidget(self.source_language_list)

        # Select destination languages
        destination_languages_label = QLabel("Select the destination languages")
        self.destination_languages_list = QListWidget()
        for language in languages:
            item = QListWidgetItem(list(language.keys())[0])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.destination_languages_list.addItem(item)
        self.destination_languages_list.setMaximumHeight(200)
        vbox.addWidget(destination_languages_label)
        vbox.addWidget(self.destination_languages_list)

        options_label = QLabel('Options')
        vbox.addWidget(options_label)
        options_grid = QGridLayout()
        
        # Output with headers or not checkbox
        all_columns_check = QCheckBox('Output with Headers')
        all_columns_check.setChecked(self.include_header_in_output)
        all_columns_check.setToolTip(
            'If checked, the output will have headers. For databases like MySQL make sure this option is not checked!')
        all_columns_check.stateChanged.connect(self.include_header_option_change)
        options_grid.addWidget(all_columns_check, 0, 0)

        # Only translate missing langs or all checkbox
        only_translate_missing_langs_check = QCheckBox('Only Translate missing langs')
        only_translate_missing_langs_check.setChecked(self.only_missing_langs)
        only_translate_missing_langs_check.setToolTip(
            'If checked, only missing translations will translate base on source language.'
        )
        only_translate_missing_langs_check.stateChanged.connect(self.only_missing_langs_change)
        options_grid.addWidget(only_translate_missing_langs_check, 0, 1)

        options_grid.setColumnStretch(1, 1)
        vbox.addLayout(options_grid)

        # Generate Button
        self.generate_button = QPushButton('Translate')
        self.generate_button.clicked.connect(self.generate)
        vbox.addWidget(self.generate_button)

        widget = QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Choose your CSV", QDir().homePath(),
                                                  "CSV (*.csv);;All Files (*.*)")
        self.file_line_edit.setText(filename)
        # currently read only because due to the lack of action when line edit updates
        self.file_line_edit.setReadOnly(True)
        self.data = Data(filename)
        self.header_list.clear()
        self.header_list.setVisible(True)
        for header in self.data.get_headers():
            item = QListWidgetItem(header)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.header_list.addItem(item)

    def on_header_list_item_selection_changed(self):
        self.selected_headers = []
        for index in range(self.header_list.count()):
            item = self.header_list.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                self.selected_headers.append(item.text())

    def select_gpt_mode(self, button):
        if button.text() == 'GPT 3.5':
            self.gpt_mode_state = 'gpt-3.5-turbo'
        elif button.text() == 'GPT 4':
            self.gpt_mode_state = 'gpt-4'
        elif button.text() == 'GPT 4 Turbo':
            self.gpt_mode_state = 'gpt-4-1106-preview'

    def include_header_option_change(self, state):
        if state == 2:
            self.include_header_in_output = True
        else:
            self.include_header_in_output = False

    def only_missing_langs_change(self, state):
        if state == 2:
            self.only_missing_langs = True
        else:
            self.only_missing_langs = False

    @QtCore.pyqtSlot()
    def generate(self):
        # self.generate_button.setText('Generating...')
        # self.generate_button.setEnabled(False)
        source_language = list(languages[self.source_language_list.currentRow()].values())[0]
        destination_languages = []
        for index in range(self.destination_languages_list.count()):
            item = self.destination_languages_list.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                destination_languages.append(list(languages[index].values())[0])
        try:
            translations = self.data.translate_columns_with_open_ai(self.selected_headers, source_language,
                                                                    destination_languages,
                                                                    self.open_ai_line_edit.text(),
                                                                    self.gpt_mode_state,
                                                                    self.only_missing_langs)
        except OpenAIException as e:
            # self.generate_button.setEnabled(True)
            # self.generate_button.setText('Generate')
            # show error message
            error_message_box = QMessageBox(self)
            error_message_box.setWindowTitle('Error')
            error_message_box.setText(str(e))
            error_message_box.setIcon(QMessageBox.Icon.Critical)
            error_message_box.exec()
            return
        # save data to a file same as the input file and end with _translated
        translations.to_csv(self.file_line_edit.text().replace('.csv', '_translated.csv'), index=False,
                            quoting=csv.QUOTE_ALL, header=self.include_header_in_output)
        # self.generate_button.setEnabled(True)
        # self.generate_button.setText('Generate')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
