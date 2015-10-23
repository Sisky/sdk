.. _installsdk:

================================
Installing the Mega SDK Python API
================================

--------------------------
1. Prepare System
--------------------------

.. code:: bash

    sudo apt-get install build-essential autoconf libtool git-core

-------------------------
2. Clone MEGA SDK
-------------------------

.. code:: bash
    
    git clone https://github.com/meganz/sdk

-------------------------
3. Install Dependencies
-------------------------

.. code:: bash

    sudo apt-get install libcrypto++-dev zlib1g-dev libsqlite3-dev libssl-dev libc-ares-dev libcurl4-openssl-dev libfreeimage-dev libreaadline6-dev swig2.0
   
----------------------
4. Configure SDK 
----------------------

.. code:: bash

    cd sdk/
   
.. code:: bash

    sh autogen.sh

.. code:: bash
    
    ./configure --disable-silent-rules --enable-python --disable-examples

-------------------------------
5. Compile & Install SDK
-------------------------------

.. code:: bash
    
    make
            
-------------------------------------------------
6. Build Python Distribution Package
-------------------------------------------------    
The Python package to be built will be a platform specific "Wheel" package, as it contains all native libraries (shared libraries, DLLs) required to use the Mega API from Python. Firstly, you need to install the wheel package for Python.

.. code:: bash

    pip install wheel 

Then you need to move to folder that contains the actual Python bindings itself and build the package.

.. code:: bash

    cd bindings/python
    
.. code:: bash

    python setup.py bdist_wheel
    
The package created will be located in folder dist/.

.. code:: bash

    cd dist/

.. code:: bash
    
    pip install megasdk-2.6.0-py2.py3-none-any.whl

It is possible to check if the package was installed properly using Python interactive shell.

.. code:: python

    import mega
    api = mega.MegaApiPython('Test', None, None, 'Test')
    print(dir(api))
   
-------------------------------------------------
7. Done
-------------------------------------------------

Congratulations you are now ready to use the MEGA SDK Python API bindings in your own applications!

.. NOTE::
    This guide was tested on Xubuntu 15.04 and is adapted from:      https://github.com/meganz/sdk/blob/master/README.md 