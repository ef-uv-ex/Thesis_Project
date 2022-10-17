

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class usr_msg:
    warno = 'warno'
    prompt = 'prompt'
    notice = 'notice'
    fail = 'fail'
# %% Functions


def user_message(_text, _type):

    if _type == 'warno':
        print(bcolors.WARNING + _text.center(len(_text)*2).capitalize() + bcolors.ENDC + '\n', flush=True)
    elif _type == 'prompt':
        print(bcolors.OKGREEN + _text.center(len(_text)*2) + bcolors.ENDC + '\n', flush=True)
    elif _type == 'notice':
        print(bcolors.OKBLUE + _text + bcolors.ENDC + '\n', flush=True)
    elif _type == 'fail':
        print(bcolors.FAIL + _text + bcolors.ENDC + '\n', flush=True)
