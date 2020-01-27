from .settings import SETTINGS

def percentage(part, total):
    return 0 if total == 0 else (part / total) * 100

def percentage_str(result):
    return f'''{result
        :.{0 if result == 0 else SETTINGS.DECIMAL_PLACES}f}%'''

if __name__ == "__main__":
    print(percentage(50, 0), percentage(50, 200), sep='\n')
