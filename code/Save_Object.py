import pickle as pkl
import os

def save_object(_obj, _dir, _filename):
    os.chdir(_dir)

    with open(_filename + '.obj', 'wb') as outp:
        pkl.dump(_obj, outp)
# End object pick'ling

