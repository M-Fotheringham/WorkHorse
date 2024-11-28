import os


def name_replacer(d, original_text, new_text):

    for root, dirs, files in os.walk(d):
        for filename in files:
            if original_text in filename:
                original_name = f"{root}\\{filename}"

                new_name = original_name.replace(original_text, new_text)

                os.rename(original_name, new_name)
