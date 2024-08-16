from setuptools import setup

setup(
    name='pwd_mgr',
    version='1.1',
    description='Python Password Manager',
    author='mukund.r',
    packages=['pm', 'pm.utils'],
    install_requires=[
        'typer',
        'rich',
        'psycopg2-binary',
        'uuid'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: None",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7, <4",
    entry_points={
        "console_scripts": [
            "pm = pm.main:app"
        ]
    }
)
