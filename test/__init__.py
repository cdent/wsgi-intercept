import os

if os.environ.get('USER') == 'cdent':
    import warnings
    warnings.simplefilter('error')
