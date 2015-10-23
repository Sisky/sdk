.. _gettingstarted:

===============
Getting Started
===============

------------
Introduction
------------

.. nature of binding: uses SWIG library to build, then uses API classes to improve usability of raw SWIG bindings, working async in C++

.. Use https://mega.nz/#doc as reference material

.. reST standards & markup http://sphinx-doc.org/rest.html

MEGA, `The Privacy Company`, is a Secure Cloud Storage provider that protects your data using automatically managed end-to-end encryption.

All files stored on MEGA are encrypted. All data transfers from and to MEGA are encrypted. While most cloud storage providers claim the same, MEGA is different. Unlike the industry norm where the cloud storage provider holds the decryption key, with MEGA, you control the encryption. You hold the keys and you decide who you grant or deny access to your files. We call it User Controlled Encryption (UCE).

MEGA Ltd provides a Software Development Kit (SDK) for its cloud storage services. The MEGA SDK is developed and maintained in C++. In order to facilitate development of third-party applications using MEGA services, MEGA provides bindings to the core C++ functionality for several high-level languages, including Python.

This guide describes how to install the MEGA SDK Python bindings and explains the basic principles of use.

^^^^
SWIG
^^^^

The additional language bindings are automatically generated from C++ by the Simplified Wrapper and Interface Generator (SWIG) open source tool.

    `"SWIG is an interface compiler that connects programs written in C and C++ with scripting languages such as Perl, Python, Ruby, and Tcl. It works by taking the declarations found in C/C++ header files and using them to generate the wrapper code that scripting languages need to access the underlying C/C++ code."` 

For more information, please visit: http://www.swig.org/

Updates to the SDK are carried out by modifying the C++ code then re-generating the bindings using SWIG. This has the benefit of adding functionality to all language bindings from a single central source, without the need to add the change to each language's bindings manually.

^^^^^^^^^^^^
API Bindings
^^^^^^^^^^^^

In order to make the automatically generated SWIG bindings more usable for developers, language native Application Programming Interfaces (APIs) are developed. These APIs are written in the native language, not SWIG generated. They aim to follow native language conventions and attempt to handle C++ differences, such as garbage handling, in the background. This frees up the developer to concentrate on developing solutions, not learning how to interface with C++ in their preferred language.

^^^^^^^^^^^^
Asynchronous
^^^^^^^^^^^^

In order to speed up the process of interacting with MEGA services, common functionality is carried out on non-blocking, concurrent threads at the core C++ code level.


----------------------------------------
Installation
----------------------------------------

Before you are able to start implementing the various functionality of the MEGA bindings you will of course need to compile and install them.

:ref:`installsdk`

The Python bindings can be found in ``sdk/bindings/python/_megawrap.py``.

-------------------
Concepts
-------------------

There are some features of the SDK which **must** be initiated in order to work with the functionality of the SDK.

^^^^^^^
AppKey
^^^^^^^

An appKey must be specified to start a session and use the MEGA SDK in your own code. Generate an appKey for free at https://mega.co.nz/#sdk

.. code:: python
    
    '''    
    An appKey is required to access MEGA services using the MEGA SDK.
    You can generate an appKey for your app for free @ https://mega.co.nz/#sdk
    '''
    APP_KEY = 'ox8xnQZL'


^^^^^^^^
API object
^^^^^^^^

To login and access MEGA services it is necessary to instantatiate an MegaApiPython object first. After the proper API object is created, it can then be used to login and access other MEGA services. In order to create MegaApiPython object it is necessary to specify an APP_KEY, processor, base and user_agent parameters.  

.. code:: python
 
    '''
    The MegaApiPython object which provides access to the various 
    MEGA storage functionality.
    '''
    api = MegaApiPython(APP_KEY, None, None, 'your_own_text')

    
^^^^^^^^^^^^^^^^^
Nodes
^^^^^^^^^^^^^^^^^

