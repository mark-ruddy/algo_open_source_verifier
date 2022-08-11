from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

setup(
    name='algorand_verifier_lib',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.43',
    license='MIT',
    author='Mark Ruddy',
    author_email='1markruddy@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/mark-ruddy/algo_open_source_verifier',
    install_requires=[
        "attrs==21.4.0",
        "certifi==2022.6.15",
        "charset-normalizer==2.1.0",
        "idna==3.3",
        "iniconfig==1.1.1",
        "packaging==21.3",
        "pipreq==0.4",
        "pluggy==1.0.0",
        "py==1.11.0",
        "pyparsing==3.0.9",
        "pytest==7.1.2",
        "python-dotenv==0.20.0",
        "requests==2.28.1",
        "tomli==2.0.1",
        "urllib3==1.26.11",
    ],
)
