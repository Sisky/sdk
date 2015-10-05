from mega import *
import threading



class MegaApiPython(MegaApi):

    '''Python Appilcation Programming Interface (API) to access MEGA SDK services on a MEGA account or shared
    public folder.
    An app_key must be specified to use the MEGA SDK. Generate an app_key for free here: https://mega.co.nz/#sdk
    Save on data usage and start up by enabling local node caching. This can be enabled by passing a local path in the
    in the initializer. Local node caching prevents the need to download the entire file system each time the MegaApiPython
    object is logged in.
    To take advantage of local node caching, the application needs to save the session key after login MegaApiPython.dump_session() and
    use it to login during the next session. A persistent local node cache will only be loaded if logging in with a session key.
    Local node caching is also recommended in order to enchance security as it prevents the account password from being stored by
    the application.
    To access MEGA services using the MEGA SDK, an object of this class (MegaApiPython) needs to be created and one
    of the MegaApiPython.login() options used to log into a MEGA account or a public folder. If the login request succeeds,
    call MegaApiPython.fetch_nodes() to get the account's file system from MEGA. Once the file system is retrieved, all other requests
    including file management and transfers can be used.
    After using MegaApiPython.logout() you can reuse the same MegaApi object to log in to another MEGA
    account or a public folder.
    '''



    def __init__(self, app_key, processor, base_path, user_agent):
        super(MegaApiPython, self).__init__(app_key, processor, base_path, user_agent)
        self.active_mega_listeners = []
        self.active_global_mega_listeners = []
        self.active_request_listeners = []
        self.active_transfer_listeners = []
        self.lock = threading.Lock()

    # API METHODS

    def run_callback(self, listener, function):
        # TODO, will use threading for callbacks
        t = threading.Thread(target = listener.function(*args))
        t.setDaemon(True)
        t.start()


    # Listener management

    def add_mega_listener(self, listener):
        '''Register a listener to receive all events (requests, transfers, global, synchronization).
        You can use MegaApiPython.remove_listener() to stop receiving events.
        :param listener Listener that will receive all events (requests, transfers, global, synchronization).
        '''
        self.addListener(self.create_delegate_mega_listener(listener))

    def add_global_listener(self, listener):
        '''Register a listener to receive global events.
        You can use MegaApiPython.remove_global_listener() to stop receiving events.
        :param listener Listener that will receive global events.
        '''
        self.addGlobalListener(self.create_delegate_mega_global_listener(listener))

    def add_request_listener(self, listener):
        '''Register a listener to receive all events about requests.
        You can use MegaApiPython.remove_request_listener() to stop receiving events.
        :param listener Listener that will receive all events about requests.
        '''
        self.addRequestListener(self.create_delegate_request_listener(listener, False))

    def add_transfer_listener(self, listener):
        '''Register a listener to receive all events about transfers.
        You can use MegaApiPython.remove_transfer_listener() to stop receiving events.
        :param listener Listener that will receive all events about transfers.
        '''
        self.addTransferListener(self.create_delegate_transfer_listener(listener, False))

    def remove_listener(self, listener):
        '''Unregister a listener.
        Stop receiving events from the specified listener.
        :param listener Object that is unregistered
        '''
        self.lock.acquire()
        try:
            for item in self.active_mega_listeners:
                if item.get_user_listener() == listener.get_user_listener():
                    self.active_mega_listeners.remove(item)
        finally:
            self.lock.release()

    def remove_request_listener(self, listener):
        '''Unregister a listener.
        Stop receiving events from the specified listener.
        :param listener Object that is unregistered
        '''
        self.lock.acquire()
        try:
            for item in self.active_request_listeners:
                if item.get_user_listener() == listener.get_user_listener():
                    self.active_request_listeners.remove(item)
        finally:
            self.lock.release()

    def remove_transfer_listener(self, listener):
        '''Unregister a listener.
        Stop receiving events from the specified listener.
        :param listener Object that is unregistered
        '''
        self.lock.acquire()
        try:
            for item in self.active_transfer_listeners:
                if item.get_user_listener() == listener.get_user_listener():
                    self.active_transfer_listeners.remove(item)
        finally:
            self.lock.release()

    def remove_global_listener(self, listener):
        '''Unregister a listener.
        Stop receiving events from the specified listener.
        :param listener Object that is unregistered
        '''
        self.lock.acquire()
        try:
            for item in self.active_global_mega_listeners:
                if item.get_user_listener() == listener.get_user_listener():
                    self.active_global_mega_listeners.remove(item)
        finally:
            self.lock.release()

    # UTILS

    def get_current_request(self):
    	'''need clarification'''
        return self.getCurrentRequest()

    def get_current_transfer(self):
    	'''need clarification'''
        return self.getCurrentTransfer()

    def get_current_error(self):
    	'''need clarification'''
        return self.getCurrentError()

    def get_current_nodes(self):
    	'''need clarification'''
        return self.getCurrentNodes()

    def get_current_users(self):
    	'''need clarification'''
        return self.getCurrentUsers()

    def get_base64_pw_key(self, password):
    	'''Generates a private key based on the access password. This is a time consuming operation (specially for low-end mobile devices).  Since the resulting key is required to log in, this function   allows to do this step in a separate function. You should run this function in a background thread, to prevent UI hangs. The resulting key can be used in MegaApi.fastLogin.
        You take the ownership of the returned value.
        :param password - Access password
        :Returns - Base64-encoded private key
        :Deprecated
        '''
        return self.getBase64PwKey(password)

    def get_string_hash(self,base_64_pwkey, email):
    	'''Generates a hash based in the provided private key and email.
This is a time consuming operation (specially for low-end mobile devices). Since the resulting key is required to log in, this function allows to do this step in a separate function. You should run this function in a background thread, to prevent UI hangs. The resulting key can be used in MegaApi.fastLogin
        You take the ownership of the returned value.
        :param base_64_pwkey- Private key returned by MegaApi.get_base64_pw_key()
        :param email - Email to create the hash
        :Returns - Base64-encoded hash
        :Deprecated
        '''
        return self.getStringHash(base_64_pwkey, email)

    def retry_pending_connections(self):
    	'''Retry all pending requests.
		When requests fails they wait some time before being retried. That delay grows exponentially if the request fails again.
        For this reason, and since this request is very lightweight, it's recommended to call it with the default parameters on every
        user interaction with the application. This will prevent very big delays completing requests.
       	'''
        self.retryPendingConnections()

    def login(self, email, password):
    	'''Log in to a MEGA account.
        :param email -Email of the user
        :param password - Password
        '''
        self.login(email, password)

    def login_with_listener(self, email, password, listener):
    	'''Log in to a MEGA account.
		The associated request type with this request is MegaRequest.TYPE_LOGIN. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest.getEmail - Returns the first parameter
    		MegaRequest.getPassword - Returns the second parameter
		If the email/password aren't valid the error code provided in onRequestFinish is MegaError.API_ENOENT.
        :param email -Email of the user
        :param password - Password
        :param listener - MegaRequestListener to track this request
        '''
        self.login(email, password, self.create_delegate_request_listener(listener))

    def login_to_folder(self, mega_folder_link):
    	'''Log in to a public folder using a folder link.
		After a successful login, you should call MegaApi.fetch_nodes() to get filesystem and start working with the folder.
		:param megaFolderLink - Public link to a folder in MEGA
        '''
        self.loginToFolder(mega_folder_link)

    def login_to_folder_with_listener(self, mega_folder_link, listener):
    	'''Log in to a public folder using a folder link.
		After a successful login, you should call MegaApi.fetch_nodes() to get filesystem and start working with the folder.
		The associated request type with this request is MegaRequest.TYPE_LOGIN. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest.getEmail - Retuns the string "FOLDER"
    		MegaRequest.getLink - Returns the public link to the folder
		:param megaFolderLink - Public link to a folder in MEGA
        :param listener - MegaRequestListener to track this request
        '''
        self.loginToFolder(mega_folder_link, self.create_delegate_request_listener(listener))

    def fast_login_with_listener(self, email, string_hash,base_64_pwkey, listener):
    	'''Login to a MEGA account with precomputed keys.
        The associated request type with this request is MegaRequest.TYPE_LOGIN. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest.get_my_email() - Returns the email for the account
            MegaRequest.get_private_key() - Returns the private key calculated with MegaApi.get_base64_pw_key()
    		MegaRequest.get_string_hash() - Returns the hash of the user
    	:param email - Email for the account
        :param string_hash -hash of the email returned by MegaApi.get_string_hash()
    	:param base_64_pwkey	- Private key calculated with MegaApi.get_base64_pw_key()
    	:param listener - MegaRequestListener to track this request
        '''
        self.fastLogin(email, string_hash, base_64_pwkey, self.create_delegate_request_listener(listener))

    def fast_login(self, email, string_hash, base_64_pwkey):
    	'''Login to a MEGA account with precomputed keys.
    	:param email - Email for the account
        :param string_hash -hash of the email returned by MegaApi.get_string_hash()
    	:param base_64_pwkey	- Private key calculated with MegaApi.get_base64_pw_key()
        '''
        self.fastLogin(email, string_hash, base_64_pwkey)

    def fast_login_with_session(self, session):
    	'''Login to a MEGA account with a session key.
    	:param session - Session key previously dumped with api.dump_session()
        '''
        self.fastLogin(session)

    def fast_login_with_session_listener(session, listener):
    	'''Login to a MEGA account with a session key.
    	:param session - Session key previously dumped with api.dump_session()
        param listener - MegaRequestListener to track this request
        '''
        self.fastLogin(session, self.create_delegate_request_listener(listener))

    def kill_session_listener(self, session_handle, listener):
    	'''Close a MEGA session. All clients using this session will be automatically logged out.
        You can get session information using MegaApi.get_extended_account_details().
        Then use MegaAccountDetails.getNumSessions() and MegaAccountDetails.getSession()
        to get session info.
        MegaAccountSession.getHandle provides the handle that this function needs.
        If you use mega.INVALID_HANDLE, all sessions except the current one will be closed.
        :param session_handle of the session. Use mega.INVALID_HANDLE to cancel all sessions except the current one
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.killSession(session_handle, self.create_delegate_request_listener(listener))

    def kill_session(self, session_handle):
    	'''Close a MEGA session. All clients using this session will be automatically logged out.
        You can get session information using MegaApi.get_extended_account_details().
        Then use MegaAccountDetails.getNumSessions() and MegaAccountDetails.getSession()
        to get session info.
        MegaAccountSession.getHandle provides the handle that this function needs.
        If you use mega.INVALID_HANDLE, all sessions except the current one will be closed.
        :param session_handle of the session. Use mega.INVALID_HANDLE to cancel all sessions except the current one
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.killSession(session_handle)

    def get_user_data_listener(self, listener):
    	'''Get data about the logged account.
        The associated request type with this request is MegaRequest.TYPE_GET_USER_DATA.
        Valid data in the MegaRequest object received in onRequestFinish() when the error code is MegaError.API_OK:
            MegaRequest.getName() - Returns the name of the logged user
            MegaRequest.getPassword() - Returns the the public RSA key of the account, Base64-encoded
            MegaRequest.getPrivateKey() - Returns the private RSA key of the account, Base64-encoded
        param:listener MegaRequestListener to track this request
        '''
        self.getUserData(self.create_delegate_request_listener(listener))

    def get_user_data(self):
        '''Get data about the logged account.
        '''
        self.getUserData()

    def get_user_data_with_mega_user_listener(self, user, listener):
        '''Get data about a contact.
        The associated request type with this request is MegaRequest.TYPE_GET_USER_DATA.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail - Returns the email of the contact
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getText() - Returns the XMPP ID of the contact
            MegaRequest.getPassword() - Returns the public RSA key of the contact, Base64-encoded
        :param user  Contact to get the data
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.getUserData(user, self.create_delegate_request_listener(listener))

    def get_user_data_with_mega_user(self, user):
        '''Get data about a contact.
        :param user MegaUser contact to get the data
        '''
        self.getUserData(user)

    def get_user_data_with_user_listener(self, user, listener):
        '''
        Get data about a contact.
        The associated request type with this request is MegaRequest.TYPE_GET_USER_DATA.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail() - Returns the email or the Base64 handle of the contact
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getText() - Returns the XMPP ID of the contact
            MegaRequest.getPassword() - Returns the public RSA key of the contact, Base64-encoded
        :param user Email or Base64 handle of the contact
        :param listener MegaRequestListener to track this request
        '''
        self.getUserData(user, self.create_delegate_request_listener(listener))

    def get_user_data_with_user(self, user):
        '''Get data about a contact.
        :param user Email or Base64 handle of the contact
        '''
        self.getUserData(user)

    def dump_session(self):
    	'''Returns the current session key.
        You have to be logged in to get a valid session key. Otherwise, this function returns NULL.
        You take the ownership of the returned value.
        :Returns current session key
        '''
        return self.dumpSession()

    def dump_XMPP_session(self):
    	'''Returns the current XMPP session key.
        You have to be logged in to get a valid session key. Otherwise, this function returns NULL.
        You take the ownership of the returned value.
        :Returns current XMPP session key
        '''
        return self.dumpXMPPSession()

    def create_account_with_listener(self, email, password, name, listener):
    	'''Initialize the creation of a new MEGA account.
        The associated request type with this request is MegaRequest.TYPE_CREATE_ACCOUNT. Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail - Returns the email for the account
            MegaRequest.getPassword - Returns the password for the account
            MegaRequest.getName - Returns the name of the user
        If this request succeed, a confirmation email will be sent to the users.
        If an account with the same email already exists, you will get the error code MegaError.API_EEXIST in onRequestFinish
        :param email - Email for the account
        :param password - Password for the account
        :param name - Name of the user
        :param listener - MegaRequestListener to track this request
        '''
        self.createAccount(email, password, name, self.create_delegate_request_listener(listener))

    def create_account(self, email, password, name):
        '''Initialize a creation of the new MEGA account.
        :param email - Email for the account
        :param password - Password for the account
        :param name - Name of the user
        '''
        self.createAccount(email, password, name)

    def fast_create_account_listener(self, email, base_64_pwkey, name, listener):
    	'''Initialize the creation of a new MEGA account with precomputed keys.
        The associated request type with this request is MegaRequest.TYPE_CREATE_ACCOUNT. Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail - Returns the email for the account
            MegaRequest.getPrivateKey - Returns the private key calculated with MegaApi.getBase64PwKey
            MegaRequest.getName - Returns the name of the user
        If this request succeed, a confirmation email will be sent to the users. If an account with the same email already exists, you will get the error code MegaError.API_EEXIST in onRequestFinish
        :param email - Email for the account
        :param base_64_pwkey - Private key calculated with MegaApi.get_base64_pw_key()
        :param name - Name of the user
        :param listener - MegaRequestListener to track this request
        '''
        self.fastCreateAccount(email, base_64_pwkey, name, self.create_delegate_request_listener(listener))

    def fast_create_account(self, email, base_64_pwkey, name):
        '''Initialize the creation of a new MEGA account with precomputed keys.
        :param email - Email for the account
        :param base_64_pwkey - Private key calculated with MegaApi.get_base64_pw_key()
        :param name - Name of the user
        '''
        self.fastCreateAccount(email, base_64_pwkey, name)

    def query_signup_link_listener(self, link, listener):
    	'''Get information about a confirmation link.
        The associated request type with this request is MegaRequest.TYPE_QUERY_SIGNUP_LINK. Valid data in the MegaRequest object received on all callbacks:
            MegaRequest.getLink - Returns the confirmation link
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getEmail - Return the email associated with the confirmation link
            MegaRequest.getName - Returns the name associated with the confirmation link
        :param link - Confirmation link
        :param listener - MegaRequestListener to track this request
        '''
        self.querySignupLink(link, self.create_delegate_request_listener(listener))

    def query_signup_link(self, link):
        '''Get information about a confirmation link.
        :param link Confirmation link
        '''
        self.querySignupLink(link)

    def confirm_account_listener(self, link, password, listener):
    	'''Confirm a MEGA account using a confirmation link and the user password.
        The associated request type with this request is MegaRequest.TYPE_CONFIRM_ACCOUNT Valid data in the MegaRequest object received on callbacks:
        MegaRequest.getLink - Returns the confirmation link
        MegaRequest.getPassword - Returns the password
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getEmail - Email of the account
            MegaRequest.getName - Name of the user
        :param link - Confirmation link
        :param password - Password of the account
        :param listener - MegaRequestListener to track this request
        '''
        self.confirmAccount(link, password, self.create_delegate_request_listener(listener))

    def confirm_account(self, link, password):
        '''Confirm a MEGA account using a confirmation link and the user password.
        :param link - Confirmation link
        :param password - Password of the account
        '''
        self.confirmAccount(link, password)

    def fast_confirm_account_listener(self, link, base_64_pwkey, listener):
    	'''Confirm a MEGA account using a confirmation link and a precomputed key.
        The associated request type with this request is MegaRequest.TYPE_CONFIRM_ACCOUNT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getLink - Returns the confirmation link
            MegaRequest.getPrivateKey - Returns the base64pwkey parameter
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getEmail - Email of the account
            MegaRequest.getName - Name of the user
        :param link - Confirmation link
        :param base_64_pwkey - Private key precomputed with MegaApi.get_base64_pw_key()
        :param listener - MegaRequestListener to track this request
        '''
        self.fastConfirmAccount(link, base_64_pwkey, self.create_delegate_request_listener(listener))

    def fast_confirm_account(self, link, base_64_pwkey):
        '''Confirm a MEGA account using a confirmation key and a precomputed key.
        :param link - Confirmation link
        :param base_64_pwkey - Private key precomputed with MegaApi.get_base64_pw_key()
        '''
        self.fastConfirmAccount(link, base_64_pwkey)

    def set_proxy_settings(self, proxy_settings):
    	'''Set proxy settings.
        The SDK will start using the provided proxy settings as soon as this function returns.
        :param proxy_settings - Proxy settings
        '''
        self.setProxySettings(proxy_settings)

    def get_auto_proxy_settings(self):
    	'''Try to detect the system's proxy settings.
        Automatic proxy detection is currently supported on Windows only. On other platforms, this fuction will return a MegaProxy object of type MegaProxy.PROXY_NONE
        You take the ownership of the returned value.
        :param Returns MegaProxy object with the detected proxy settings.
        '''
        return self.getAutoProxySettings()

    def is_logged_in(self):
    	'''Check if the MegaApi object is logged in.
        :Returns 0 if not logged in, else a number >= 0
        '''
        return self.isLoggedIn()

    def get_my_email(self):
    	'''Returns the email of the currently open account.
        If the MegaApi object isn't logged in or the email isn't available, this function returns None
        You take the ownership of the returned value
        :Returns Email of the account
        '''
        return self.getMyEmail()

    def get_my_user_handle(self):
    	'''need clarification'''
        return self.getMyUserHandle()

    def set_logger_object(self, mega_logger):
        '''Set a MegaLogger implementation to receive SDK logs.
        Logs received by this objects depends on the active log level.
        By default it is MegaApi.LOG_LEVEL_INFO.You can changed it using
        MegaApi.setLogLevel()
        :param mega_logger MegaLogger implementation
        '''
        new_logger = DelegateMegaLoggerListener(mega_logger)
        self.setLoggerObject(new_logger)
        logger = new_logger

    def set_log_level(self, log_level):
        '''Set the active log level.
        This function sets the log level of the logging system. If you set a log listener using
        MegaApiJava.set_logger_object(), you will receive logs with the same or a lower level than
        the one passed to this function.
        :param logLevel Active log level. These are the valid values for this parameter:
             MegaApiJava.LOG_LEVEL_FATAL = 0
             MegaApiJava.LOG_LEVEL_ERROR = 1
             MegaApiJava.LOG_LEVEL_WARNING = 2
             MegaApiJava.LOG_LEVEL_INFO = 3
             MegaApiJava.LOG_LEVEL_DEBUG = 4
             MegaApiJava.LOG_LEVEL_MAX = 5
        '''
        self.setLogLevel(log_level)

    def log():
        pass

    def log():
        pass

    def log():
        pass

    def create_folder_listener(self, name, parent, listener):
    	'''Create a folder in the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_CREATE_FOLDER Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getParentHandle - Returns the handle of the parent folder
            MegaRequest.getName - Returns the name of the new folder
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getNodeHandle - Handle of the new folder
        :param name - Name of the new folder
        :param parent - Parent folder
        :param listener - MegaRequestListener to track this request
        '''
        self.createFolder(name, parent, self.create_delegate_request_listener(listener))

    def create_folder(self, name, parent):
        '''Create a folder in the MEGA account.
        :param name - Name of the new folder
        :param parent - Parent folder
        '''
        self.createFolder(name, parent)

    def move_node_listener(self, node, new_parent, listener):
    	'''Move a node in the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_MOVE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to move
            MegaRequest.getParentHandle - Returns the handle of the new parent for the node
        :param node - Node to move
        :param new_parent - New parent for the node
        :param listener - MegaRequestListener to track this request
        '''
        self.moveNode(node, new_parent, self.create_delegate_request_listener(listener))

    def move_node(self, node, new_parent):
        '''Move a node in the MEGA account.
        :param node - Node to move
        :param new_parent - New parent for the node
        '''
        self.moveNode(node, new_parent)

    def copy_node_listener(self, node, new_parent, listener):
    	'''Copy a node in the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to copy
            MegaRequest.getParentHandle - Returns the handle of the new parent for the new node
            MegaRequest.getPublicMegaNode - Returns the node to copy (if it is a public node)
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getNodeHandle - Handle of the new node
        :param node - Node to copy
        :param new_parent - Parent for the new node
        :param listener - MegaRequestListener to track this request
        '''
        self.copyNode(node, new_parent, self.create_delegate_request_listener(listener))

    def copy_node(self, node, new_parent):
        '''Copy a node in the MEGA account.
        :param node - Node to copy
        :param new_parent - Parent for the new node
        '''
        self.copyNode(node, new_parent)

    def copy_node_new_name_listener(self,node, new_parent, new_name, listener):
    	'''Copy a node in the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to copy
            MegaRequest.getParentHandle - Returns the handle of the new parent for the new node
            MegaRequest.getPublicMegaNode - Returns the node to copy (if it is a public node)
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getNodeHandle - Handle of the new node
        :param node - Node to copy
        :param new_parent - Parent for the new node
        :param new_name - Name for the new node
        :param listener - MegaRequestListener to track this request
        '''
        self.copyNode(node, new_parent, new_name, self.create_delegate_request_listener(listener))

    def copy_node_new_name(self, new_parent, new_name):
        '''Copy a node in the MEGA account
        :param node - Node to copy
        :param new_parent - Parent for the new node
        :param new_name - Name for the new node
        '''
        self.copyNode(node, new_parent, new_name)

    def rename_node_listener(self, node, new_name, listener):
    	'''Rename a node in the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_RENAME Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to rename
            MegaRequest.getName - Returns the new name for the node
        :param node - Node to modify
        :param new_name - New name for the node
        :param listener - MegaRequestListener to track this request
        '''
        self.renameNode(node, new_name, self.create_delegate_request_listener(listener))

    def rename_node(self, node, new_name):
        '''Rename a node in the MEGA accoutn.
        :param node - Node to modify
        :param new_name - New name for the node
        '''
        self.renameNode(node, new_name)

    def remove_with_listener(self, node, listener):
    	'''Remove a node from the MEGA account.
        This function doesn't move the node to the Rubbish Bin, it fully removes the node. To move the node to the Rubbish Bin use MegaApi.moveNode
        The associated request type with this request is MegaRequest.TYPE_REMOVE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to remove
        :param node - Node to remove
        :param listener - MegaRequestListener to track this request
        '''
        self.remove(node, self.create_delegate_request_listener(listener))

    def remove(self, node):
        '''Remove a node from the MEGA account.
        :param node - Node to remove
        '''
        self.remove(node)

    def send_file_to_user_listener(self, node, user, listener):
    	'''Send a node to the Inbox of another MEGA user using a MegaUser.
        The associated request type with this request is MegaRequest.TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to send
            MegaRequest.getEmail - Returns the email of the user that receives the node
        :param node - Node to send
        :param user - User that receives the node
        :param listener - MegaRequestListener to track this request
        '''
        self.sendFileToUser(node, user, self.create_delegate_request_listener(listener))

    def send_file_to_user(self, node, user):
        '''Send a node to the inbox of another MEGA user using a Megauser.
        :param node - Node to send
        :param user - User that receives the node
        '''
        self.sendFileToUser(node, user)

    def share_with_listener(self, node, user, level, listener):
    	'''Share or stop sharing a folder in MEGA with another user using a MegaUser.
        To share a folder with an user, set the desired access level in the level parameter. If you want to stop sharing a folder use the access level MegaShare.ACCESS_UNKNOWN
        The associated request type with this request is MegaRequest.TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the folder to share
            MegaRequest.getEmail - Returns the email of the user that receives the shared folder
            MegaRequest.getAccess - Returns the access that is granted to the user
        :param node - The folder to share. It must be a non-root folder
        :param user - User that receives the shared folder
        :param level - Permissions that are granted to the user Valid values for this parameter:
            MegaShare.ACCESS_UNKNOWN = -1 Stop sharing a folder with this user
            MegaShare.ACCESS_READ = 0
            MegaShare.ACCESS_READWRITE = 1
            MegaShare.ACCESS_FULL = 2
            MegaShare.ACCESS_OWNER = 3
        :param listener - MegaRequestListener to track this request
        '''
        self.share(node, user, level, self.create_delegate_request_listener(listener))

    def share(self, node, user, level):
        '''Share or stop sharing a folder in MEGA with another user using a MegaUser.
        :param node - The folder to share. It must be a non-root folder
        :param user - User that receives the shared folder
        :param level - Permissions that are granted to the user Valid values for this parameter:
            MegaShare.ACCESS_UNKNOWN = -1 Stop sharing a folder with this user
            MegaShare.ACCESS_READ = 0
            MegaShare.ACCESS_READWRITE = 1
            MegaShare.ACCESS_FULL = 2
            MegaShare.ACCESS_OWNER = 3
        '''
        self.share(node, user, level)

    def share_using_email_with_listener(self, node, email, level, listener):
        '''Share or stop sharing a folder in MEGA with another user using his/her email.
        :param node - The folder to share. It must be a non-root folder
        :param email Email of the user that receives the shared folder. If it does not have a MEGA account, the folder will be shared anyway
        and the user will be invited to register an account.
        :param level - Permissions that are granted to the user Valid values for this parameter:
            MegaShare.ACCESS_UNKNOWN = -1 Stop sharing a folder with this user
            MegaShare.ACCESS_READ = 0
            MegaShare.ACCESS_READWRITE = 1
            MegaShare.ACCESS_FULL = 2
            MegaShare.ACCESS_OWNER = 3
        :param listener MegaRequestListener to track the request
        '''
        self.share(node, email, level, self.create_delegate_request_listener(listener))

    def share_using_email(self, node, email, level):
        '''Share or stop sharing a folder in MEGA with another user using his/her email.
        :param node - The folder to share. It must be a non-root folder
        :param email Email of the user that receives the shared folder. If it does not have a MEGA account, the folder will be shared anyway
        and the user will be invited to register an account.
        :param level - Permissions that are granted to the user Valid values for this parameter:
            MegaShare.ACCESS_UNKNOWN = -1 Stop sharing a folder with this user
            MegaShare.ACCESS_READ = 0
            MegaShare.ACCESS_READWRITE = 1
            MegaShare.ACCESS_FULL = 2
            MegaShare.ACCESS_OWNER = 3
        '''
        self.share(node, email, level)

    def import_file_link_using_listener(self, mega_file_link, parent, listener):
    	'''Import a public link to the account.
        The associated request type with this request is MegaRequest.TYPE_IMPORT_LINK Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getLink - Returns the public link to the file
            MegaRequest.getParentHandle - Returns the folder that receives the imported file
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getNodeHandle - Handle of the new node in the account
        :param mega_file_link - Public link to a file in MEGA
        :param parent - Parent folder for the imported file
        :param listener - MegaRequestListener to track this request
        '''
        self.importFileLink(mega_file_link, parent, self.create_delegate_request_listener(listener))

    def import_file_link(self, mega_file_link, parent):
        '''Import a public link to the account.
        :param mega_file_link - Public link to a file in MEGA
        :param parent - Parent folder for the imported file
        '''
        self.importFileLink(mega_file_link, parent)

    def get_public_node_using_listener(self, mega_file_link, listener):
    	'''Get a MegaNode from a public link to a file.
        A public node can be imported using MegaApi.copy_node() or downloaded using MegaApi.start_download()
        The associated request type with this request is MegaRequest.TYPE_GET_PUBLIC_NODE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getLink - Returns the public link to the file
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getPublicMegaNode - Public MegaNode corresponding to the public link
        :param mega_file_link - Public link to a file in MEGA
        :param listener - MegaRequestListener to track this request
        '''
        self.getPublicNode(mega_file_link, self.create_delegate_request_listener(listener))

    def get_public_node(self, mega_file_link):
        '''Get a MegaNode from a public link to a file.
        A public node can be imported using MegaApi.copy_node() or downloaded using MegaApi.start_download()
        :param mega_file_link - Public link to a file in MEGA
        '''
        self.getPublicNode(mega_file_link)

    def get_thumbnail_using_listener(self, node, dst_file_path, listener):
    	'''Get the thumbnail of a node.
        If the node doesn't have a thumbnail the request fails with the MegaError.API_ENOENT error code
        The associated request type with this request is MegaRequest.TYPE_GET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getFile - Returns the destination path
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_THUMBNAIL
        :param node - Node to get the thumbnail
        :param dst_file_path - Destination path for the thumbnail. If this path is a local folder,
        it must end with a '\' or '/' character and (Base64-encoded handle + "0.jpg") will be used as the file name inside that folder.
        If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        :param listener - MegaRequestListener to track this request
        '''
        self.getThumbnail(node, dst_file_path, self.create_delegate_request_listener(listener))

    def get_thumbnail(self, node, dst_file_path):
        '''Get the thumbnail of a node.
        If the node doesn't have a thumbnail the request fails with the MegaError.API_ENOENT error code
        :param node - Node to get the thumbnail
        :param dst_file_path - Destination path for the thumbnail. If this path is a local folder,
        it must end with a '\' or '/' character and (Base64-encoded handle + "0.jpg") will be used as the file name inside that folder.
        If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        '''
        self.getThumbnail(node, dst_file_path)

    def get_preview_using_listener(self, node, dst_file_path, listener):
    	'''Get the preview of a node.
        If the node doesn't have a preview the request fails with the MegaError.API_ENOENT error code
        The associated request type with this request is MegaRequest.TYPE_GET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getFile - Returns the destination path
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_PREVIEW
        :param node - Node to get the preview
        :param dst_file_path - Destination path for the preview. If this path is a local folder,
        it must end with a '\' or '/' character and (Base64-encoded handle + "1.jpg") will be used
        as the file name inside that folder. If the path doesn't finish with one of these
        characters, the file will be downloaded to a file in that path.
        :param listener - MegaRequestListener to track this request
        '''
        self.getPreview(node, dst_file_path, self.create_delegate_request_listener(listener))

    def get_preview(self, node, dst_file_path):
    	'''Get the preview of a node.
        If the node doesn't have a preview the request fails with the MegaError.API_ENOENT error code
        :param node - Node to get the preview
        :param dst_file_path - Destination path for the preview. If this path is a local folder,
        it must end with a '\' or '/' character and (Base64-encoded handle + "1.jpg") will be used
        as the file name inside that folder. If the path doesn't finish with one of these
        characters, the file will be downloaded to a file in that path.
        '''
        self.getPreview(node, dst_file_path)

    def get_user_avatar_with_listener(self, user, dst_file_path, listener):
    	'''Get the avatar of a MegaUser.
        The associated request type with this request is MegaRequest.TYPE_GET_ATTR_USER Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getFile - Returns the destination path
            MegaRequest.getEmail - Returns the email of the user
        :param user - MegaUser to get the avatar
        :param dst_file_path - Destination path for the avatar. It has to be a path to a file, not to a folder.
        If this path is a local folder, it must end with a '\' or '/' character and (email + "0.jpg") will be
        used as the file name inside that folder. If the path doesn't finish with one of these characters,
        the file will be downloaded to a file in that path.
        :param listener - MegaRequestListener to track this request
        '''
        self.getUserAvatar(user, dst_file_path, self.create_delegate_request_listener(listener))

    def get_user_avatar(self, user, dst_file_path):
        '''Get the avatar of a MegaUser.
        :param user - MegaUser to get the avatar
        :param dst_file_path - Destination path for the avatar. It has to be a path to a file, not to a folder.
        If this path is a local folder, it must end with a '\' or '/' character and (email + "0.jpg") will be
        used as the file name inside that folder. If the path doesn't finish with one of these characters,
        the file will be downloaded to a file in that path.
        '''
        self.getUserAvatar(user, dst_file_path)

    def get_user_attribute_with_listener(self, user, type, listener):
        '''Get an attribute of a MegaUser.
        The associated request type with this request is MegaRequest.TYPE_GET_ATTR_USER
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getParamType() - Returns the attribute type
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getText() - Returns the value of the attribute
        :param user MegaUser to get the attribute
        :param type Attribute type. Valid values are:
            MegaApi.USER_ATTR_FIRSTNAME = 1 Get the firstname of the user
            MegaApi.USER_ATTR_LASTNAME = 2 Get the lastname of the user
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.getUserAttribute(user, type, self.create_delegate_request_listener(listener))

    def get_user_attribute(self, user, type):
        '''Get an attribute of a MegaUser.
        :param user MegaUser to get the attribute
        :param type Attribute type. Valid values are:
            MegaApi.USER_ATTR_FIRSTNAME = 1 Get the firstname of the user
            MegaApi.USER_ATTR_LASTNAME = 2 Get the lastname of the user
        '''
        self.getUserAttribute(user, type)

    def get_user_attribute_by_type_with_listener(self, type, listener):
        '''Get an attribute of the current account.
        The associated request type with this request is MegaRequest.TYPE_GET_ATTR_USER.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getParamType() - Returns the attribute type
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getText() - Returns the value of the attribute.
        :param type Attribute type. Valid values are:
            MegaApi.USER_ATTR_FIRSTNAME = 1 Get the firstname of the user.
            MegaApi.USER_ATTR_LASTNAME = 2 Get the lastname of the user
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.getUserAttribute(type, self.create_delegate_request_listener(listener))

    def get_user_attribute_by_type(self, type):
        '''Get an attribute of the current account.
        :param type Attribute type. Valid values are:
            MegaApi.USER_ATTR_FIRSTNAME = 1 Get the firstname of the user.
            MegaApi.USER_ATTR_LASTNAME = 2 Get the lastname of the user
        '''
        self.getUserAttribute(type)

    def cancel_get_thumbnail_with_listener(self, node, listener):
    	'''Cancel the retrieval of a thumbnail.
        The associated request type with this request is MegaRequest.TYPE_CANCEL_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_THUMBNAIL
        :param node - Node to cancel the retrieval of the preview
        :param listener - listener	MegaRequestListener to track this request
        '''
        self.cancelGetThumbnail(node, self.create_delegate_request_listener(listener))

    def cancel_get_thumbnail(self, node):
    	'''Cancel the retrieval of a thumbnail.
        :param node - Node to cancel the retrieval of the preview
        '''
        self.cancelGetThumbnail(node)

    def cancel_get_preview_with_listener(self, node, listener):
    	'''Cancel the retrieval of a preview.
        The associated request type with this request is MegaRequest.TYPE_CANCEL_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_PREVIEW
        :param node - Node to cancel the retrieval of the preview
        :param listener - listener	MegaRequestListener to track this request
        '''
        self.cancelGetPreview(node, self.create_delegate_request_listener(listener))

    def cancel_get_preview(self, node):
    	'''Cancel the retrieval of a preview.
        :param node - Node to cancel the retrieval of the preview
        '''
        self.cancelGetPreview(node)

    def set_thumbnail_with_listener(self, node, src_file_path, listener):
    	'''Set the thumbnail of a MegaNode.
        The associated request type with this request is MegaRequest.TYPE_SET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getFile - Returns the source path
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_THUMBNAIL
        :param node - MegaNode to set the thumbnail
        :param src_file_path - Source path of the file that will be set as thumbnail
        :param listener - MegaRequestListener to track this request
        '''
        self.setThumbnail(node, src_file_path, self.create_delegate_request_listener(listener))

    def set_thumbnail(self, node, src_file_path):
    	'''Set the thumbnail of a MegaNode.
        :param node - MegaNode to set the thumbnail
        :param src_file_path - Source path of the file that will be set as thumbnail
        '''
        self.setThumbnail(node, src_file_path)

    def set_preview_with_listener(self, node, src_file_path, listener):
    	'''Set the preview of a MegaNode.
        The associated request type with this request is MegaRequest.TYPE_SET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getFile - Returns the source path
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_PREVIEW
        :param node - MegaNode to set the preview
        :param src_file_path - Source path of the file that will be set as preview
        :param listener - MegaRequestListener to track this request
        '''
        self.setPreview(node, src_file_path, self.create_delegate_mega_listener(listener))

    def set_preview(self, node, src_file_path):
    	'''Set the preview of a MegaNode.
        :param node - MegaNode to set the preview
        :param src_file_path - Source path of the file that will be set as preview
        '''
        self.setPreview(node, src_file_path)

    def set_avatar_with_listener(self, src_file_path, listener):
    	'''Set the avatar of the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_SET_ATTR_USER Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getFile - Returns the source path
        :param src_file_path - Source path of the file that will be set as avatar
        :param listener - MegaRequestListener to track this request
        '''
        self.setAvatar(src_file_path, self.create_delegate_request_listener(listener))

    def set_avatar(self, src_file_path):
    	'''Set the avatar of the MEGA account.
        :param src_file_path - Source path of the file that will be set as avatar
        '''
        self.setAvatar(src_file_path)

    def set_user_attribute_with_listener(self, type, value, listener):
        '''Set an attribute of the current user.
        The associated request type with this request is MegaRequest.TYPE_SET_ATTR_USER
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getParamType() - Returns the attribute type
            MegaRequest.getFile() - Returns the new value for the attribute
        :param type Attribute type. Valid values are:
                 USER_ATTR_FIRSTNAME = 1
                 Change the firstname of the user
                 USER_ATTR_LASTNAME = 2
                 Change the lastname of the user
        :param value  New attribute value
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.setUserAttribute(type, value, self.create_delegate_request_listener(listener))

    def set_user_attribute(self, type, value):
        '''Set an attribute of the current user.
        :param type Attribute type. Valid values are:
                 USER_ATTR_FIRSTNAME = 1
                 Change the firstname of the user
                 USER_ATTR_LASTNAME = 2
                 Change the lastname of the user
        :param value  New attribute value
        '''
        self.setUserAttribute(type, value)

    def export_node_with_listener(self, node, listener):
    	'''Generate a public link of a file/folder in MEGA.
        The associated request type with this request is MegaRequest.TYPE_EXPORT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getAccess - Returns true
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getLink - Public link
        :param node - MegaNode to get the public link
        :param listener - MegaRequestListener to track this request
        '''
        self.exportNode(node, self.create_delegate_request_listener(listener))

    def export_node(self, node):
    	'''Generate a public link of a file/folder in MEGA.
        :param node - MegaNode to get the public link
        '''
        self.exportNode(node)

    def disable_export_with_listener(self, node, listener):
    	'''Stop sharing a file/folder.
        The associated request type with this request is MegaRequest.TYPE_EXPORT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getAccess - Returns false
        :param node - MegaNode to stop sharing
        :param listener - MegaRequestListener to track this request
        '''
        self.disableExport(node, self.create_delegate_request_listener(listener))

    def disable_export(self, node):
    	'''Stop sharing a file/folder.
        :param node - MegaNode to stop sharing
        '''
        self.disableExport(node)

    def fetch_nodes_with_listener(self, listener):
    	'''Fetch the filesystem in MEGA.
        The MegaApi object must be logged in in an account or a public folder to successfully complete this request.
        The associated request type with this request is MegaRequest.TYPE_FETCH_NODES
        :param listener - MegaRequestListener to track this request
        '''
        self.fetchNodes(self.create_delegate_request_listener(listener))

    def fetch_nodes(self):
    	'''Fetch the filesystem in MEGA.
        The MegaApi object must be logged in in an account or a public folder to successfully complete this request.
        '''
        self.fetchNodes()

    def get_account_details_with_listener(self, listener):
    	'''Get details about the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_ACCOUNT_DETAILS
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getMegaAccountDetails - Details of the MEGA account
        :param listener - MegaRequestListener to track this request
        '''
        self.getAccountDetails(self.create_delegate_request_listener(listener))

    def get_account_details(self):
        '''Get details about the MEGA account.
        '''
        self.getAccountDetails()

    def get_extended_account_details_with_listener(self, sessions, purchases, transactions, listener):
        '''Get details about the MEGA account.
        This function allows to optionally get data about sessions, transactions and purchases related to the account.
        The associated request type with this request is MegaRequest.TYPE_ACCOUNT_DETAILS.
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getMegaAccountDetails() - Details of the MEGA account
        :param sessions Boolean. Get sessions history if true. Do not get sessions history if false
        :param purchases Boolean. Get purchase history if true. Do not get purchase history if false
        :param transactions Boolean. Get transactions history if true. Do not get transactions history if false
        :param listener MegaRequestListener to track this request
        '''
        self.getExtendedAccountDetails(sessions, purchases, transactions, self.create_delegate_request_listener(listener))

    def get_extended_account_details(self, sessions, purchases, transactions):
        '''Get details about the MEGA account.
        This function allows to optionally get data about sessions, transactions and purchases related to the account.
        :param sessions Boolean. Get sessions history if true. Do not get sessions history if false
        :param purchases Boolean. Get purchase history if true. Do not get purchase history if false
        :param transactions Boolean. Get transactions history if true. Do not get transactions history if false
        '''
        self.getExtendedAccountDetails(sessions, purchases, transactions)

    def get_extended_account_details_no_transactions(self, sessions, purchases):
        '''Get details about the MEGA account.
        This function allows to optionally get data about sessions, transactions and purchases related to the account.
        :param sessions Boolean. Get sessions history if true. Do not get sessions history if false
        :param purchases Boolean. Get purchase history if true. Do not get purchase history if false
        '''
        self.getExtendedAccountDetails(sessions, purchases)

    def get_extended_account_details_only_sessions(self, sessions):
        '''Get details about the MEGA account.
        This function allows to optionally get data about sessions, transactions and purchases related to the account.
        :param sessions Boolean. Get sessions history if true. Do not get sessions history if false
        '''
        self.getExtendedAccountDetails(sessions)

    def get_all_extended_account_details(self):
        '''Get details about the MEGA account.
        '''
        self.getExtendedAccountDetails()

    def get_pricing_with_listener(self, listener):
    	'''Get the available pricing plans to upgrade a MEGA account.
        You can get a payment URL for any of the pricing plans provided by this function using MegaApi.get_payment_url()
        The associated request type with this request is MegaRequest.TYPE_GET_PRICING
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getPricing - MegaPricing object with all pricing plans
        :param listener - MegaRequestListener to track this request
        '''
        self.getPricing(self.create_delegate_request_listener(listener))

    def get_pricing(self):
    	'''Get the available pricing plans to upgrade a MEGA account.
        '''
        self.getPricing()

    def get_payment_id_with_listener(self, product_handle, listener):
    	'''Get the payment id for an upgrade.
        The associated request type with this request is MegaRequest.TYPE_GET_PAYMENT_ID
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle() - Returns the handle of the product
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getLink() - Payment link
        :param product_handle Handle of the product (see MegaApi.get_pricing())
        :param listener MegaRequestListener to track this request
        '''
        self.getPaymentId(product_handle, self.create_delegate_request_listener(listener))

    def get_payment_id(self, product_handle):
    	'''Get the payment id for an upgrade.
        :param product_handle Handle of the product (see MegaApi.get_pricing())
        '''
        self.getPaymentId(product_handle)

    def upgrade_account_with_listener(self, product_handle, payment_method, listener):
    	'''Upgrade an account.
        :param product_handle Product handle to purchase.
        It is possible to get all pricing plans with their product handles using
        MegaApi.get_pricing()
        The associated request type with this request is MegaRequest.TYPE_UPGRADE_ACCOUNT
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle() - Returns the handle of the product
            MegaRequest.getNumber() - Returns the payment method
        :param payment_method Payment method. Valid values are:
            MegaApi.PAYMENT_METHOD_BALANCE = 0
        Use the account balance for the payment
            MegaApi.PAYMENT_METHOD_CREDIT_CARD = 8
        Complete the payment with your credit card. Use MegaApi.credit_card_store() to add
        a credit card to your account
        :param listener MegaRequestListener to track this request
        '''
        self.upgradeAccount(product_handle, payment_method, self.create_delegate_request_listener(listener))

    def upgrade_account(self, product_handle, payment_method):
    	'''Upgrade an account.
        :param product_handle Product handle to purchase.
        It is possible to get all pricing plans with their product handles using
        MegaApi.get_pricing()
        :param payment_method Payment method. Valid values are:
            MegaApi.PAYMENT_METHOD_BALANCE = 0
        Use the account balance for the payment
            MegaApi.PAYMENT_METHOD_CREDIT_CARD = 8
        Complete the payment with your credit card. Use MegaApi.credit_card_store() to add
        a credit card to your account
        '''
        self.upgradeAccount(product_handle, payment_method)

    def submit_purchase_receipt_with_listener(self, receipt, listener):
    	'''Send the Google Play receipt after a correct purchase of subscription.
        :param receipt String the complete receipt from Google Play
        :param listener MegaRequestListener to track this request
        '''
        self.submitPurchaseReceipt(receipt, self.create_delegate_request_listener(listener))

    def submit_purchase_receipt(self, receipt):
    	'''Send the Google Play receipt after a correct purchase of subscription.
        :param receipt String the complete receipt from Google Play
        '''
        self.submitPurchaseReceipt(receipt)

    def credit_card_store_with_listener(self, address_1, address_2, city, province, country, postal_code,
        first_name, last_name, credit_card, expire_month, expire_year, cv_2, listener):
        '''Store a credit card.
        The associated request type with this request is MegaRequest.TYPE_CREDIT_CARD_STORE
        :param address_1 Billing address
        :param address_2 Second line of the billing address (optional)
        :param city City of the billing address
        :param province Province of the billing address
        :param country Country of the billing address
        :param postal_code Postal code of the billing address
        :param first_name Firstname of the owner of the credit card
        :param last_name Lastname of the owner of the credit card
        :param credit_card Credit card number. Only digits, no spaces nor dashes
        :param expire_month Expire month of the credit card. Must have two digits ("03" for example)
        :param expire_year Expire year of the credit card. Must have four digits ("2010" for example)
        :param cv_2 Security code of the credit card (3 digits)
        :param listener MegaRequestListener to track this request
        '''
        self.creditCardStore(address_1, address_2, city, province, country, postal_code,
            first_name, last_name, credit_card, expire_month, expire_year, cv_2,
            self.create_delegate_request_listener(listener))

    def credit_card_store(self, address_1, address_2, city, province, country, postal_code,
        first_name, last_name, credit_card, expire_month, expire_year, cv_2):
        '''Store a credit card.
        The associated request type with this request is MegaRequest.TYPE_CREDIT_CARD_STORE
        :param address_1 Billing address
        :param address_2 Second line of the billing address (optional)
        :param city City of the billing address
        :param province Province of the billing address
        :param country Country of the billing address
        :param postal_code Postal code of the billing address
        :param first_name Firstname of the owner of the credit card
        :param last_name Lastname of the owner of the credit card
        :param credit_card Credit card number. Only digits, no spaces nor dashes
        :param expire_month Expire month of the credit card. Must have two digits ("03" for example)
        :param expire_year Expire year of the credit card. Must have four digits ("2010" for example)
        :param cv_2 Security code of the credit card (3 digits)
        '''
        self.creditCardStore(address_1, address_2, city, province, country, postal_code,
            first_name, last_name, credit_card, expire_month, expire_year, cv_2)

    def credit_card_query_subscriptions_with_listener(self, listener):
    	'''Get the credit card subscriptions of the account.
        The associated request type with this request is MegaRequest.TYPE_CREDIT_CARD_QUERY_SUBSCRIPTIONS
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getNumber() - Number of credit card subscriptions
        :param listener MegaRequestListener to track this request
        '''
        self.creditCardQuerySubscriptions(self.create_delegate_request_listener(listener))

    def credit_card_query_subscriptions(self):
    	'''Get the credit card subscriptions of the account.
        '''
        self.creditCardQuerySubscriptions())

    def credit_card_cancel_subscriptions_with_listener(self, reason,  listener):
    	'''Cancel credit card subscriptions of the account.
        The associated request type with this request is MegaRequest.TYPE_CREDIT_CARD_CANCEL_SUBSCRIPTIONS
        :param reason for cancellation it can be None
        :param listener MegaRequestListener to track this request
        '''
        self.creditCardCancelSubscriptions(reason, self.create_delegate_request_listener(listener))

    def credit_card_cancel_subscriptions(self, reason):
    	'''Cancel credit card subscriptions of the account.
        :param reason for cancellation it can be None
        '''
        self.creditCardCancelSubscriptions(reason)

    def get_payment_methods_with_listener(self, listener):
    	'''Get the available payment methods.
        The associated request type with this request is MegaRequest.TYPE_GET_PAYMENT_METHODS
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getNumber() - Bitfield with available payment methods
        To identify if a payment method is available, the following check can be performed:
        request.getNumber() & (1 << MegaApi.PAYMENT_METHOD_CREDIT_CARD) != 0)
        :param listener MegaRequestListener to track this request
        '''
        self.getPaymentMethods(self.create_delegate_request_listener(listener))

    def get_payment_methods(self):
    	'''Get the available payment methods.
        '''
        self.getPaymentMethods()

    def export_master_key(self):
    	'''Export the master key of the account.
        The returned value is a Base64-encoded string
        With the master key, it's possible to start the recovery of an account when the password is lost:
            https://mega.co.nz/#recovery
        You take the ownership of the returned value.
        :Returns Base64-encoded master key
        '''
        return self.exportMasterKey()

    def change_password_with_listener(self, old_pass, new_pass, listener):
    	'''Change the password of the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_CHANGE_PW Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getPassword - Returns the old password
            MegaRequest.getNewPassword - Returns the new password
        :param old_pass - old password
        :param new_pass - new password
        :param listener - MegaRequestListener to track this request
        '''
        self.changePassword(old_pass, new_pass, self.create_delegate_request_listener(listener))

    def change_password(self, old_pass, new_pass):
    	'''Change the password of the MEGA account.
        :param old_pass - old password
        :param new_pass - new password
        '''
        self.changePassword(old_pass, new_pass)
        
    def add_contact(self, *args):
    	'''Add a new contact to the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_ADD_CONTACT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail - Returns the email of the contact
        :param email - Email of the new contact
        :param listener - MegaRequestListener to track this request
        '''
        return self.addContact(self.api, *args)

    def invite_contact(self, *args):
    	'''need clarification'''
        return self.inviteContact(self.api, *args)

    def reply_contact_request(self, *args):
    	'''need clarification'''
        return self.replyContactRequest(self.api, *args)

    def remove_contact(self, *args):
    	'''Remove a contact to the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_REMOVE_CONTACT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail - Returns the email of the contact
        :param user - 	MegaUser of the contact (see MegaApi.getContact)
        :param listener - MegaRequestListener to track this request
        '''
        return self.removeContact(self.api, *args)

    def logout(self, listener=None):
    	'''Logout of the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_LOGOUT
        :param listener - MegaRequestListener to track this request
        '''
        return self.logout(self.api, listener)

    def local_logout(self, listener=None):
    	'''need clarification'''
        return self.localLogout(self.api, listener)

    def submit_feedback(self, *args):
    	'''need clarification'''
        return self.submitFeedback(self.api, *args)

    def report_debug_event(self, *args):
    	'''need clarification'''
        return self.reportDebugEvent(self.api, *args)

    def start_upload(self, *args):
    	'''Upload a file.
        :param localPath - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param listener - MegaTransferListener to track this transfer
        '''
        return self.startUpload(self.api, *args)

    def start_download(self, *args):
    	'''Download a file from MEGA.
        :param node - MegaNode that identifies the file
        :param localPath - Destination path for the file If this path is a local folder, it must end with a '\' or '/' character and the file name in MEGA will be used to store a file inside that folder. If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        :param listener - MegaTransferListener to track this transfer
        '''
        return self.startDownload(self.api, *args)

    def start_streaming(self, *args):
    	'''Start an streaming download.
        Streaming downloads don't save the downloaded data into a local file. It is provided in MegaTransferListener.onTransferUpdate in a byte buffer.
        Only the MegaTransferListener passed to this function will receive MegaTransferListener.onTransferData callbacks. MegaTransferListener objects registered with MegaApi.addTransferListener won't receive them for performance reasons
        :param node - MegaNode that identifies the file (public nodes aren't supported yet)
        :param startPos - First byte to download from the file
        :param size - Size of the data to download
        :param listener - MegaTransferListener to track this transfer
        '''
        return self.startStreaming(self.api, *args)

    def cancel_transfer(self, *args):
    	'''Cancel a transfer.
        When a transfer is cancelled, it will finish and will provide the error code MegaError.API_EINCOMPLETE in MegaTransferListener.onTransferFinish and MegaListener.onTransferFinish
        The associated request type with this request is MegaRequest.TYPE_CANCEL_TRANSFER Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getTransferTag - Returns the tag of the cancelled transfer (MegaTransfer.getTag)
        :param transfer - MegaTransfer object that identifies the transfer You can get this object in any MegaTransferListener callback or any MegaListener callback related to transfers.
        :param listener - MegaRequestListener to track this request
        '''
        return self.cancelTransfer(self.api, *args)

    def cancel_transfer_by_tag(self, *args):
    	'''need clarification'''
        return self.cancelTransferByTag(self.api, *args)

    def cancel_transfers(self, *args):
    	'''Cancel all transfers of the same type.
        The associated request type with this request is MegaRequest.TYPE_CANCEL_TRANSFERS Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getParamType - Returns the first parameter
        :param type - 	Type of transfers to cancel. Valid values are:
            MegaTransfer.TYPE_DOWNLOAD = 0
            MegaTransfer.TYPE_UPLOAD = 1
        :param listener - MegaRequestListener to track this request
        '''
        return self.cancelTransfers(self.api, *args)

    def pause_transfers(self, *args):
    	'''Pause/resume all transfers.
        The associated request type with this request is MegaRequest.TYPE_PAUSE_TRANSFERS Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getFlag - Returns the first parameter
        :param pause - True to pause all transfers or False to resume all transfers
        :param listener - MegaRequestListener to track this request
        '''
        return self.pauseTransfers(self.api, *args)

    def are_tansfers_paused(self, *args):
    	'''need clarification'''
        return self.areTansfersPaused(self.api, *args)

    def set_upload_limit(self, *args):
    	'''Set the upload speed limit.
        The limit will be applied on the server side when starting a transfer. Thus the limit won't be applied for already started uploads and it's applied per storage server.
        :param bpslimit - -1 to automatically select the limit, 0 for no limit, otherwise the speed limit in bytes per second
        '''
        return self.setUploadLimit(self.api, *args)

    def set_download_method(self, *args):
    	'''need clarification'''
        return self.setDownloadMethod(self.api, *args)

    def set_upload_method(self, *args):
    	'''need clarification'''
        return self.setUploadMethod(self.api, *args)

    def get_download_method(self):
    	'''need clarification'''
        return self.getDownloadMethod(self.api)

    def get_upload_method(self):
    	'''need clarification'''
        return self.getUploadMethod(self.api)

    def get_transfer_by_tag(self, *args):
    	'''need clarification'''
        return self.getTransferByTag(self.api, *args)

    def update(self):
    	'''Force a loop of the SDK thread.'''
        return self.update(self.api)

    def is_waiting(self):
    	'''Check if the SDK is waiting for the server.
		:Returns true if the SDK is waiting for the server to complete a request
		'''
        return self.isWaiting(self.api)

    def get_num_pending_uploads(self):
    	'''Get the number of pending uploads.
		:Returns the number of pending uploads.
		'''
        return self.getNumPendingUploads(self.api)

    def get_num_pending_downloads(self):
    	'''Get the number of pending downloads.
		:Returns the number of pending downloads.
		'''
        return self.getNumPendingDownloads(self.api)

    def get_total_uploads(self):
    	'''Get the number of queued uploads since the last call to MegaApi.resetTotalUploads.
		:Returns number of queued uploads since the last call to MegaApi.resetTotalUploads
		'''
        return self.getTotalUploads(self.api)

    def get_total_downloads(self):
    	'''Get the number of queued uploads since the last call to MegaApi.resetTotalDownloads.
		:Returns number of queued uploads since the last call to MegaApi.resetTotalDownloads
		'''
        return self.getTotalDownloads(self.api)

    def reset_total_downloads(self):
    	'''Reset the number of total downloads This function resets the number returned by MegaApi.getTotalDownloads.
		'''
        return self.resetTotalDownloads(self.api)

    def reset_total_uploads(self):
    	'''Reset the number of total uploads This function resets the number returned by MegaApi.getTotalUploads.
		'''
        return self.resetTotalUploads(self.api)

    def get_total_downloaded_bytes(self):
    	'''Get the total downloaded bytes since the creation of the MegaApi object.
		:Returns total downloaded bytes since the creation of the MegaApi object
		'''
        return self.getTotalDownloadedBytes(self.api)

    def getTotalUploadedBytes(self):
    	'''Get the total uploaded bytes since the creation of the MegaApi object.
		:Returns total uploaded bytes since the creation of the MegaApi object
		'''
        return self.getTotalUploadedBytes(self.api)

    def updateStats(self):
    	'''Force a loop of the SDK thread. '''
        return self.updateStats(self.api)

    def get_num_children(self, *args):
    	'''Get the number of child nodes.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child nodes.
        :param parent - Parent node
        :Returns Number of child nodes
        '''
        return self.getNumChildren(self.api, *args)

    def get_num_child_files(self, *args):
    	'''Get the number of child files of a node.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child files.
        :parent parent - Parent node
        :Returns Number of child files
        '''
        return self.getNumChildFiles(self.api, *args)

    def get_num_child_folders(self, *args):
    	'''Get the number of child folders of a node.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child folders.
        :param parent - Parent node
        :Returns Number of child folders
        '''
        return self.getNumChildFolders(self.api, *args)

    def get_index(self, *args):
    	'''Get the current index of the node in the parent folder for a specific sorting order.
        If the node doesn't exist or it doesn't have a parent node (because it's a root node) this function returns -1
        :param node - Node to check
        :param order - Sorting order to use
        :Returns index of the node in its parent folder
        '''
        return self.getIndex(self.api, *args)

    def get_child_node(self, *args):
    	'''Get the child node with the provided name.
        If the node doesn't exist, this function returns None
        You take the ownership of the returned value
        :param parent - Parent node
        :param name - name of the node
        :Returns The MegaNode that has the selected parent and name
        '''
        return self.getChildNode(self.api, *args)

    def get_parent_node(self, *args):
    	'''Get the parent node of a MegaNode.
        If the node doesn't exist in the account or it is a root node, this function returns NULL
        You take the ownership of the returned value.
        :param node - MegaNode to get the parent
        :Returns the parent of the provided node
        '''
        return self.getParentNode(self, *args)

    def get_node_path(self, *args):
    	'''Get the path of a MegaNode.
        If the node doesn't exist, this function returns NULL. You can recoved the node later using MegaApi.getNodeByPath except if the path contains names with '/', '\' or ':' characters.
        You take the ownership of the returned value
        :param node - MegaNode for which the path will be returned
        :Returns the path of the node
        '''
        return self.getNodePath(self.api, *args)

    def get_node_by_path(self, *args):
    	'''Get the MegaNode in a specific path in the MEGA account.
        The path separator character is '/' The Root node is / The Inbox root node is //in/ The Rubbish root node is //bin/
        Paths with names containing '/', '\' or ':' aren't compatible with this function.
        It is needed to be logged in and to have successfully completed a fetchNodes request before calling this function. Otherwise, it will return None.
        You take the ownership of the returned value
        :param path - Path to check
        :param n - Base node if the path is relative
        :Returns The MegaNode object in the path, otherwise None
        '''
        return self.getNodeByPath(self.api, *args)

    def get_node_by_handle(self, *args):
    	'''Get the MegaNode that has a specific handle.
        You can get the handle of a MegaNode using MegaNode.getHandle. The same handle can be got in a Base64-encoded string using MegaNode.getBase64Handle. Conversions between these formats can be done using MegaApi.base64ToHandle and MegaApi.handleToBase64.
        It is needed to be logged in and to have successfully completed a fetchNodes request before calling this function. Otherwise, it will return None.
        You take the ownership of the returned value.
        :param MegaHandler - Node handle to check
        :Returns MegaNode object with the handle, otherwise None
        '''
        return self.getNodeByHandle(self.api, *args)

    def get_contact_request_by_handle(self, *args):
    	'''need clarification'''
        return self.getContactRequestByHandle(self.api, *args)


    def get_contact(self, *args):
    	'''Get the MegaUser that has a specific email address.
        You can get the email of a MegaUser using MegaUser.getEmail
        You take the ownership of the returned value
        :param email - Email address to check
        :Returns MegaUser that has the email address, otherwise None
        '''
        return self.getContact(self.api, *args)



    def is_shared(self, *args):
    	'''Check if a MegaNode is being shared.
        For nodes that are being shared, you can get a a list of MegaShare objects using MegaApi.getOutShares
        :param node - Node to check
        :Returns True if the MegaNode is being shared, otherwise false
        '''
        return self.isShared(self.api, *args)


    def get_access(self, *args):
    	'''Get the access level of a MegaNode.
        :param node - MegaNode to check
        :Returns Access level of the node Valid values are:
            MegaShare.ACCESS_OWNER
            MegaShare.ACCESS_FULL
            MegaShare.ACCESS_READWRITE
            MegaShare.ACCESS_READ
            MegaShare.ACCESS_UNKNOWN
        '''
        return self.getAccess(self.api, *args)

    def get_size(self, *args):
    	'''Get the size of a node tree.
        If the MegaNode is a file, this function returns the size of the file. If it's a folder, this fuction returns the sum of the sizes of all nodes in the node tree.
        :param node - Parent node
        :Returns size of the node tree
        '''
        return self.getSize(self.api, *args)

    def get_fingerprint(self, *args):
    	'''Get a Base64-encoded fingerprint for a node.
        If the node doesn't exist or doesn't have a fingerprint, this function returns None.
        You take the ownership of the returned value
        :param node - Node for which we want to get the fingerprint
        :Returns Base64-encoded fingerprint for the file
        '''
        return self.getFingerprint(self.api, *args)

    def get_node_by_fingerprint(self, *args):
    	'''Returns a node with the provided fingerprint.
        If there isn't any node in the account with that fingerprint, this function returns None.
        You take the ownership of the returned value.
        :param fingerprint - Fingerprint to check
        :Returns MegaNode object with the provided fingerprint
        '''
        return self.getNodeByFingerprint(self.api, *args)

    def has_fingerprint(self, *args):
    	'''Check if the account already has a node with the provided fingerprint.
        A fingerprint for a local file can be generated using MegaApi.getFingerprint
        :param fingerprint - Fingerprint to check
        :Returns True if the account contains a node with the same fingerprint
        '''
        return self.hasFingerprint(self.api, *args)

    def get_CRC(self, *args):
    	'''need clarification'''
        return self.getCRC(self.api, *args)

    def get_node_by_CRC(self, *args):
    	'''need clarification'''
        return self.getNodeByCRC(self.api, *args)

    def check_access(self, *args):
    	'''Check if a node has an access level.
        :param node - Node to check
        :param level - Access level to check Valid values for this parameter are:
            MegaShare.ACCESS_OWNER
            MegaShare.ACCESS_FULL
            MegaShare.ACCESS_READWRITE
            MegaShare.ACCESS_READ
        :Returns MegaError object with the result: Valid values for the error code are:
            MegaError.API_OK - The node can be moved to the target
            MegaError.API_EACCESS - The node can't be moved because of permissions problems
            MegaError.API_ECIRCULAR - The node can't be moved because that would create a circular linkage
            MegaError.API_ENOENT - The node or the target doesn't exist in the account
            MegaError.API_EARGS - Invalid parameters
        '''
        return self.checkAccess(self.api, *args)

    def check_move(self, *args):
    	'''Check if a node can be moved to a target node.
        node - Node to check
        target - Target for the move operation
        :Returns MegaError object with the result: Valid values for the error code are:
            MegaError.API_OK - The node can be moved to the target
            MegaError.API_EACCESS - The node can't be moved because of permissions problems
            MegaError.API_ECIRCULAR - The node can't be moved because that would create a circular linkage
            MegaError.API_ENOENT - The node or the target doesn't exist in the account
            MegaError.API_EARGS - Invalid parameters
        '''
        return self.checkMove(self.api, *args)

    def get_root_node(self):
    	'''Returns the root node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi.fetchNodes before, this function returns None
        :Returns Root node of the account
        '''
        return self.getRootNode(self.api)

    def get_inbox_node(self):
    	'''Returns the inbox node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi.fetchNodes before, this function returns None
        :Returns Inbox node of the account
        '''
        return self.getInboxNode(self.api)

    def get_rubbish_node(self):
    	'''Returns the rubbish node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi.fetchNodes before, this function returns None
        :Returns Rubbish node of the account
        '''
        return self.getRubbishNode(self.api)

    def process_mega_tree(self, *args):
    	'''Process a node tree using a MegaTreeProcessor implementation.
		:param node - The parent node of the tree to explore
		:param processor - MegaTreeProcessor that will receive callbacks for every node in the tree
		:param recursive - True if you want to recursively process the whole node tree. False if you want to process the children of the node only
		:Returns True  if all nodes were processed. False otherwise (the operation can be cancelled by MegaTreeProcessor.processMegaNode())
        '''
        return self.processMegaTree(self.api, *args)

    def create_public_file_node(self, *args):
    	'''need clarification'''
        return self.createPublicFileNode(self.api, *args)

    def create_public_folder_node(self, *args):
    	'''need clarification'''
        return self.createPublicFolderNode(self.api, *args)

    def get_version(self):
    	'''need clarification'''
        return self.getVersion(self.api)

    def get_user_agent(self):
    	'''need clarification'''
        return self.getUserAgent(self.api)

    def change_api_url(self, *args):
    	'''need clarification'''
        return self.changeApiUrl(self.api, *args)

    def escape_fs_incompatible(self, *args):
    	'''need clarification'''
        return self.escapeFsIncompatible(self.api, *args)

    def unescape_fs_incompatible(self, *args):
    	'''need clarification'''
        return self.unescapeFsIncompatible(self.api, *args)

    def create_thumbnail(self, *args):
    	'''need clarification'''
        return self.createThumbnail(self.api, *args)

    def create_preview(self, *args):
    	'''need clarification'''
        return self.createPreview(self.api, *args)

    def get_contacts(self):
    	'''Get all contacts of this MEGA account.
        You take the ownership of the returned value
        :Returns List of MegaUser object with all contacts of this account
        '''
        return self.user_list_to_array(self.getContacts())

    def get_in_shares(self, user):
    	'''Get a list with all inbound sharings from one MegaUser.
        You take the ownership of the returned value
        :param user - MegaUser sharing folders with this account
        :Returns List of MegaNode objects that this user is sharing with this account
        '''
        return self.node_list_to_array(self.getInShares(user))

    def get_all_in_shares(self):
    	'''Get a list with all inbound sharings.
        You take the ownership of the returned value
        :Returns List of MegaNode objects that this user is sharing with this account
        '''
        return self.node_list_to_array(self.getInShares())

    def get_children(self, parent, order):
    	'''Get all children of a MegaNode.
        If the parent node doesn't exist or it isn't a folder, this function returns None
        You take the ownership of the returned value
        :param parent - parent node
        :param order Order of the returned list. Valid values are:
            MegaApi.ORDER_NONE = 0 Undefined order
            MegaApi.ORDER_DEFAULT_ASC = 1 Folders first in alphabetical order, then files in the same order
            MegaApi.ORDER_DEFAULT_DESC = 2 Files first in reverse alphabetical order, then folders in the same order
            MegaApi.ORDER_SIZE_ASC = 3 Sort by size, ascending
            MegaApi.ORDER_SIZE_DESC = 4 Sort by size, descending
            MegaApi.ORDER_CREATION_ASC = 5 Sort by creation time in MEGA, ascending
            MegaApi.ORDER_CREATION_DESC = 6 Sort by creation time in MEGA, descending
            MegaApi.ORDER_MODIFICATION_ASC = 7 Sort by modification time of the original file, ascending
            MegaApi.ORDER_MODIFICATION_DESC = 8 Sort by modification time of the original file, descending
            MegaApi.ORDER_ALPHABETICAL_ASC = 9 Sort in alphabetical order, ascending
            MegaApi.ORDER_ALPHABETICAL_DESC = 10 Sort in alphabetical order, descending
        :Returns list of MegaNode object that are children of the given parent object
        '''
        return self.node_list_to_array(self.getChildren(parent, order))

    def get_out_shares(self, node):
    	'''Get a list with the active outbound sharings for a MegaNode.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :param node - MegaNode to check
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.getOutShares(node))

    def get_all_out_shares(self):
    	'''Get a list with the active outbound sharings for the current account.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.getOutShares())

    def get_pending_out_shares(self, node):
    	'''Get a list with the pending outbound sharings for a MegaNode.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :param node - MegaNode to check
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.getPendingOutShares(node))

    def get_all_pending_out_shares(self):
    	'''Get a list with the pending outbound sharings for the current account.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.getPendingOutShares())

    def get_incoming_contact_requests(self):
        '''Get a list with all incoming contact requests
        :Returns list of MegaContactRequest objects
        '''
        return self.contact_request_list_to_array(self.getIncomingContactRequests())

    def get_outgoing_contact_requests(self):
        '''Get a list with all outgoing contact requests
        :Returns list of MegaContactRequest objects
        '''
        return self.contact_request_list_to_array(self.getOutgoingContactRequests())

    def search(self, parent, search_string):
    	'''Search nodes containing a search string in their name.
		The search is case-insensitive.
    	:param node	The parent node of the tree to explore
    	:param searchString	Search string. The search is case-insensitive
		:Returns list of nodes that contain the desired string in their name
    	'''
        return self.node_list_to_array(super(MegaApiPython, self).search(parent, search_string))

    def search_recursively(self, parent, search_string, recursive):
    	'''Search nodes containing a search string in their name.
		The search is case-insensitive.
    	:param node	The parent node of the tree to explore
    	:param searchString	Search string. The search is case-insensitive
    	:param recursive	True if you want to seach recursively in the node tree. False if you want to seach in the children of the node only
		:Returns list of nodes that contain the desired string in their name
    	'''
        return self.node_list_to_array(super(MegaApiPython, self).search(parent, search_string, recursive))

    def get_transfers(self):
    	'''Get all active transfers.
		You take the ownership of the returned value
		:Returns list with all active downloads or uploads
		'''
        return self.transfer_list_to_array(self.getTransfers())

    def get_transfers_based_on_type(self, type):
    	'''Get all active transfers based on type.
		You take the ownership of the returned value
		:Returns list with all active downloads or uploads
		'''
        return self.transfer_list_to_array(self.getTransfers(type))

    # PRIVATE METHODS

    # Listener creation

    def create_delegate_mega_listener(self, listener):
        '''Create a new delegate listener object of type DelegateMegaListener
        and attempts to add it to the corresponding list. If the listener object is none,
        returns None
        :param listener Listener object associated with the new delegate
        :Returns the newly created delegate listener object
        '''
        if listener is None:
            return None
        delegate_listener = DelegateMegaListener(self, listener)
        self.lock.acquire()
        try:
            self.active_mega_listeners.append(delegate_listener)
        finally:
            self.lock.release()
        return delegate_listener

    def create_delegate_mega_global_listener(self, listener):
        '''Create a new delegate listener object of type DelegateMegaGlobalListener
        and attempts to add it to the corresponding list.If the listener object is none,
        returns None
        :param listener Listener object associated with the new delegate
        :Returns the newly created delegate global listener object
        '''
        if listener is None:
            return None
        delegate_global_listener = DelegateMegaGlobalListener(self, listener)
        self.lock.acquire()
        try:
            self.active_global_mega_listeners.append(delegate_global_listener)
        finally:
            self.lock.release()
        return delegate_global_listener

    def create_delegate_request_listener(self, listener ,single):
        '''Create a new delegate listener object of type DelegateMegaRequestListener
        and attempts to add it to the corresponding list. If the listener object is none,
        returns None
        :param listener Listener object associated with the new delegate
        :Returns the newly created delegate request listener object
        '''
        if listener is None:
            return None
        delegate_request_listener = DelegateMegaRequestListener(self, listener, single)
        self.lock.acquire()
        try:
            self.active_request_listeners.append(delegate_request_listener)
        finally:
            self.lock.release()
        return delegate_request_listener

    def create_delegate_transfer_listener(self, listener, single):
        '''Create a new delegate listener object of type DelegateMegaTransferListener
        and attempts to add it to the corresponding list. If the listener object is none,
        returns None
        :param listener Listener object associated with the new delegate
        :Returns the newly created delegate transfer listener object
        '''
        if listener is None:
            return None
        delegate_transfer_listener = DelegateMegaTransferListener(self, listener, single)
        self.lock.acquire()
        try:
            self.active_transfer_listeners.append(delegate_transfer_listener)
        finally:
            self.lock.release()
        return delegate_transfer_listener

    def free_request_listener(self, delegate):
        '''Attempts to remove the delegate object of type DelegateMegaRequestListener
         from the corresponding list.
        '''
        self.lock.acquire()
        try:
            self.active_request_listeners.remove(delegate)
        finally:
            self.lock.release()

    def free_transfer_listener(self, delegate):
        '''Attempts to remove the delegate object of type DelegateMegaTransferListener
         from the corresponding list.
        '''
        self.lock.acquire()
        try:
            self.active_transfer_listeners.remove(delegate)
        finally:
            self.lock.release()


    # List management

    def user_list_to_array(self, user_list):
        '''This function is used to convert an SDK list of MegaUser objects which is not iterable
        in Python to an iterable Python list which can then be properly used.
        :param user_list List of MegaUser objects to convert
        :Returns an iterable list of MegaUser objects
        '''
        if user_list is None:
            return None
        result = []
        for user in range(user_list.size()):
            result.append(user_list.get(user).copy())
        return result

    def transfer_list_to_array(self, transfer_list):
        '''This function is used to convert an SDK list of MegaTransfer objects which is not iterable
        in Python to an iterable Python list which can then be properly used.
        :param transfer_list List of MegaTransfer objects to convert
        :Returns an iterable list of MegaTransfer objects
        '''
        if transfer_list is None:
            return None
        result = []
        for transfer in range(transfer_list.size()):
            result.append(transfer_list.get(transfer).copy())
        return result

    def contact_request_list_to_array(self, request_list):
        '''This function is used to convert an SDK list of MegaContactRequest objects which is not iterable
        in Python to an iterable Python list which can then be properly used.
        :param request_list List of MegaContactRequest objects to convert
        :Returns an iterable list of MegaContactRequest objects
        '''
        if request_list is None:
            return None
        result = []
        for request in range(request_list.size()):
            result.append(request_list.get(request).copy())
        return result

    def share_list_to_array(self, share_list):
        '''This function is used to convert an SDK list of MegaShare objects which is not iterable
        in Python to an iterable Python list which can then be properly used.
        :param share_list List of MegaShare objects to convert
        :Returns an iterable list of MegaShare objects
        '''
        if share_list is None:
            return None
        result = []
        for share in range(share_list.size()):
            result.append(share_list.get(share).copy())
        return result

    def node_list_to_array(self, node_list):
        '''This function is used to convert an SDK list of MegaNode objects which is not iterable
        in Python to an iterable Python list which can then be properly used.
        :param node_list List of MegaNode objects to convert
        :Returns an iterable list of MegaNode objects
        '''
        if node_list is None:
            return None
        result = []
        for node in range(node_list.size()):
            result.append(node_list.get(node).copy())
        return result


