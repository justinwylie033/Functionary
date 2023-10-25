from setuptools import setup, find_packages

setup(
    name='Functionary',
    version='0.1.0',
    description='A comprehensive tool for code generation, testing, and storage.',
    long_description='Functionary is a versatile tool designed to streamline the development process, offering features for automatic code generation, rigorous testing, and secure storage of code artifacts. It integrates seamlessly with various external services and provides a user-friendly interface for efficient project management.',
    url='https://github.com/justinwylie033/functionary',
    author='Justin Wylie',
    author_email='justin.wylie@example.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='code generation, testing, storage, development tools',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['docker', 'openai', 'pinecone-client', 'tenacity', 'python-decouple', 'flask', 'flask-cors'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
        'functionary': ['package_data.dat'],  # Adjust as per your package's structure
    },
    entry_points={
        'console_scripts': [
            'functionary=functionary:main',  # Adjust as per your package's structure
        ],
    },
)
