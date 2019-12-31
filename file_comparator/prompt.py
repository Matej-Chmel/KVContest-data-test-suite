'''
Input logic.
'''
from file import create_file_from_lines

def yes_no(prompt=''):
    """Prompts user with yes/no question.
    
    Args:
        prompt (str, optional): Question text. Defaults to ''.
    
    Returns:
        bool: Yes=True, No=False
    """    
    if prompt:
        print(prompt)
    answer = input('>>> ')
    if answer.lower() in ['y', 'yes', 'ok', '']:
        return True
    if answer.lower() in ['n', 'no']:
        return False
    print('Please, answer \'yes\' or \'no\'.')
    return yes_no()

def create_file_prompt(prompt, lines, ext=''):
    """Prompts user with question to save lines into file.
    
    Args:
        prompt (str): Question.
        lines (iterable): Lines data.
        ext (str, optional): File extension. Defaults to ''.

    Returns:
        bool: True=File created success, False=user cancelled action
    """           
    if yes_no(prompt):
        if not create_file_from_lines(lines, input('Name: '), ext):
            return create_file_prompt(prompt, lines, ext)
        else:
            return True
    else:
        return False
        