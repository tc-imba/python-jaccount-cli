from setuptools import setup

setup(
    name="jaccount-cli",
    version="0.0.1",
    packages=["jaccount_cli"],
    include_package_data=True,
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "pillow",
    ],
)
