def shorter_number(number):
    if number < 1000:
        return str(number)
    elif number < 1000000:
        magnitude = 10 ** (len(str(number // 1000)) - 1)
        formatted_number = number / 1000
        return f"{formatted_number:.1f}K" if formatted_number >= 10 else f"{formatted_number * magnitude / magnitude:.1f}K"
    elif number < 1000000000:
        magnitude = 10 ** (len(str(number // 1000000)) - 1)
        formatted_number = number / 1000000
        return f"{formatted_number:.1f}M" if formatted_number >= 10 else f"{formatted_number * magnitude / magnitude:.1f}M"
    else:
        magnitude = 10 ** (len(str(number // 1000000000)) - 1)
        formatted_number = number / 1000000000
        return f"{formatted_number:.1f}B" if formatted_number >= 10 else f"{formatted_number * magnitude / magnitude:.1f}B"