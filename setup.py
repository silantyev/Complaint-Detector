from setuptools import setup

setup(
    name='complaint_detector',
    version='1.0',
    description='Complaint detection model based on DistilBERT',
    author='Boris Silantev',
    author_email='silantiev@inbox.ru',
    packages=['complaint_detector'],
    include_package_data=True,
    install_requires=['numpy', 'unidecode', 'tensorflow==2.5.1', 'transformers==4.12.3'],
)