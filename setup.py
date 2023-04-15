import pathlib

import pkg_resources
from setuptools import find_packages, setup


def requirements(filepath: str):
    with pathlib.Path(filepath).open() as requirements_txt:
        return [
            str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)
        ]


setup(
    name='search_system',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Project for MSU course',
    url='https://github.com/DenisRogozhin/Slack-open-data-science-search-system/',
    python_requires='>=3.8',
    packages=find_packages(include=('development',)),
    include_package_data=True,
    install_requires=requirements('requirements.txt'),
    extras_require={'dev': requirements('requirements.dev.txt')},
)
