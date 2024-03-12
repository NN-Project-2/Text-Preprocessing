import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import csv
from extraction import tag_text

#####################################################################
#=======================================================================

"""
    "Raw Text",
    "Text",
    "phone_numbers",
    "date_and_year",
    "Emoji",
    "Punctuation",
    "Symbols",
    "currency_symbols",
    "urls",
    "Mentions",
    "emails",
    "Hashtags",
    "units_of_time",
    "Measurements"
"""
#####################################################################
#=====================================================================

input_text=input("Enter the Text here ....")

out=tag_text(input_text)

print("Tagged Text :",out)

