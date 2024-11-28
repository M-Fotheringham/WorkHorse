import os


def name_replacer(d, original_text, new_text, inside):

    for root, dirs, files in os.walk(d):
        for filename in files:
            if original_text in filename:
                
                original_name = f"{root}\\{filename}"

                new_name = original_name.replace(original_text, new_text)

                # Not sure when this is necessary
                if inside and filename.endswith(".txt"):
                    with open(original_name, "r") as file:
                        content = file.read()
                    
                    new_content = content.replace(original_text, new_text)

                    with open(original_name, "w") as file:
                        file.write(new_content)

                os.rename(original_name, new_name)
