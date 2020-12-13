===============
mlops-generator
===============


.. image:: https://img.shields.io/pypi/v/mlops_generator.svg
        :target: https://pypi.python.org/pypi/mlops_generator

.. image:: https://img.shields.io/travis/averagua/mlops_generator.svg
        :target: https://travis-ci.com/averagua/mlops_generator

.. image:: https://readthedocs.org/projects/mlops-generator/badge/?version=latest
        :target: https://mlops-generator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/averagua/mlops_generator/shield.svg
     :target: https://pyup.io/repos/github/averagua/mlops_generator/
     :alt: Updates



CLI for MLOps generator


* Free software: MIT license
* Documentation: https://mlops-generator.readthedocs.io.

Install
--------
```python
pip install -r ./requirements.txt
```

```python
python3 setup.py install
```

Features
--------

* Initialize project ```mlops_generator init```
* Add configurations ```mlops_generator add```
        * `--setup` add setup.py entry point
        * `--tests` add pytests suite for unit tests
        * `--docker` add dockerfile and .dockerignore
        * `--deploy` add Google Cloud Build CI Pipeline
* Add components ```mlops_generator component```
        * Pandas extension
        * Sklearn base classes (TransformerMixin, RegressorMixin, ClassifierMixin, etc)
        * kubeflow-component or Kubeflow Container Op 
        * kubeflow-pipeline
        * Jupyter-notebook
        * Temporal and Visualization artifacts for kubeflow

* Help ```mlops_generator --help```

Credits
-------

This documentation was generated from Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template. Thanks cookiecutter!

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