The MEGA SDK represents files and folders as trees of Node objects. Nodes point to parent nodes, forming trees. Trees have exactly one root node. For this reason, to interact with files and folders on the MEGA Cloud Storage service, ``MegaNode`` objects are referenced. 

.. code:: python
    
    # Specify file node
    node = api.get_node_by_path_base_folder("string_path_to_name_of_file", parent_node);
    

^^^^^^^^^
Listener
^^^^^^^^^

You can implement your own listener class ``AppListener``(Example name). Here you are able to implement the actual functionality and operations that will be performed when certain requests are sent to the MEGA server from your application. It is important to note that user created listener class has to extend the actual Listener class depending on the needs of application. Available Mega Listeners are:
 * MegaListener (This particular type can be used for all operations)
 * MegaRequestListener
 * MegaTransferListener
 * MegaGlobalListener

.. code:: python
    
    # Create a new listener class
    class AppListener(MegaListener): 
    ...
    

The listener should then be added to the MegaApiPython object.

.. code:: python

    # Add the MEGACRUD listener object to listen for events when interacting
    # with MEGA Services
    api.add_mega_listener(listener) # For MegaListener type
    # or
    api.add_request_listener(listener) # For MegaRequestListener type
    # or
    api.add_transfer_listener(listener) # For MegaTransferListener type
    # or
    api.add_global_listener(listener) # For MegaGlobalListenerType
    
In this way you can, for example, check that a request was carried out successfully:

.. code:: python

    def onRequestFinish(api, request, error):

        # identify the MegaRequest type which has finished and triggered this event
        request_type = request.getType()
        if request_type == MegaRequest.TYPE_ACCOUNT_DETAILS:
           print('Account details received')
 

Request Types
"""""""""""""
Some useful request types include:
 * MegaRequest.TYPE_LOGIN
 * MegaRequest.TYPE_FETCH_NODES
 * MegaRequest.TYPE_ACCOUNT_DETAILS
 * MegaRequest.TYPE_UPLOAD
 * MegaRequest.TYPE_REMOVE
 * MegaRequest.TYPE_LOGOUT

---------------------------
Basic Functionality (CRUD)
---------------------------

The following steps will help you use the basic MEGA SDK functionality, including:
 * Login
 * **Create**
 * **Read**
 * **Update**
 * **Delete**
 * Log out


^^^^^^
Log-in
^^^^^^

The first step to access MEGA services is for the user to have have a valid account and log-in. To do this you can use the MEGA API log-in functionality. One of the ``MegaApiPython.login_email()`` options should be used to log into a MEGA account to successfully start a session. This will require retrieving the user's email address (MEGA user name) and password and passing this to the function.

.. code:: python

    # Log in.
    api.login_email(user_email, password);

If the log-in request succeeds, call ``api.fetch_nodes()`` to get the account's file hierarchy from MEGA.

.. code:: python

    # The user has just logged in, so fetch the nodes of of the users account
    # object so that the MEGA API functionality can be used.
    api.fetch_nodes();

Once logged in with the file hierarchy retrieved, you will be able to carry out additional functionality. All other requests, including file management and transfers, can be used. Please see the inline Pydoc in ``sdk/bindings/python/_megawrap.py`` for other ways of logging into the account. Let's start with "Create".

^^^^^^
Create
^^^^^^

Below is the function for the uploading a file, or creating a ``MegaNode``, on the MEGA cloud storage service.

.. code:: python

    # Instantiate a MegaNode as the logged in user's root directory.
    parent_directory = api.get_root_node();

.. code:: python

    # Create (a.k.a Upload Node).
    api.start_upload("localPath/README.md", parent_directory);
    # Or create with dedicated listener
    api.start_upload_with_listener("localPath/README.md", parent_directory, listener)

