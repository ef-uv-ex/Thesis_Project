import os

def build_directories():
    """
    Builds directories variabels that are used to find data

    Input:
        Empty
    Output:
        ROOT = root directory for the program
        dir_DATA = data directory
        dir_FIG = figures directory
        dir_MWIR = mwir data directory
        dir_LWIR = lwir data directory
    """

    PATH = os.path.dirname(__file__)
    os.chdir(PATH)
    os.chdir('..')
    _ROOT = os.getcwd()
    _dir_DATA = os.path.join(_ROOT, 'data')
    _dir_FIG = os.path.join(_ROOT, 'figures')

    return (_ROOT, _dir_DATA, _dir_FIG)
# End directory builder