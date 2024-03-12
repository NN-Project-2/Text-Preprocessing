
import re


def extract_text(input_text):
    excluded_patterns = [
        r'\d',  # Numbers
        r'\b(?:\+\d{1,2}\s?)?(\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})\b',  # Phone Numbers
        r'\b\d{4}-\d{2}-\d{2}\b',  # Date and Year
        r'[^\w\s,\u0900-\u0DFF\u0B80-\u0BFF\u0C80-\u0CFF\u0D00-\u0D7F\u0E00-\u0E7F\u0A80-\u0AFF\u0964\u2013]',  # Emoji
        r'[^\w\s\u0900-\u0DFF\u0B80-\u0BFF\u0C80-\u0CFF\u0D00-\u0D7F\u0E00-\u0E7F\u0A80-\u0AFF\u0964\u2013]',  # Punctuation
        r'[^\w\s%\u0900-\u0DFF\u0B80-\u0BFF\u0C80-\u0CFF\u0D00-\u0D7F\u0E00-\u0E7F\u0A80-\u0AFF\u0964\u2013]',  # Symbols like % and @
        r'[$€£]',  # Currency Symbols
        r'https?://\S+',  # URL
        r'\b@\w+',  # Mentions/reference
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b#\w+',  # Hashtags
        r'\b\d+\s?\w+\b',  # Units of Time
        r'\b\d+\s?\w+\b'  # Measurements
    ]

    pattern = '|'.join(excluded_pattern for excluded_pattern in excluded_patterns)
    extract = re.sub(fr'(?i){pattern}', ' ', input_text)
    final_data = re.sub(r'\s+', ' ', extract).strip()  # Replace multiple spaces with a single space
    return final_data.lower()



def extract_phone_numbers(input_text):
    phone_numbers = re.findall(r'\+\d{1,3}\s?\d+[-.\s]?\d+[-.\s]?\d{1,9}', input_text)
    return phone_numbers


def extract_date_and_year(input_text):
    dates = re.findall(r'\b\d{1,4}[-./]\d{1,2}[-./]\d{1,4}\b', input_text)
    return dates

def extract_emoji(input_text):
    emojis = re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF\U00002300-\U000023FF\U00002B50]+', input_text)
    return emojis

# def extract_punctuation(input_text):
#     punctuation = re.findall(r'[^\w\s]', input_text)
#     return punctuation

def extract_symbols(input_text):
    symbols = re.findall(r'(?<!\S)[%@](?!\S)', input_text)
    return symbols

def extract_currency_symbols(input_text):
    currency_symbols = re.findall(r'[$€£]', input_text)
    return currency_symbols

def extract_urls(input_text):
    urls = re.findall(r'https?://\S+', input_text)
    return urls

def extract_mentions(input_text):
    mentions = re.findall(r'(?<!\S)(@\w+)', input_text)
    return mentions

def extract_emails(input_text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', input_text)
    return emails

def extract_hashtags(input_text):
    hashtags = re.findall(r'#\w+', input_text)
    return hashtags

def extract_units_of_time(input_text):
    units_of_time = re.findall(r'\b(\d+\s?(?:hours?|minutes?|hrs|secs?))\b', input_text, flags=re.IGNORECASE)
    return units_of_time

def extract_measurements(input_text):
    measurements = re.findall(r'\b(\d+\s?(?:kg|gram|meters?))\b', input_text, flags=re.IGNORECASE)
    return measurements


def tag_text(input_text):
    patterns_and_tags = [
        (r'([\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+)', '<E_s:{}><E_e>'),  # Emojis
        (r'\b(?:\+\d{1,2}\s?)?(\d{10,11})\b', '<P_s:{}><P_e>'),  # Phone Numbers with 10 or 11 digits
        (r'\b\d+\b', '<N_s:{}><N_e>'),  # Numbers
    ]

    matches = []
    remaining_text = input_text

    for pattern, tag_template in patterns_and_tags:
        for match in re.finditer(pattern, remaining_text, flags=re.UNICODE):
            if match.lastindex is not None:
                matches.append((match.start(), match.end(), tag_template.format(match.group(match.lastindex))))
            else:
                matches.append((match.start(), match.end(), tag_template.format(match.group(0))))

    matches.sort(key=lambda x: x[0])  

    result = []
    last_end = 0

    for match_start, match_end, tag in matches:
        
        if match_start < last_end:
            continue

        result.append('<T_s>' + remaining_text[last_end:match_start].strip() + '<T_e>')
        result.append(tag)
        last_end = match_end

    if last_end < len(remaining_text):
        result.append('<T_s>' + remaining_text[last_end:].strip() + '<T_e>')

    result = [tag for tag in result if '<T_s>' not in tag or '<T_e>' not in tag or tag != '<T_s><T_e>']

    return result


