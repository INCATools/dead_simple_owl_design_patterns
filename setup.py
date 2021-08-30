import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dosdp",
    version="0.1.7.dev1",
    description="The aim of this project is to specify a simple OWL design pattern system that can easily be consumed, whatever your code base.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/INCATools/dead_simple_owl_design_patterns",
    author="INCATools",
    license="GPL-3.0 License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=["dosdp", "schema", "dosdp.document", "dosdp.document.pattern", "dosdp.document.schema"],
    include_package_data=True,
    install_requires=["PyYAML", "jsonschema", "requests", "jsonpath_rw", "ruamel.yaml", "jsonschema2md", "pandas"],
    entry_points={
        "console_scripts": [
            "dosdp=dosdp.__main__:main",
        ]
    },
)
