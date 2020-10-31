from pathlib import Path

import setuptools

with Path("README.md").open("r", encoding='utf8') as fh:
    long_description = fh.read()

with Path("requirements.txt").open("r", encoding='utf8') as fh:
    all_requires = [i for i in fh.read().split('\n') if i]

install_requires = [
    'plac'
]

install_requires_with_version = [i for i in all_requires for j in install_requires if j in i]
setuptools.setup(
    name="fastapi_generator",
    version="0.1",
    author="Steven Wang",
    author_email="wangzhou8284@outlook.com",
    description="Used to quickly generate fastapi project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StevenLianaL/fastapi_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
    install_requires=install_requires_with_version,
)