This example shows the upload of a file called ``README.md`` to a parent directory on the MEGA Cloud Storage service. It simply calls the ``start_upload()`` method and passes the local path of the file as a String. The destination parent directory in the user's MEGA cloud storage file hierarchy is specified as a ``MegaNode`` object.
Using function as shown an second example with dedicated listener will not use the primary listener created in the ``add_mega_listener()`` step, but will create its own listener that will be used to perform the action. The listener in parameters is the one created by used as shown in ``Listener`` section of the guide.
Please see the inline Pydoc in ``sdk/bindings/python/_megawrap.py`` for other ways of calling the ``start_upload()`` function with different parameters. Next we look at "Read".

^^^^
Read
^^^^

Being able to retrieve uploaded files is an important feature which can be achieved using the methods below:

.. code:: python

    # Instantiate a MegaNode object as the target file to download from the logged
    # in user's root directory.
    file_to_download = api.get_node_by_path_base_folder("README.md", parent_directory)

.. code:: python

    # Read (a.k.a Download Node).
    api.start_download(file_to_download, "README_returned.rst")
    # Or read with dedicated listener
    api.start_download_with_listener(file_to_download, "README_returned.rst", listener)        

This example shows reading a file called ``README.md`` from a directory, specified as ``parentDirectory``, on the MEGA Cloud Storage service.

The desired file to be downloaded is represented by an instantiated node object which is passed to the ``start_download()`` method. The local path of where to store the file is specified as a String. If this path is a local folder, it must end with a '\\' or '/' character. In this case, the file name in MEGA will be used to store a file inside that folder. If the path does not finish with one of these characters, the file will be downloaded with the specified name to the specified path. This is the case in our example where the returned file is downloaded to the application's root folder as ``README_returned.rst``.
Using function as shown an second example with dedicated listener will not use the primary listener created in the ``add_mega_listener()`` step, but will create its own listener that will be used to perform the action. The listener in parameters is the one created by used as shown in ``Listener`` section of the guide.

^^^^^^
Update
^^^^^^
A special case presents itself when replacing a file on the MEGA Cloud Storage with a file of the same name from your local directory. Below is an example of the readme.md file being uploaded for second time.

.. NOTE::
    Uploading a node with the same name does not overwrite the existing node. Instead, a second file with the same name is created.

.. code:: python

    # Instantiate a MegaNode as the target file to replace on the logged in
    # user's root directory.
    old_node = api.get_node_by_path_base_folder("README.md", parent_directory)
    
.. code:: python
    
    # Update
    api.start_upload("README.md", parent_directory)
    
If there is an old node with the same name you may want to delete that node before updating with the new node. This is the topic of the next section.

^^^^^^
Delete
^^^^^^

To delete a file from the MEGA Cloud Storage service simply call the ``remove_node()`` method, specifying the node you wish to remove.

.. code:: python

    # Check if the file is already present on MEGA.
    if old_node is not None:
        # Remove the old node with the same name.
        api.remove_node(old_node)
    

To tidy up, any unwanted files created by the application can be removed using the the ``remove_node()`` method as above. All that remains is to close the session.

^^^^^^^
Log-out
^^^^^^^

.. @TODO How to tidy up (if necessary) when ending the application's MEGA session.

Call ``logout_from_account()`` to close the MEGA session.

.. code:: python
    
    api.logout_from_account()

Ensure the ``logout_from_account()`` request has completed to guarantee that the session has been invalidated. This can be confirmed by waiting for a ``MegaRequest.TYPE_LOGOUT`` to trigger the ``onRequestFinish()`` listener method as demonstrated in Listener_.

After using ``api.logout_from_account()`` you can reuse the same ``MegaApiPython`` object to log in to another MEGA account.

``local_logout()`` can be used to log out without invalidating the current session. In this way the session can be resumed using log-in_.


---------------------------
Fin
---------------------------

And that's it. You are now ready to develop in Python for the MEGA Cloud Storage service.

For more specific information you can check out the inline Pydoc in the Python binding classes, particularly ``sdk/bindings/python/_megawrap.py``. For a detailed, C++ specific explanation, please visit: https://mega.nz/#doc


