"""Setup script for advanced-agent-token-optimizer package."""
from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='advanced-agent-token-optimizer',
    version='1.0.0',
    author='labgadget015-dotcom',
    description='Advanced autonomous agent with token budget optimization and strategic execution capabilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer',
    packages=find_packages(exclude=['tests*']),
    py_modules=['agent_core', 'config', 'examples'],
    install_requires=requirements,
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='agent automation token-optimization ai autonomous',
    project_urls={
        'Bug Reports': 'https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer/issues',
        'Source': 'https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer',
    },
)
