from setuptools import setup, find_packages

setup(
    name='heartfailure',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==1.1.2',
        'pandas==1.2.4',
        'scikit-learn==0.24.1',
        # 'pylint',
    ],
)
