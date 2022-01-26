import setuptools

setuptools.setup(
    name="pyhwjser",
    version="0.0.4",
    author="KyuzoM",
    author_email="kyuzom@googlegroups.com",
    description="json-serializable HWSerial",
    long_description="json-serializable HWSerial",
    url="https://github.com/kyuzom/taskedin",
    license="MIT",
    packages=[
        "pyhwjser",
    ],
    package_data={
        "pyhwjser": ["**/*"],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
