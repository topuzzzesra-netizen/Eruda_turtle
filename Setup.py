from setuptools import setup

setup(
    name="eruda-turtle",
    version="0.1.0",
    py_modules=["eruda_turtle"],
    author="Yusuf",
    description="Python Turtle için Eruda DevTools Konsol Kütüphanesi",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
