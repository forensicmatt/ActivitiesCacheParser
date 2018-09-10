from setuptools import setup

setup(
    name='winactivities',
    version="0.0.1",
    description='Parse Windows ActivitiesCache to JSONL.',
    author='Matthew Seyer',
    url='https://github.com/forensicmatt/ActivitiesCacheParser',
    license='Apache License (2.0)',
    packages=[
        'winactivities'
    ],
    python_requires='>=3',
    install_requires=[
        'ujson',
        'pytsk3'
    ],
    scripts=[
        'scripts/winactivities2json.py'
    ]
)
