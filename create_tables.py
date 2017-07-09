#!/usr/bin/env python

import os

os.environ.setdefault('TORNADO_MODULE_SETTINGS', 'settings.development')

from hotel_api.contrib.db import Model


def main():
    print('Creating tables...')
    Model.create_all()


if __name__ == '__main__':
    main()
