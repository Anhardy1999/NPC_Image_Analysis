import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-package-anhardy",
    version="0.0.1",
    author="Example Author",
    author_email="ahardy.contact@gmail.com",
    description=" A Python package to assist in performing image analysis on Neural Progenitor Cells (NPCS).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anhardy1999/NPC_Image_Analysis",
    project_urls={
        "Bug Tracker": "https://github.com/Anhardy1999/NPC_Image_Analysis/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)