from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt', 'r') as f:
        ret = [line.strip() for line in f.readlines()]
        print("requirements:", ret)
    return ret


setup(
    name='ligent',
    version='0.0.0',
    description='',
    author='THUNLP',
    url='https://github.com/thunlp/LIGENT',
    author_email='chengzl22@mails.tsinghua.edu.cn',
    download_url='https://github.com/thunlp/LIGENT/archive/master.zip',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=['nlp', 'embodied', 'ai'],
    python_requires=">=3.6.0",
    install_requires=get_requirements(),
    packages=find_packages(),
    package_data={'': ['*.json']},
    entry_points={
        "console_scripts": [
            "ligent=ligent:main",
        ],
    }
)
