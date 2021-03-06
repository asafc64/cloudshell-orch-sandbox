from setuptools import setup, find_packages
import os

with open(os.path.join('version.txt')) as version_file:
    version_from_file = version_file.read().strip()

with open('requirements.txt') as f_required:
    required = f_required.read().splitlines()

setup(
        name="cloudshell-orch-core",
        author="Quali",
        author_email="support@qualisystems.com",
        packages=find_packages(),
        package_data={'': ['*.txt']},
        install_requires=required,
        version=version_from_file,
        include_package_data=True,
        keywords="sandbox cloud cloudshell",
        classifiers=[
            "Topic :: Software Development :: Libraries",
            "License :: OSI Approved :: Apache Software License",
        ]
)