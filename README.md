# nbib

A parser of the nbib citation format exported by PubMed & other NCBI tools. 

## About
`nbib` is opinionated in what data it parses and how it is structured, with the aim of supporting the most common use 
cases. Unlike other parsers, which produce "flat" data (i.e. string key-value pairs), `nbib`:

* Parses strings into their correct data type, as possible
* Creates hierarchical and list objects when appropriate

## Install

Install the latest production from [PyPi](https://pypi.org/project/nbib/):
```bash
pip install nbib
```

To install the latest dev version:

```bash
pip install git+https://github.com/holub008/nbib.git
```

## Using

### Example
```python
import nbib
refs = nbib.read("""PMID- 1337\nTI  - `nbib` Rocks!\n\n""")
```

### General

`nbib` does:

* Provide parsing of both nbib files (`read_file()`) and strings (`read()`)
* Guarantee that the output format will remain backwards compatible, within a major release
    * The type of an attribute will never change within a major release
    * An attribute will never change name within a major release
    * New attributes may be added with a minor release
* Guarantee that the order of output refs matches the incoming order. Moreover, this holds for all list attributes
(e.g. authors)

`nbib` does not:

* Allow users to customize parsing methods
    * `nbib` opines that performing the "obvious" parsing covers 99% of use cases, so don't push this work onto the 
    client 
* Play nicely with improperly formatted files - exceptions are aggressively thrown for unexpected inputs
    * Given PubMed is effectively the sole producer of these files, the risk is minimal
    * Please report any issues encountered! 
* Have great run time performance
    * As of writing, a 10,000 ref file (PubMed max export size) of 829K lines took 9.2 seconds on a standard laptop.
    For comparison, the ris parsing package `rispy`, which produces flat string data, took 2.2 seconds for 10K refs 
    (670K lines).
    * If your use case needs faster performance, please file an issue!
    
## Developing

Issues and pull requests are always welcome.

### Testing
To set up the project:

```bash
pipenv install --dev
```

To run tests:

```bash
pipenv run python -m pytest
```