class DelegateMegaLoggerListener(MegaLogger):

    '''Interface to receive SDK logs.
    You can implement this class and pass an object of your subclass to MegaApiPython.set_logger_class()
    to receive SDK logs. You will also have to use MegaApiPython.set_log_level() to select the level of the
    logs you want to receive.
    '''
    def __init__(self, listener):
        self.listener = listener
        super(DelegateMegaLoggerListener, self).__init__()

    def log(self, time, log_level, source, message):
        '''This function will be called with all logs with level smaller or equal to selected level of logging.
        By default logging level is MegaApi.LOG_LEVEL_INFO
        :param time Readable string representing the current time. The SDK retains the ownership of this string,
        it will not be valid after this function returns.
        :param loglevel Log level of this message. Valid values are:
            LOG_LEVEL_FATAL = 0.
            LOG_LEVEL_ERROR = 1
            LOG_LEVEL_WARNING = 2
            LOG_LEVEL_INFO = 3
            LOG_LEVEL_DEBUG = 4
            LOG_LEVEL_MAX = 5
        :param source Location where the log was generated. The SDK retains the ownership of this string,
        it will be valid after this function returns.
        :param message Log message. The SDK retains the ownership of this string, it will be valid after
        this function returns
        '''
        if self.listener is not None:
            self.listener.log(time, log_level, source, message)


