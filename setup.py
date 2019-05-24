import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hodgelaplacians",
    version="0.1",
    keywords="Laplacian, TDA, Spectrum",
    author="Mikhail Tsitsvero",
    author_email="tsitsvero@gmail.com",
    description="Hodge Laplacians and their spectra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsitsvero/hodgelaplacians",
    packages=setuptools.find_packages(),
    classifiers=[
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Scientific/Engineering :: Physics",
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License"
      ],
    tests_require=[
          'unittest2',
    ],
    include_package_data=True,
    test_suite="test",
    zip_safe=False
)
