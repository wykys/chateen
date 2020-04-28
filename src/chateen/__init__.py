from .database import db
from .loader import Loader, FbLoader, IgLoader
from .main import App

__all__ = [
    'db', 'Loader', 'FbLoader', 'IgLoader', 'App'
]

__version__ = version = '0.1'
__copyright__ = 'Copyright 2020, Chateen'
__author__ = 'Jan Vykydal'
__credits__ = ['Jan Vykydal', 'Filip Kubeček']