class DelegateMegaRequestListener(MegaRequestListener):

    '''Interface to receive information about requests.
    All requests allow to pass a pointer to an implementation of this interface in the last parameter.
    You can also get information about all requests using MegaApiPython.add_request_listener().
    MegaListener objects can also receive information about requests.
    Please note that not all fields of MegaRequest objects are valid for all requests.
    See the documentation about each request to know which fields contain useful information for each one.
    '''
    def __init__(self, mega_api, listener,  single_listener):
        self.mega_api = mega_api
        self.listener = listener
        self.single_listener = single_listener
        super(DelegateMegaRequestListener, self).__init__()

    def get_user_listener(self):
        '''Receive the listener
        :Returns the listener object associated with the delegate
        '''
        return self.listener

    def onRequestStart(self, mega_api, request):
        '''This function is called when a request is about to start being processed.
        The SDK retains the ownership of the request parameter. Do not it use after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the request
        :param request Information about the request.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            self.listener.onRequestStart(self.mega_api, mega_request)



    def onRequestFinish(self, mega_api, request, error):
        '''This function is called when a request has finished.
        There will be no further callbacks related to this request.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the request
        :param request Information about the request
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            mega_error = error.copy()
            self.listener.onRequestFinish(self.mega_api, mega_request, mega_error)
        if single_listener:
            mega_api.free_request_listener()

    def onRequestUpdate(self, mega_api, request):
        '''This function is called to get details about the progress of a request.
        Currently, this callback is only used for fetchNodes requests (MegaRequest.TYPE_FETCH_NODES).
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the request
        :param request Information about the request
        '''
        if self.listener is not None:
            mega_request = request.copy()
            self.listener.onRequestUpdate(self.mega_api, mega_request)



    def onRequestTemporaryError(self, mega_api, request, error):
        '''This function is called when there is a temporary error processing a request.
        The request continues after this callback, so expect more MegaRequestListener.onRequestTemporaryError or
        a MegaRequestListener.onRequestFinish callback.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the request
        :param request Information about the request
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            mega_error = error.copy()
            self.listener.onRequestTemporaryError(self.mega_api, mega_request, mega_error)



class DelegateMegaTransferListener(MegaTransferListener):

    '''Interface to receive information about transfers.
    All transfers are able to pass a pointer to an implementation of this interface in the single_listener parameter.
    You can also get information about all transfers user MegaApiPython.add_transfer_listener().
    MegaListener objects can also receive information about transfers.
    '''
    def __init__(self, mega_api, listener, single_listener):
        self.mega_api = mega_api
        self.listener = listener
        self.single_listener = single_listener
        super(DelegateMegaTransferListener, self).__init__()

    def get_user_listener(self):
        '''Get the listener
        :Returns the listener object associated with the delegate
        '''
        return self.listener


    def onTransferStart(self, mega_api, transfer):
        '''This function is called when a transfer is about to start being processed.
        The SDK retains the ownership of the transfer parameter. Do not it use after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferStart(self.mega_api, mega_transfer)



    def onTransferFinish(self, mega_api, transfer, error):
        '''This function is called when a transfer has finished.
        There will be no further callbacks related to this transfer. The last parameter provides the result of the transfer.
        If the transfer completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the transfer and error parameters. Do not use them after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferFinish(self.mega_api, mega_transfer, mega_error)


    def onTransferUpdate(self, mega_api, transfer):
        '''This function is called to get details about the progress of a transfer.
        The SDK retains the ownership of the transfer parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferUpdate(self.mega_api, mega_transfer)



    def onTransferTemporaryError(self, mega_api, transfer, error):
        '''This function is called when there is a temporary error processing a transfer.
        The transfer continues after this callback, so expect more MegaRequestListener.onTransferTemporaryError or
        a MegaRequestListener.onTransfertFinish callback.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferTemporaryError(self.mega_api, mega_transfer, mega_error)



    def onTransferData(self, mega_api, transfer, buffer):
        '''This function is called to provide the last read bytes of streaming downloads.
        This function will not be called for non streaming downloads. You can get the same buffer provided
        by this function in MegaTransferListener.onTransferUpdate(), using MegaTransfer.getLastBytes() and
        MegaTransfer.getDeltaSize(). The SDK retains the ownership of this transfer and buffer parameters. Do not
        use them after this function returns.
        :param mega_api API object that started the transfer.
        :transfer information about the transfer.
        :buffer buffer with the last read bytes.
        :Returns Size of the buffer.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferData(self.mega_api, mega_transfer, buffer)



