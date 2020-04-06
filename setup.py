from setuptools import setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


setup(
    name="quoras",
    version="1.0.0",
    description="A Python package collect data from Quora.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DiptoDas8/quoras",
    author="Dipto Das",
    author_email="dipto.cse.buet@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["quoras"],
    include_package_data=True,
    install_requires=["selenium", "bs4", "lxml"],
    entry_points={
        
        ]
    },
)