

# Errata and changes for Python Microservices Development, 2nd Edition

# Chapter 9 - Packaging and Running Python

## Page 226

The list of files to include in a project mentions `pyproject.toml`, but
describes `setup.py`. Given the text in the chapter, the list should include
`setup.py`, although more recent Python practices include using
`pyproject.toml` instead. Please consult the [pip
documentation](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)
for further information.

The list of files to include in a project should also include `MANIFEST.in`,
which while not required, can be a good idea, and is described in the chapter. 
