from util import hook, web

languages = {
  "af": "Afrikaans",
  "sq": "Albanian",
  "ar": "Arabic",
  "az": "Azerbaijani",
  "eu": "Basque",
  "bn": "Bengali",
  "be": "Belarusian",
  "bg": "Bulgarian",
  "ca": "Catalan",
  "zh-CN": "Simplified Chinese",
  "zh-TW": "Traditional Chinese",
  "hr": "Croatian",
  "cs": "Czech",
  "da": "Danish",
  "nl": "Dutch",
  "en": "English",
  "eo": "Esperanto",
  "et": "Estonian",
  "tl": "Filipino",
  "fi": "Finnish",
  "fr": "French",
  "gl": "Galician",
  "ka": "Georgian",
  "de": "German",
  "el": "Greek",
  "gu": "Gujarati",
  "ht": "Haitian Creole",
  "iw": "Hebrew",
  "hi": "Hindi",
  "hu": "Hungarian",
  "is": "Icelandic",
  "id": "Indonesian",
  "ga": "Irish",
  "it": "Italian",
  "ja": "Japanese",
  "kn": "Kannada",
  "ko": "Korean",
  "la": "Latin",
  "lv": "Latvian",
  "lt": "Lithuanian",
  "mk": "Macedonian",
  "ms": "Malay",
  "mt": "Maltese",
  "no": "Norwegian",
  "fa": "Persian",
  "pl": "Polish",
  "pt": "Portuguese",
  "ro": "Romanian",
  "ru": "Russian",
  "sr": "Serbian",
  "sk": "Slovak",
  "sl": "Slovenian",
  "es": "Spanish",
  "sw": "Swahili",
  "sv": "Swedish",
  "ta": "Tamil",
  "te": "Telugu",
  "th": "Thai",
  "tr": "Turkish",
  "uk": "Ukrainian",
  "ur": "Urdu",
  "vi": "Vietnamese",
  "cy": "Welsh",
  "yi": "Yiddish"
}
@hook.regex(r'do you speak (?P<language>\w*)')
def do_you_speak(bot_input, bot_output):
    language = bot_input.inp['language']
    target = [k for k,v in languages.items() if v.lower() == language.lower()]
    term = "yes, {0}.  Why?".format(bot_input.nick)
    if target:
        translation = translate(target=target, term=term)
        bot_output.say(translation)
    else:
        bot_output.say("No I don't speak %(language)s, {0}.  Do you speak English?" % bot_input.inp)


def translate(origin='en', target='es', term='translate this'):
    url = "https://translate.google.com/translate_a/single"
          #"dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=2&tk=517129|678405&q=do%20you%20speak%20spanish%3F
    #url = "https://translate.google.com/translate_a/t"
    params = {
        'client': 't',
        'sl': origin,
        'tl': target,
        'hl': 'en',
        'ssel': 0,
        'tsel': 0,
        'dt': 'bd',
        'dt':'ex',
        'dt': 'ld',
        'dt': 'md',
        'dt': 'qc',
        'dt': 'rw',
        'dt': 'rm',
        'dt': 'ss',
        'dt': 't',
        'dt': 'at',
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'otf': '2',
        'tk': '517129|678405',
        #'multires': '1',
        #'sc': 1,
        #'uptl': "en",
        'q': term
    }
    response = web.get_json_with_querystring(url, params)
    return response

