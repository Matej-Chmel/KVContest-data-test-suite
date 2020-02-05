from typing import Union

def valid_input(prompt='', key_formatter=None):
    """Ask user for input. If not valid, ask again.
    Args:
        prompt (str) opt: Print as input prompt..
        key_formatter (function) opt: 
            Tries to return result of that function with input as argument.
    Returns:
        Return type of key_formatter.
    """
    while True:
        try:
            return key_formatter(input(prompt))
        except ValueError:
            print('I did not understand, sorry.')

def valid_choice(
    source: Union[list, dict], 
    heading='', to_lower=True,
    key_formatter=None,
    prompt='Type name of your chosen item or its index: '
):
    """Display choices to user and ask for an item choice.
    Args:
        source (list | dict): Iterable of items to choose from.
        heading (str) opt: Printed at the top.
        to_lower (bool) opt: If input should be lowercased.
        key_formatter (function) opt: For evaluation, result of key_formatter(input) will be used.
        prompt (str) opt: Print as input prompt.
    Returns:
        object: Item or value of key if source is dict.
    """
    if heading:
        print(heading)
    source_to_lower = [
        item.lower() if isinstance(item, str) else item for item in source
    ] if to_lower else source
    while True:
        print(*[f'{item}: {idx}' for idx, item in enumerate(source)], sep='\n')
        selected = input(prompt)
        try:
            if key_formatter:
                selected = key_formatter(selected)
            elif to_lower:
                selected = selected.lower()
            if selected in source_to_lower:
                return selected if isinstance(source, list) else source[selected]
            selected = int(selected)
            return source[selected] if isinstance(source, list) else list(source.values())[selected]
        except (IndexError, KeyError, ValueError):
            print("Input did not match any of the items or their indexes. Please, try again.")

def yes_no(prompt=''):
    """Prompts user with yes/no question.
    Args:
        prompt (str) opt: Question text. Defaults to ''.
    Returns:
        bool: Yes=True, No=False
    """
    while True:
        if prompt:
            print(prompt)
        answer = input('>>> ').lower()
        if answer in ['y', 'yes', 'ok', '']:
            return True
        if answer in ['n', 'no']:
            return False
        print('Please, answer \'yes\' or \'no\'.')

if __name__ == "__main__":
    print(valid_choice(['A', 'B']))
    print(valid_choice({1: 2, 3: 5}, heading='Choose:', prompt='>>> ', key_formatter=int))
    print(yes_no(prompt='Hey'))
    print(valid_input(prompt='Enter integer: ', key_formatter=int))