class DelegateMegaListener(MegaListener):

    '''Listener to receive and send events to the app
    :Returns the listener object associated with the delegate
    '''

    def __init__(self, mega_api, listener):
        self.mega_api = mega_api
        self.listener = listener
        super(DelegateMegaListener, self).__init__()

    def get_user_listener(self):
        '''Get the listener
        :Returns the listener object associated with the delegate
        '''
        return self.listener

    def onRequestStart(self, mega_api, request):
        '''This function is called when a request is about to start being processed.
        The SDK retains the ownership of the request parameter. Do not it use after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the request
        :param request Information about the request.
        '''
        if self.listener is not None:
            print "Starting request"
            mega_request = request.copy()
            print "requiest copied!" + str(mega_request)
            self.listener.onRequestStart(self.mega_api, mega_request)

    def onRequestFinish(self, mega_api, request, error):
        '''This function is called when a request has finished.
        There will be no further callbacks related to this request.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the request
        :param request Information about the request
        :param error Information about error.
        '''
        if self.listener is not None:
            print "Starting request"
            mega_request = request.copy()
            mega_error = error.copy()
            print "requiest copied!" + str(mega_request)
            print "error is: " + str(mega_error)
            self.listener.onRequestFinish(self.mega_api, mega_request, mega_error)

    def onRequestTemporaryError(self, mega_api, request, error):
        '''This function is called when there is a temporary error processing a request.
        The request continues after this callback, so expect more MegaRequestListener.onRequestTemporaryError or
        a MegaRequestListener.onRequestFinish callback.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the request
        :param request Information about the request
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            mega_error = error.copy()
            self.listener.onRequestTemporaryError(self.mega_api, mega_request, mega_error)



    def onTransferStart(self, mega_api, transfer):
        '''This function is called when a transfer is about to start being processed.
        The SDK retains the ownership of the transfer parameter. Do not it use after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferStart(self.mega_api, mega_transfer)



    def onTransferFinish(self, mega_api, transfer, error):
        '''This function is called when a transfer has finished.
        There will be no further callbacks related to this transfer. The last parameter provides the result of the transfer.
        If the transfer completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the transfer and error parameters. Do not use them after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferFinish(self.mega_api, mega_transfer, mega_error)


    def onTransferUpdate(self, mega_api, transfer):
        '''This function is called to get details about the progress of a transfer.
        The SDK retains the ownership of the transfer parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferUpdate(self.mega_api, mega_transfer)


    def onTransferTemporaryError(self, mega_api, transfer, error):
        '''This function is called when there is a temporary error processing a transfer.
        The transfer continues after this callback, so expect more MegaRequestListener.onTransferTemporaryError or
        a MegaRequestListener.onTransfertFinish callback.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param rtransfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferTemporaryError(self.mega_api, mega_transfer, mega_error)



    def onUsersUpdate(self, mega_api, user_list):
        '''This function is called when there are new or updated contacts in the account.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaUser objects that it contains will be valid until this function returns.
        If you want to save the list, use user_list.copy().
        If you want to save only some of the MegaUser objects, use MegaUser.copy() for those objects.
        :param mega_api API object connected to account.
        :param user_list List that contains the new or updated contacts.
        '''
        if self.listener is not None:
            updated_user_list =  mega_api.user_list_to_array(user_list)
            self.listener.onUsersUpdate(self.mega_api, updated_user_list)



    def onNodesUpdate(self, mega_api, node_list):
        '''This function is called when there are new or updated nodes in the account.
        When the full account is reloaded or a large number of server notifications arrive at once,
        the second parameter will be null.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaNode objects that it contains will be valid until this function returns.
        If you want to save the list, use node_list.copy().
        If you want to save only some of the MegaNode objects, use MegaNode.copy() for those objects.
        :param mega_api API object connected to account.
        :param node_list List that contains the new or updated nodes.
        '''
        if self.listener is not None:
            updated_node_list = mega_api.node_list_to_array(node_list)
            self.listener.onNodesUpdate(self.mega_api, updated_node_list)



    def onReloadNeeded(self, mega_api):
        '''This function is called when an inconsistency is detected in the local cache.
        You should call MegaApiPython.fetch_nodes() when this callback is received.
        :param mega_api API object connected to account.
        '''
        if self.listener is not None:
            self.listener.onReloadNeeded(self.mega_api)



    def onAccountUpdate(self, mega_api):
        if self.listener is not None:
            self.listener.onAccountUpdate(self.mega_api)



    def onContactRequestsUpdate(self, mega_api, contact_request_list):
        '''This function is called when there are new contact requests in the account.
        If you want to save the list, use contact_request_list.copy().
        If you want to save only some of the MegaContactRequest objects, use MegaContactRequest.copy() for those objects.
        :param mega_api API object connected to the account
        :param contact_request_list List that contains new contact requests
        '''
        if self.listener is not None:
            contact_list = mega_api.contact_request_list_to_array(contact_list)
            self.listener.onContactRequestsUpdate(self.mega_api, contact_list)



class DelegateMegaGlobalListener(MegaGlobalListener):
    '''Listener to receive and send global events to the app.
    '''
    def __init__(self, listener, mega_api):
        self.mega_api = mega_api
        self.listener = listener
        super(DelegateMegaGlobalListener, self).__init__()


    def get_user_listener(self):
        '''Get the listener
        :Returns the listener object associated with the delegate
        '''
        return self.listener


    def onUsersUpdate(self, mega_api, user_list):
        '''This function is called when there are new or updated contacts in the account.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaUser objects that it contains will be valid until this function returns.
        If you want to save the list, use user_list.copy().
        If you want to save only some of the MegaUser objects, use MegaUser.copy() for those objects.
        :param mega_api API object connected to account.
        :param user_list List that contains the new or updated contacts.
        '''
        if self.listener is not None:
            updated_user_list =  mega_api.user_list_to_array(user_list)
            self.listener.onUsersUpdate(self.mega_api, updated_user_list)



    def onNodesUpdate(self, mega_api, node_list):
        '''This function is called when there are new or updated nodes in the account.
        When the full account is reloaded or a large number of server notifications arrive at once,
        the second parameter will be null.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaNode objects that it contains will be valid until this function returns.
        If you want to save the list, use node_list.copy().
        If you want to save only some of the MegaNode objects, use MegaNode.copy() for those objects.
        :param mega_api API object connected to account.
        :param node_list List that contains the new or updated nodes.
        '''
        if self.listener is not None:
            updated_node_list = mega_api.node_list_to_array(node_list)
            self.listener.onNodesUpdate(self.mega_api, updated_node_list)


    def onReloadNeeded(self, mega_api):
        '''This function is called when an inconsistency is detected in the local cache.
        You should call MegaApiPython.fetch_nodes() when this callback is received.
        :param mega_api API object connected to account.
        '''
        if self.listener is not None:
            self.istener.onReloadNeeded(self.mega_api)


    def onAccountUpdate(self, mega_api):
        if self.listener is not None:
            self.listener.onAccountUpdate(self.mega_api)


    def onContactRequestsUpdate(self, mega_api, contact_request_list):
        '''This function is called when there are new contact requests in the account.
        If you want to save the list, use contact_request_list.copy().
        If you want to save only some of the MegaContactRequest objects, use MegaContactRequest.copy() for those objects.
        :param mega_api API object connected to the account
        :param contact_request_list List that contains new contact requests
        '''
        if self.listener is not None:
            contact_list = mega_api.contact_request_list_to_array(contact_list)
            self.listener.onContactRequestsUpdate(self.mega_api, contact_list)


# Mirroring, WILL BE MOVED TO MegaApiPython class later
MegaApi.get_current_request = MegaApi.getCurrentRequest
MegaApi.get_current_transfer = MegaApi.getCurrentTransfer
MegaApi.get_current_error = MegaApi.getCurrentError
MegaApi.get_current_nodes = MegaApi.getCurrentNodes
MegaApi.get_current_users = MegaApi.getCurrentUsers
MegaApi.get_base64_pw_key = MegaApi.getBase64PwKey
MegaApi.get_string_hash = MegaApi.getStringHash
MegaApi.get_session_transfer_URL = MegaApi.getSessionTransferURL
MegaApi.retry_pending_connections = MegaApi.retryPendingConnections
MegaApi.login_to_folder = MegaApi.loginToFolder
MegaApi.fast_login = MegaApi.fastLogin
MegaApi.kill_session = MegaApi.killSession
MegaApi.get_user_data = MegaApi.getUserData
MegaApi.dump_session = MegaApi.dumpSession
MegaApi.dump_XMPP_session = MegaApi.dumpXMPPSession
MegaApi.create_account = MegaApi.createAccount
MegaApi.fast_create_account = MegaApi.fastCreateAccount
MegaApi.query_signup_link = MegaApi.querySignupLink
MegaApi.confirm_account = MegaApi.confirmAccount
MegaApi.fast_confirm_account = MegaApi.fastConfirmAccount
MegaApi.set_proxy_settings = MegaApi.setProxySettings
MegaApi.get_auto_proxy_settings = MegaApi.getAutoProxySettings
MegaApi.is_logged_in = MegaApi.isLoggedIn
MegaApi.get_my_email = MegaApi.getMyEmail
MegaApi.get_my_user_handle = MegaApi.getMyUserHandle
MegaApi.create_folder = MegaApi.createFolder
MegaApi.move_node = MegaApi.moveNode
MegaApi.copy_node = MegaApi.copyNode
MegaApi.rename_node = MegaApi.renameNode
MegaApi.send_file_to_user = MegaApi.sendFileToUser
MegaApi.import_file_link = MegaApi.importFileLink
MegaApi.get_public_node = MegaApi.getPublicNode
MegaApi.get_thumbnail = MegaApi.getThumbnail
MegaApi.get_preview = MegaApi.getPreview
MegaApi.get_user_avatar = MegaApi.getUserAvatar
MegaApi.get_user_attribute = MegaApi.getUserAttribute
MegaApi.cancel_get_thumbnail = MegaApi.cancelGetThumbnail
MegaApi.cancel_get_preview = MegaApi.cancelGetPreview
MegaApi.set_thumbnail = MegaApi.setThumbnail
MegaApi.set_preview = MegaApi.setPreview
MegaApi.set_avatar = MegaApi.setAvatar
MegaApi.set_user_attribute = MegaApi.setUserAttribute
MegaApi.export_node = MegaApi.exportNode
MegaApi.disable_export = MegaApi.disableExport
MegaApi.fetch_nodes = MegaApi.fetchNodes
MegaApi.get_account_details = MegaApi.getAccountDetails
MegaApi.get_extended_account_details = MegaApi.getExtendedAccountDetails
MegaApi.get_pricing = MegaApi.getPricing
MegaApi.get_payment_id = MegaApi.getPaymentId
MegaApi.upgrade_account = MegaApi.upgradeAccount
MegaApi.submit_purchase_receipt = MegaApi.submitPurchaseReceipt
MegaApi.credit_card_store = MegaApi.creditCardStore
MegaApi.credit_card_query_subscriptions = MegaApi.creditCardQuerySubscriptions
MegaApi.credit_card_cancel_subscriptions = MegaApi.creditCardCancelSubscriptions
MegaApi.get_payment_methods = MegaApi.getPaymentMethods
MegaApi.export_master_key = MegaApi.exportMasterKey
MegaApi.change_password = MegaApi.changePassword
MegaApi.add_contact = MegaApi.addContact
MegaApi.invite_contact = MegaApi.inviteContact
MegaApi.reply_contact_request = MegaApi.replyContactRequest
MegaApi.remove_contact = MegaApi.removeContact
MegaApi.local_logout = MegaApi.localLogout
MegaApi.submit_feedback = MegaApi.submitFeedback
MegaApi.report_debug_event = MegaApi.reportDebugEvent
MegaApi.start_upload = MegaApi.startUpload
MegaApi.start_download = MegaApi.startDownload
MegaApi.start_streaming = MegaApi.startStreaming
MegaApi.cancel_transfer = MegaApi.cancelTransfer
MegaApi.cancel_transfer_by_tag = MegaApi.cancelTransferByTag
MegaApi.cancel_transfers = MegaApi.cancelTransfers
MegaApi.pause_transfers = MegaApi.pauseTransfers
MegaApi.are_transfers_paused = MegaApi.areTransfersPaused
MegaApi.set_upload_limit = MegaApi.setUploadLimit
MegaApi.set_download_method = MegaApi.setDownloadMethod
MegaApi.set_upload_method = MegaApi.setUploadMethod
MegaApi.get_download_method = MegaApi.getDownloadMethod
MegaApi.get_upload_method = MegaApi.getUploadMethod
MegaApi.get_transfer_by_tag = MegaApi.getTransferByTag
MegaApi.is_waiting = MegaApi.isWaiting
MegaApi.get_num_pending_uploads = MegaApi.getNumPendingUploads
MegaApi.get_num_pending_downloads = MegaApi.getNumPendingDownloads
MegaApi.get_total_uploads = MegaApi.getTotalUploads
MegaApi.get_total_downloads = MegaApi.getTotalDownloads
MegaApi.reset_total_downloads = MegaApi.resetTotalDownloads
MegaApi.reset_total_uploads = MegaApi.resetTotalUploads
MegaApi.get_total_downloaded_bytes = MegaApi.getTotalDownloadedBytes
MegaApi.get_total_uploaded_bytes = MegaApi.getTotalUploadedBytes
MegaApi.update_stats = MegaApi. updateStats
MegaApi.get_num_children = MegaApi.getNumChildren
MegaApi.get_num_child_files = MegaApi.getNumChildFiles
MegaApi.get_num_child_folders = MegaApi.getNumChildFolders
MegaApi.get_index = MegaApi.getIndex
MegaApi.get_child_node = MegaApi.getChildNode
MegaApi.get_parent_node = MegaApi.getParentNode
MegaApi.get_node_path = MegaApi.getNodePath
MegaApi.get_node_by_path = MegaApi.getNodeByPath
MegaApi.get_node_by_handle = MegaApi.getNodeByHandle
MegaApi.get_contact_request_by_handle = MegaApi.getContactRequestByHandle
MegaApi.get_contact = MegaApi.getContact
MegaApi.is_shared = MegaApi.isShared
MegaApi.get_access = MegaApi.getAccess
MegaApi.get_size = MegaApi.getSize
MegaApi.get_fingerprint = MegaApi.getFingerprint
MegaApi.get_node_by_fingerprint = MegaApi.getNodeByFingerprint
MegaApi.has_fingerprint = MegaApi.hasFingerprint
MegaApi.get_CRC = MegaApi.getCRC
MegaApi.get_node_by_CRC = MegaApi.getNodeByCRC
MegaApi.check_access = MegaApi.checkAccess
MegaApi.check_move = MegaApi.checkMove
MegaApi.get_root_node = MegaApi.getRootNode
MegaApi.get_inbox_node = MegaApi.getInboxNode
MegaApi.get_rubbish_node = MegaApi.getRubbishNode
MegaApi.process_mega_tree = MegaApi.processMegaTree
MegaApi.create_public_file_node = MegaApi.createPublicFileNode
MegaApi.create_public_folder_node = MegaApi.createPublicFolderNode
MegaApi.get_version = MegaApi.getVersion
MegaApi.get_user_agent = MegaApi.getUserAgent
MegaApi.change_api_url = MegaApi.changeApiUrl
MegaApi.escape_fs_incompatible = MegaApi.escapeFsIncompatible
MegaApi.unescape_fs_incompatible = MegaApi.unescapeFsIncompatible
MegaApi.create_thumbnail = MegaApi.createThumbnail
MegaApi.create_preview = MegaApi.createPreview
MegaApi.load_balancing = MegaApi.loadBalancing

del MegaApi.getCurrentRequest
del MegaApi.getCurrentTransfer
del MegaApi.getCurrentError
del MegaApi.getCurrentNodes
del MegaApi.getCurrentUsers
del MegaApi.getBase64PwKey
del MegaApi.getStringHash
del MegaApi.getSessionTransferURL
del MegaApi.retryPendingConnections
del MegaApi.loginToFolder
del MegaApi.fastLogin
del MegaApi.killSession
del MegaApi.getUserData
del MegaApi.dumpSession
del MegaApi.dumpXMPPSession
del MegaApi.getAccountDetails
del MegaApi.createAccount
del MegaApi.getMyEmail
del MegaApi.fastCreateAccount
del MegaApi.querySignupLink
del MegaApi.confirmAccount
del MegaApi.fastConfirmAccount
del MegaApi.setProxySettings
del MegaApi.getAutoProxySettings
del MegaApi.isLoggedIn
del MegaApi.getMyUserHandle
del MegaApi.createFolder
del MegaApi.moveNode
del MegaApi.copyNode
del MegaApi.renameNode
del MegaApi.sendFileToUser
del MegaApi.importFileLink
del MegaApi.getPublicNode
del MegaApi.getThumbnail
del MegaApi.getPreview
del MegaApi.getUserAvatar
del MegaApi.getUserAttribute
del MegaApi.cancelGetThumbnail
del MegaApi.cancelGetPreview
del MegaApi.setThumbnail
del MegaApi.setPreview
del MegaApi.setAvatar
del MegaApi.setUserAttribute
del MegaApi.exportNode
del MegaApi.disableExport
del MegaApi.fetchNodes
del MegaApi.getExtendedAccountDetails
del MegaApi.getPricing
del MegaApi.getPaymentId
del MegaApi.upgradeAccount
del MegaApi.submitPurchaseReceipt
del MegaApi.creditCardStore
del MegaApi.creditCardQuerySubscriptions
del MegaApi.creditCardCancelSubscriptions
del MegaApi.getPaymentMethods
del MegaApi.exportMasterKey
del MegaApi.changePassword
del MegaApi.addContact
del MegaApi.inviteContact
del MegaApi.replyContactRequest
del MegaApi.removeContact
del MegaApi.localLogout
del MegaApi.submitFeedback
del MegaApi.reportDebugEvent
del MegaApi.startUpload
del MegaApi.startDownload
del MegaApi.startStreaming
del MegaApi.cancelTransfer
del MegaApi.cancelTransferByTag
del MegaApi.cancelTransfers
del MegaApi.pauseTransfers
del MegaApi.areTransfersPaused
del MegaApi.setUploadLimit
del MegaApi.setDownloadMethod
del MegaApi.setUploadMethod
del MegaApi.getDownloadMethod
del MegaApi.getUploadMethod
del MegaApi.getTransferByTag
del MegaApi.isWaiting
del MegaApi.getNumPendingUploads
del MegaApi.getNumPendingDownloads
del MegaApi.getTotalUploads
del MegaApi.getTotalDownloads
del MegaApi.resetTotalDownloads
del MegaApi.resetTotalUploads
del MegaApi.getTotalDownloadedBytes
del MegaApi.getTotalUploadedBytes
del MegaApi. updateStats
del MegaApi.getNumChildren
del MegaApi.getNumChildFiles
del MegaApi.getNumChildFolders
del MegaApi.getIndex
del MegaApi.getChildNode
del MegaApi.getParentNode
del MegaApi.getNodePath
del MegaApi.getNodeByPath
del MegaApi.getNodeByHandle
del MegaApi.getContactRequestByHandle
del MegaApi.getContact
del MegaApi.isShared
del MegaApi.getAccess
del MegaApi.getSize
del MegaApi.getFingerprint
del MegaApi.getNodeByFingerprint
del MegaApi.hasFingerprint
del MegaApi.getCRC
del MegaApi.getNodeByCRC
del MegaApi.checkAccess
del MegaApi.checkMove
del MegaApi.getRootNode
del MegaApi.getInboxNode
del MegaApi.getRubbishNode
del MegaApi.processMegaTree
del MegaApi.createPublicFileNode
del MegaApi.createPublicFolderNode
del MegaApi.getVersion
del MegaApi.getUserAgent
del MegaApi.changeApiUrl
del MegaApi.escapeFsIncompatible
del MegaApi.unescapeFsIncompatible
del MegaApi.createThumbnail
del MegaApi.createPreview
del MegaApi.loadBalancing
