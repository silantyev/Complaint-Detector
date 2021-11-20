from setuptools import setup

setup(
   name='complaint_detector',
   version='1.0',
   description='Complaint detection model based on DistilBERT',
   author='Boris Silantev',
   author_email='silantiev@inbox.ru',
   packages=['complaint_detector'],
   install_requires=['numpy', 'unidecode', 'tensorflow', 'transformers'],
)