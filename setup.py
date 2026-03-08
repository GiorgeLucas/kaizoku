from setuptools import find_namespace_packages, setup

setup(
    name="kaizoku-cli",
    version="0.1.0",
    py_modules=["main"],
    packages=find_namespace_packages(),
    entry_points={
        "console_scripts": [
            "kaizoku-cli=main:main",
        ],
    },
)
