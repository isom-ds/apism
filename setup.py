from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='uoa_isom_ds_sm_api_sdk',
    version='0.0.22',
    description='Simplified social media API calls',
    url='https://github.com/isom-ds/social-media-api-sdk',
    author='Brice Shun',
    author_email='brice.kok.shun@auckland.ac.nz',
    license='internal_use',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False
)