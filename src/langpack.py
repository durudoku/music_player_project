import glob


class I18N:
    def __init__(self, language):
            if language in self.get_available_languages():
                self.load_data_from_file(language)
            else:
                raise NotImplementedError("Unsupported language. Add missing language file.")

    def load_data_from_file(self, lang):
        lang_data = {}
        lang_file = f"data_{lang}.lng"
        with open(file=lang_file, encoding="utf-8") as f:
            for line in f:
                (key, val) = line.strip().split("=")
                lang_data[key] = val

        self.label_login = lang_data["label_login"]
        self.label_email = lang_data["label_email"]
        self.label_password = lang_data["label_password"]
        self.button_login = lang_data["button_login"]
        self.label_dont_have_account = lang_data["label_dont_have_account"]
        self.button_signup = lang_data["button_signup"]
        self.label_signup = lang_data["label_signup"]
        self.label_name = lang_data["label_name"]
        self.label_already_have_account = lang_data["label_already_have_account"]

    @staticmethod
    def get_available_languages():
        language_files = glob.glob("*.lng")
        language_codes = []

        for f in language_files:
            language_code = f.replace("data_", "").replace(".lng", "")
            language_codes.append(language_code)

        return language_codes