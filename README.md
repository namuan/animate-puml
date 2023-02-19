# PlantUML Animation

[![PyPI](https://img.shields.io/pypi/v/animate-puml?style=flat-square)](https://pypi.python.org/pypi/animate-puml/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/animate-puml?style=flat-square)](https://pypi.python.org/pypi/animate-puml/)
[![PyPI - License](https://img.shields.io/pypi/l/animate-puml?style=flat-square)](https://pypi.python.org/pypi/animate-puml/)

Simple animation for PlantUML diagrams.

![](assets/security-puml.gif)

---

**Documentation**: [https://namuan.github.io/animate-puml](https://namuan.github.io/animate-puml)

**Source Code**: [https://github.com/namuan/animate-puml](https://github.com/namuan/animate-puml)

**PyPI**: [https://pypi.org/project/animate-puml/](https://pypi.org/project/animate-puml/)

---

## Pre-requisites

- [PlantUML](https://plantuml.com/)
  ```shell
  brew install plantuml
  ```

## Installation

```sh
pip install animate-puml
```

## Usage

Given an example PlantUML document in `assets/security.puml`:

```shell
animate-puml -i assets/security.puml -o assets/security-puml.gif
```

By default, the script will delete any temporary files generated during the animation process.
To keep the files, use the `--debug` flag.

```shell
animate-puml -i assets/security.puml -o assets/security-puml.gif --debug
```

Each frame of the animation will wait for 1 second by default.
To change the wait time, use the `--frame-duration` flag to specify the time in milliseconds.

```shell
animate-puml -i assets/security.puml -o assets/security-puml.gif --frame-duration 4000
```

Use the `-h` flag to see all available options.

```shell
animate-puml -h
```

## Acknowledgements

- [PlantUML](https://plantuml.com/)

## Development

* Clone this repository
* Requirements:
  * Python 3.7+
  * [Poetry](https://python-poetry.org/)

* Create a virtual environment and install the dependencies
```sh
poetry install
```

* Activate the virtual environment
```sh
poetry shell
```

### Validating build
```sh
make build
```

### Release process
A release is automatically published when a new version is bumped using `make bump`.
See `.github/workflows/build.yml` for more details.
Once the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.

### Disclaimer

This project is not affiliated with PlantUML.
