import setuptools

setuptools.setup(
    name="menuscraper",
    version="0.0.1",
    author="KyuzoM",
    author_email="zoli@exmple.com",
    description="Meal menu scraper",
    long_description="Find your favorite food at the best price.",
    url="https://github.com/kyuzom/taskedin",
    license="MIT",
    packages=[
        "menuscraper",
    ],
    package_data={
        "menuscraper": ["**/*"],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.10",
)
