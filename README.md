# switchmng

[![Build Status](https://travis-ci.org/AnsgarKlein/switchmng.svg?branch=develop)](https://travis-ci.org/AnsgarKlein/switchmng)
[![Coverage](https://codecov.io/gh/AnsgarKlein/switchmng/branch/develop/graph/badge.svg)](https://codecov.io/gh/AnsgarKlein/switchmng)
![License](https://img.shields.io/github/license/AnsgarKlein/switchmng?color=blue)

*switchmng* is a documentation service for network switches.  
It allows configurations of network switches like VLAN assignments on ports to
be documented in a structured way and exposed via REST. It is meant to be used
as a building block in configuration management for network switches. In the
future *switchmng* might be able to query switches in a vendor-specific way to
apply configuration from *switchmng* or to update information in *switchmng*.

*switchmng* is written in python and builds heavily on
[SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) and
[Flask](https://github.com/pallets/flask).

# Installing

Install all dependencies via pip:

```
$ pip install -r requirements.txt
```

# Using

After installing dependencies just start switchmng module:

```
$ python -m switchmng
```

See `--help` option for more information.

# License
*switchmng* is distributed under the
[MIT license](https://opensource.org/licenses/mit-license.php).
