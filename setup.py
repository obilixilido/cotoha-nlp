from setuptools import setup, find_packages

setup(name='cotoha_nlp',
      version='0.0.1',
      description='Utitlty for Parsing API of COTOHA',
      author='obilixilido',
      author_email='obilixilido@gmail.com',
      url='https://github.com/obilixilido/cotoha-nlp',
      packages=find_packages(exclude=('tests', 'docs')),
      install_requires=[
        "requests",
        "oauthlib",
        "requests_oauthlib"
      ],
      setup_requires=["pytest-runner"],
      tests_require=["pytest", "pytest-cov"])
