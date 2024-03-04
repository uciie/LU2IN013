#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

try:
	with open('package_description.rst', 'r') as file_description:
		description = file_description.read()

except IOError:
	description = "Module 2IN013-Robot"

from setuptools import setup, find_packages

setup(
    name = "robot2IN013",
    version = "1.2022.0",

    description = "Module pour le controleur du Robot GoPiGo3 pour le cours 2IN013-Robot",
    long_description = description,

    author = "Nicolas Baskiotis",
    author_email = "nicolas.baskiotis@sorbonne-universite.fr",

    license = 'MIT',
    url = "https://github.com/baskiotisn/2IN013robot2022",


    packages=find_packages(),
    py_modules = ['robot2IN013'],
)
