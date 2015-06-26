#!/usr/bin/env python
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from setuptools import setup

setup(name='DirMonitor',
      version='1.0',
      author="ziXiong",
      author_email="quezixiong@qq.com",
      classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      packages=['DirMonitor'],
      platforms=["Any"],
      license="BSD",
      keywords='Directory Monitor',
      description="Set to monitor a directory, call a callback whenever file changed under this directory",
      )