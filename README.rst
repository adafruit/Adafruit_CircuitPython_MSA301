Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-msa301/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/msa301/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_MSA301.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_MSA301
    :alt: Build Status

CircuitPython library for the MSA301 Accelerometer


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-msa301/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-msa301

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-msa301

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-msa301

Usage Example
=============

.. code-block: python3
    import time
    import board
    import adafruit_msa301
    import busio

    i2c = busio.I2C(board.SCL, board.SDA)

    msa = adafruit_msa301.MSA301(i2c)
    while True:
        print("%f %f %f"%msa.acceleration)
        time.sleep(0.125)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_MSA301/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
