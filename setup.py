from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="pytest-variant",
    author="Balazs Eszes",
    author_email="c4deszes@gmail.com",
    description="Variant support for Pytest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c4deszes/pytest-variant",
    packages=find_packages(),
    license='MIT',
    keywords=['pytest', 'variant'],
    entry_points={
        "pytest11": ["variant = pytest_variant.plugin"]
    },
    classifiers=[
        "Framework :: Pytest",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    project_urls={
        "Documentation": "https://github.com/c4deszes/pytest-variant",
        "Source Code": "https://github.com/c4deszes/pytest-variant",
    }
)
