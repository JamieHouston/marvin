# from util import hook, web2
# import json
#
# languages = {
#     "af": "Afrikaans",
#     "sq": "Albanian",
#     "ar": "Arabic",
#     "az": "Azerbaijani",
#     "eu": "Basque",
#     "bn": "Bengali",
#     "be": "Belarusian",
#     "bg": "Bulgarian",
#     "ca": "Catalan",
#     "zh-CN": "Simplified Chinese",
#     "zh-TW": "Traditional Chinese",
#     "hr": "Croatian",
#     "cs": "Czech",
#     "da": "Danish",
#     "nl": "Dutch",
#     "en": "English",
#     "eo": "Esperanto",
#     "et": "Estonian",
#     "tl": "Filipino",
#     "fi": "Finnish",
#     "fr": "French",
#     "gl": "Galician",
#     "ka": "Georgian",
#     "de": "German",
#     "el": "Greek",
#     "gu": "Gujarati",
#     "ht": "Haitian Creole",
#     "iw": "Hebrew",
#     "hi": "Hindi",
#     "hu": "Hungarian",
#     "is": "Icelandic",
#     "id": "Indonesian",
#     "ga": "Irish",
#     "it": "Italian",
#     "ja": "Japanese",
#     "kn": "Kannada",
#     "ko": "Korean",
#     "la": "Latin",
#     "lv": "Latvian",
#     "lt": "Lithuanian",
#     "mk": "Macedonian",
#     "ms": "Malay",
#     "mt": "Maltese",
#     "no": "Norwegian",
#     "fa": "Persian",
#     "pl": "Polish",
#     "pt": "Portuguese",
#     "ro": "Romanian",
#     "ru": "Russian",
#     "sr": "Serbian",
#     "sk": "Slovak",
#     "sl": "Slovenian",
#     "es": "Spanish",
#     "sw": "Swahili",
#     "sv": "Swedish",
#     "ta": "Tamil",
#     "te": "Telugu",
#     "th": "Thai",
#     "tr": "Turkish",
#     "uk": "Ukrainian",
#     "ur": "Urdu",
#     "vi": "Vietnamese",
#     "cy": "Welsh",
#     "yi": "Yiddish"
# }
#
#
# def get_language_code(language_name):
#     if len(language_name) == 2:
#         return language_name
#
#     code = [k for k, v in languages.items() if v.lower() == language_name.lower()]
#     if code:
#         return code[0]
#
#     return None
#
#
# @hook.regex(r'do you speak (?P<language>\w*)')
# def do_you_speak(bot_input, bot_output):
#     language_name = bot_input.inp['language']
#     to_language = get_language_code(language_name)
#     sentence = "Yes. Do you speak english, {0}?".format(bot_input.nick)
#     if to_language:
#         translation = translate(sentence, 'en', to_language)
#         bot_output.say(translation)
#     else:
#         bot_output.say("No I don't speak %(language)s, {0}.  Do you speak English?" % bot_input.inp)
#
#
# @hook.regex(r'(?:how do you )?say (?P<sentence>[\"“\w\s\W”]*) in (?P<language>\w*)')
# @hook.regex(r'(?:how do you )?say (?P<sentence>\w*) in (?P<language>\w*)')
# def how_do_you_say(bot_input, bot_output):
#     if hasattr(bot_input, 'groupdict'):
#         translate_parameters = bot_input.groupdict()
#         sentence = translate_parameters["sentence"]
#         language = translate_parameters["language"]
#         to_language = get_language_code(language)
#         result = translate(sentence, 'auto', to_language)
#         bot_output.say(result)
#
#
# def translate(text_to_translate, from_language="auto", to_language=None):
#     phonetic = False
#
#     if from_language is None:
#         from_language = "en"
#
#     text = text_to_translate.strip('" ')
#     page = web2.request(
#         "http://translate.google.com/translate_a/t",
#         modern=True,
#         query={
#             "client": "t",
#             "hl": "en",
#             "sl": from_language,
#             "tl": to_language,
#             "multires": "1",
#             "otf": "1",
#             "ssel": "0",
#             "tsel": "0",
#             "sc": "1",
#             "text": text
#         })
#
#     result = page["text"]
#     while ",," in result:
#         result = result.replace(",,", ",null,")
#     result = result.replace("[,", "[null,")
#     result = result.replace(",]", ",null]")
#
#     try:
#         js = json.loads(result)
#     except ValueError:
#         return "What do you care?"
#
#     if phonetic:
#         translation = js[0][0][3] or js[0][0][0]
#     else:
#         translation = "".join(t[0] for t in js[0])
#
#     return translation.replace(" ,", ",")
#
#
# @hook.regex(r'what languages')
# @hook.command
# def language_list(bot_input, bot_ouput):
#     bot_ouput.say("I know {0}".format(', '.join(languages.values())))