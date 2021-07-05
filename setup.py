from setuptools import setup


def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


setup(
    name="jaccount-cli",
    version="0.0.5",
    url="https://github.com/tc-imba/python-jaccount-cli",
    license="MIT",
    description="A small plugin to help use jaccount login in cli programs.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="tc-imba",
    author_email="liuyh615@126.com",
    maintainer="tc-imba",
    maintainer_email="liuyh615@126.com",
    packages=["jaccount_cli"],
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/tc-imba/python-jaccount-cli/issues",
        "Source": "https://github.com/tc-imba/python-jaccount-cli",
    },
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "pillow",
    ],
)
