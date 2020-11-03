from pathlib import Path

import setuptools

with Path("README.md").open("r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi_generator",
    version="0.3.2",
    author="Steven Wang",
    author_email="wangzhou8284@outlook.com",
    description="Used to quickly generate fastapi project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StevenLianaL/fastapi_generator",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
    install_requires=[
        'plac',
        'envoy',
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'databases',
        'aiomysql',
        'mysqlclient',
        'pandas',
        'orm'
    ]
)
