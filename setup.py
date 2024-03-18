import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="fancyInput",
  version="0.0.14",
  author="MintCoffeeCat",
  author_email="zzwyxl@163.com",
  description="A terminal-based python input tool for asking users with several options and except their input.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/MintCoffeeCat/FancyInput",
  packages=setuptools.find_packages(),
  install_requires= [
      'rich', 
      'wcwidth'
    ],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)