# -*- coding: utf-8 -*-
from mstranslator import Translator

translator = Translator('hswn_client_id', 'mLmqE4kYtcVddhVG2Vq2MLsSTDbhKCmuxqfsrU7Lj7M=')

def translate(word):
	return translator.translate(word, lang_from='hi', lang_to='en')