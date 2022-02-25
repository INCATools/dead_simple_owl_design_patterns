import pathlib
from setuptools import setup

READTHEDOCS = "(http://incatools.github.io/dead_simple_owl_design_patterns/"
relative_link_mapping = {"(docs/dosdp_schema.md)": READTHEDOCS + "dosdp_schema/)",
                         "(docs/validator.md)": READTHEDOCS + "validator/)",
                         "(docs/document.md)": READTHEDOCS + "document/)"}


def update_relative_links(readme_content):
    """
    Relative links are broken in the pypi home page. So replace them with read the docs absolute links.
    """
    for key, value in relative_link_mapping.items():
        readme_content = readme_content.replace(key, value)
    return readme_content


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
README = update_relative_links(README)

# This call to setup() does all the work
setup(
    name="dosdp",
    version="0.1.10.dev1",
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
