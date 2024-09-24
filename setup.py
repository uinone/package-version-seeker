from setuptools import setup, find_packages

setup(
    name='pakage-version-seeker',
    version='1.0.0',
    description='Find unspecified pakages verison!!',
    author='uinone',
    author_email='tizm423@gmail.com',
    url='https://github.com/uinone/pakage-version-seeker',
    packages=find_packages(exclude=[]),
    include_package_data=True,
    keywords=[],
    python_requires='>=3.8',
    package_data={},
    entry_points={'console_scripts': ["pvs=src:main"]},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    install_requires=['requests==2.32.3', 'beautifulsoup4==4.12.3',],
    license='MIT',
)