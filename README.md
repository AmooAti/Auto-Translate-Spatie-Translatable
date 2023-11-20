# Auto-Translate spatie/laravel-translatable tool

## Description
This tool is used to translate your already exiting data in your database when you want to use [spatie/laravel-translatable](https://github.com/spatie/laravel-translatable) package.
One of the pain points of using this package is that you have to translate your exiting data manually which is a tedious task.

With this tool you can export your data to a CSV file, translate it using this tool and import it back to your database.

Currently, this tool uses OpenAI API to translate your data.

## How to use

### Run source code
1. Clone the repository
2. Create virtual environment (Recommended, Optional)
```bash
python -m venv venv
```

3. Activate virtual environment (Optional)

    On Windows:
    ```bash
    venv\Scripts\activate.bat
    ```
    On MacOS/Linux:
    ```bash
    source venv/bin/activate
    ```
4. Install dependencies
```bash
pip install -r requirements.txt
```
5. Run the application
```bash
python main.py
```

### Using GUI
1. Enter you OpenAi API key. You can get it from [here](https://platform.openai.com/docs/quickstart/account-setup)
2. Select your model.
3. Choose your csv file.
4. Choose the column that you want to translate.
5. Choose the source language.
6. Choose the target languages.
7. Click on translate button.

## TODO
- [ ] Replace the Google Translate package
- [ ] User can choose whether ID column should be in output file
- [ ] Translate missing languages features
- [ ] Main thread issue, use multithreading to prevent screen freeze during translation and show loader or progress bar
- [ ] Input validation

## Troubleshooting
### Application not running on ubuntu
If you faced the below error
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: linuxfb, vnc, wayland, xcb, minimalegl, offscreen, vkkhrdisplay, eglfs, wayland-egl, minimal.

[1]    260179 IOT instruction (core dumped)  python main.py

```

Try to run the application after running the following command
```bash
sudo apt-get install libxcb-cursor0
```