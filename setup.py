from setuptools import setup, find_packages

setup(
    name="advanced_password_inspector",
    version="1.0.0",
    author="Tom Souillard",
    author_email="tom.souillard@gmail.com",
    description="A comprehensive tool for password strength evaluation, including API access and detailed reporting features.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tom-Souillard/advanced_password_inspector",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "zxcvbn>=4.4.28",
        "pytest>=8.1.1",
        "colorama>=0.4.6",
        "Pygments>=2.17.2",
        "rich>=13.7.1",
        "readme_renderer>=43.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.12',
    entry_points={
        'console_scripts': [
            'advanced_password_inspector=advanced_password_inspector.main:main',
        ],
    },
    keywords='password security analysis',
    license='Apache License 2.0',
    project_urls={
        'Documentation': 'https://github.com/Tom-Souillard/advanced_password_inspector',
        'Source': 'https://github.com/Tom-Souillard/advanced_password_inspector',
        'Tracker': 'https://github.com/Tom-Souillard/advanced_password_inspector/issues',
    },
    test_suite='tests'
)
