import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyFloatplane',
    version='1.1.3',
    author='Sammy8806',
    author_email='mail@sammy8806.de',
    description='Unofficial REST-Client bindings for Floatplane.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.dark-it.net/stappert/pyFloatpane',
    keywords='floatplane floatplanemedia rest-client linustechtips linusmedia videos',
    project_urls={
        'Floatplane': 'https://floatplane.com',
    },
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=(
        'Development Status :: 4 - Beta',

        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Video',
    ),
    install_requires=[
        'requests',
        'python-dateutil'
    ],
    python_requires='>=3.5',
    package_data={
        '': ['*.txt', '*.rst', '*.md'],
    },
)
