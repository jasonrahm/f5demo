

class Configuration(object):
    SECRET_KEY = 'super secret demo key right here. Plaintext FTW!!'

    CODEMIRROR_LANGUAGES = ['tcl']
    # CODEMIRROR_THEME = 'cobalt'
    CODEMIRROR_THEME = 'monokai'
    CODEMIRROR_ADDONS = (
        ('display', 'placeholder'),
    )