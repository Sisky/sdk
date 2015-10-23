from mega import *
import threading

class MegaApiPython(object):

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
    After using MegaApiPython.logout_from_account() you can reuse the same MegaApi object to log in to another MEGA
    account or a public folder.
    '''



    def __init__(self, app_key, processor, base_path, user_agent):
        self.api = MegaApi(app_key, processor, base_path, user_agent)
        self.logger = None
        self.active_mega_listeners = []
        self.active_global_mega_listeners = []
        self.active_request_listeners = []
        self.active_transfer_listeners = []
        self.lock = threading.Lock()

    ### API METHODS ###

    # Listener management

    def add_mega_listener(self, listener):
        '''Register a listener to receive all events (requests, transfers, global, synchronization).
        You can use MegaApiPython.remove_listener() to stop receiving events.
        :param listener Listener that will receive all events (requests, transfers, global, synchronization).
        '''
        self.api.addListener(self.create_delegate_mega_listener(listener))

    def add_global_listener(self, listener):
        '''Register a listener to receive global events.
        You can use MegaApiPython.remove_global_listener() to stop receiving events.
        :param listener Listener that will receive global events.
        '''
        self.api.addGlobalListener(self.create_delegate_mega_global_listener(listener))

    def add_request_listener(self, listener):
        '''Register a listener to receive all events about requests.
        You can use MegaApiPython.remove_request_listener() to stop receiving events.
        :param listener Listener that will receive all events about requests.
        '''
        self.api.addRequestListener(self.create_delegate_request_listener(listener, False))

    def add_transfer_listener(self, listener):
        '''Register a listener to receive all events about transfers.
        You can use MegaApiPython.remove_transfer_listener() to stop receiving events.
        :param listener Listener that will receive all events about transfers.
        '''
        self.api.addTransferListener(self.create_delegate_transfer_listener(listener, False))

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

    def get_base64_pw_key(self, password):
    	'''Generates a private key based on the access password. This is a time consuming operation
        (specially for low-end mobile devices).  Since the resulting key is required to log in, this function
         allows to do this step in a separate function. You should run this function in a background thread, to prevent UI hangs.
         The resulting key can be used in MegaApi.fastLogin.
         You take the ownership of the returned value.
        :param password - Access password
        :Returns - Base64-encoded private key
        :Deprecated
        '''
        return self.api.getBase64PwKey(password)

    def base32_to_handle(self, base32_handle):
        '''Converts a Base32 - encoded user handle to a MegaHandle.
        :param base32_handle Base32-encoded handle
        :Returns Base64-encoded hash.
        :Deprecated
        '''
        return self.api.base32ToHandle(base32_handle)

    def base64_to_handle(self, base64_handle):
        '''Converts a Base64-encoded node handle to a MegaHandle.
        The returned value can be used to recover a MegaNode using
        MegaApi.get_node_by_handle()
        You can revert this operation using MegaApi.handle_to_base64()
        :param base64_handle Base64-encoded node handle.
        :Returns Node handle.
        '''
        return self.api.base64ToHandle(base64_handle)

    def handle_to_base64(self, handle):
        '''Converts a MegaHandle to a Base64-encoded string.
        You can revert this operation using MegaApi.base64_to_handle().
        :param handle handle to be converted
        :Returns Base64-encoded node handle.
        '''
        return self.api.handleToBase64(handle)

    def user_handle_to_base64(self, handle):
        '''Converts a MegaHandle to a Base64-encoded string.
        You take the ownership of the returned value.
        You can revert this operation using MegaApi.base64_to_handle()
        :param handle handle to be converted
        :Returns Base64-encoded user handle.
        '''
        return self.api.userHandleToBase64(handle)

    def add_entropy(self, data, size):
        '''Add entropy to internal random number generators.
        It is recommended to call this function with random data to
        enhance security.
        :param data Byte array with random data.
        :param size Size of the byte array (in bytes)
        '''
        self.api.addEntropy(data, size)

    def get_string_hash(self,base_64_pwkey, email):
    	'''Generates a hash based in the provided private key and email.
        This is a time consuming operation (specially for low-end mobile devices).
        Since the resulting key is required to log in, this function allows to do this step in a separate function.
        You should run this function in a background thread, to prevent UI hangs.
        The resulting key can be used in MegaApi.fastLogin
        You take the ownership of the returned value.
        :param base_64_pwkey- Private key returned by MegaApi.get_base64_pw_key()
        :param email - Email to create the hash
        :Returns - Base64-encoded hash
        :Deprecated
        '''
        return self.api.getStringHash(base_64_pwkey, email)

    def reconnect_to_account(self):
        '''Reconnect and retry all transfers
        '''
        self.api.retryPendingConnections(True, True)

    def retry_pending_connections(self):
    	'''Retry all pending requests.
		When requests fails they wait some time before being retried. That delay grows exponentially if the request fails again.
        For this reason, and since this request is very lightweight, it's recommended to call it with the default parameters on every
        user interaction with the application. This will prevent very big delays completing requests.
       	'''
        self.api.retryPendingConnections()

    #REQUESTS

    def login_email(self, email, password):
    	'''Log in to a MEGA account.
        :param email -Email of the user
        :param password - Password
        '''
        self.api.login(email, password)

    def login_email_with_listener(self, email, password, listener):
    	'''Log in to a MEGA account.
		The associated request type with this request is MegaRequest.TYPE_LOGIN. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest.getEmail - Returns the first parameter
    		MegaRequest.getPassword - Returns the second parameter
		If the email/password aren't valid the error code provided in onRequestFinish is MegaError.API_ENOENT.
        :param email -Email of the user
        :param password - Password
        :param listener - MegaRequestListener to track this request
        '''
        self.api.login(email, password, self.create_delegate_request_listener(listener, True))

    def login_to_folder(self, mega_folder_link):
    	'''Log in to a public folder using a folder link.
		After a successful login, you should call MegaApi.fetch_nodes() to get filesystem and start working with the folder.
		:param megaFolderLink - Public link to a folder in MEGA
        '''
        self.api.loginToFolder(mega_folder_link)

    def login_to_folder_with_listener(self, mega_folder_link, listener):
    	'''Log in to a public folder using a folder link.
		After a successful login, you should call MegaApi.fetch_nodes() to get filesystem and start working with the folder.
		The associated request type with this request is MegaRequest.TYPE_LOGIN. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest.getEmail - Retuns the string "FOLDER"
    		MegaRequest.getLink - Returns the public link to the folder
		:param megaFolderLink - Public link to a folder in MEGA
        :param listener - MegaRequestListener to track this request
        '''
        self.api.loginToFolder(mega_folder_link, self.create_delegate_request_listener(listener, True))

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
        self.api.fastLogin(email, string_hash, base_64_pwkey, self.create_delegate_request_listener(listener, True))

    def fast_login(self, email, string_hash, base_64_pwkey):
    	'''Login to a MEGA account with precomputed keys.
    	:param email - Email for the account
        :param string_hash -hash of the email returned by MegaApi.get_string_hash()
    	:param base_64_pwkey	- Private key calculated with MegaApi.get_base64_pw_key()
        '''
        self.api.fastLogin(email, string_hash, base_64_pwkey)

    def fast_login_with_session(self, session):
    	'''Login to a MEGA account with a session key.
    	:param session - Session key previously dumped with api.dump_session()
        '''
        self.api.fastLogin(session)

    def fast_login_with_session_listener(session, listener):
    	'''Login to a MEGA account with a session key.
    	:param session - Session key previously dumped with api.dump_session()
        param listener - MegaRequestListener to track this request
        '''
        self.api.fastLogin(session, self.create_delegate_request_listener(listener, True))

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
        self.api.killSession(session_handle, self.create_delegate_request_listener(listener, True))

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
        self.api.killSession(session_handle)

    def get_user_data_listener(self, listener):
    	'''Get data about the logged account.
        The associated request type with this request is MegaRequest.TYPE_GET_USER_DATA.
        Valid data in the MegaRequest object received in onRequestFinish() when the error code is MegaError.API_OK:
            MegaRequest.getName() - Returns the name of the logged user
            MegaRequest.getPassword() - Returns the the public RSA key of the account, Base64-encoded
            MegaRequest.getPrivateKey() - Returns the private RSA key of the account, Base64-encoded
        param:listener MegaRequestListener to track this request
        '''
        self.api.getUserData(self.create_delegate_request_listener(listener, True))

    def get_user_data(self):
        '''Get data about the logged account.
        '''
        self.api.getUserData()

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
        self.api.getUserData(user, self.create_delegate_request_listener(listener, True))

    def get_user_data_with_mega_user(self, user):
        '''Get data about a contact.
        :param user MegaUser contact to get the data
        '''
        self.api.getUserData(user)

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
        self.api.getUserData(user, self.create_delegate_request_listener(listener, True))

    def get_user_data_with_user(self, user):
        '''Get data about a contact.
        :param user Email or Base64 handle of the contact
        '''
        self.api.getUserData(user)

    def dump_session(self):
    	'''Returns the current session key.
        You have to be logged in to get a valid session key. Otherwise, this function returns NULL.
        You take the ownership of the returned value.
        :Returns current session key
        '''
        return self.api.dumpSession()

    def dump_XMPP_session(self):
    	'''Returns the current XMPP session key.
        You have to be logged in to get a valid session key. Otherwise, this function returns NULL.
        You take the ownership of the returned value.
        :Returns current XMPP session key
        '''
        return self.api.dumpXMPPSession()

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
        self.api.createAccount(email, password, name, self.create_delegate_request_listener(listener, True))

    def create_account(self, email, password, name):
        '''Initialize a creation of the new MEGA account.
        :param email - Email for the account
        :param password - Password for the account
        :param name - Name of the user
        '''
        self.api.createAccount(email, password, name)

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
        self.api.fastCreateAccount(email, base_64_pwkey, name, self.create_delegate_request_listener(listener, True))

    def fast_create_account(self, email, base_64_pwkey, name):
        '''Initialize the creation of a new MEGA account with precomputed keys.
        :param email - Email for the account
        :param base_64_pwkey - Private key calculated with MegaApi.get_base64_pw_key()
        :param name - Name of the user
        '''
        self.api.fastCreateAccount(email, base_64_pwkey, name)

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
        self.api.querySignupLink(link, self.create_delegate_request_listener(listener, True))

    def query_signup_link(self, link):
        '''Get information about a confirmation link.
        :param link Confirmation link
        '''
        self.api.querySignupLink(link)

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
        self.api.confirmAccount(link, password, self.create_delegate_request_listener(listener, True))

    def confirm_account(self, link, password):
        '''Confirm a MEGA account using a confirmation link and the user password.
        :param link - Confirmation link
        :param password - Password of the account
        '''
        self.api.confirmAccount(link, password)

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
        self.api.fastConfirmAccount(link, base_64_pwkey, self.create_delegate_request_listener(listener, True))

    def fast_confirm_account(self, link, base_64_pwkey):
        '''Confirm a MEGA account using a confirmation key and a precomputed key.
        :param link - Confirmation link
        :param base_64_pwkey - Private key precomputed with MegaApi.get_base64_pw_key()
        '''
        self.api.fastConfirmAccount(link, base_64_pwkey)

    def set_proxy_settings(self, proxy_settings):
    	'''Set proxy settings.
        The SDK will start using the provided proxy settings as soon as this function returns.
        :param proxy_settings - Proxy settings
        '''
        self.api.setProxySettings(proxy_settings)

    def get_auto_proxy_settings(self):
    	'''Try to detect the system's proxy settings.
        Automatic proxy detection is currently supported on Windows only. On other platforms, this fuction will return a MegaProxy object of type MegaProxy.PROXY_NONE
        You take the ownership of the returned value.
        :param Returns MegaProxy object with the detected proxy settings.
        '''
        return self.api.getAutoProxySettings()

    def is_logged_in(self):
    	'''Check if the MegaApi object is logged in.
        :Returns 0 if not logged in, else a number >= 0
        '''
        return self.api.isLoggedIn()

    def get_my_email(self):
    	'''Returns the email of the currently open account.
        If the MegaApi object isn't logged in or the email isn't available, this function returns None
        You take the ownership of the returned value
        :Returns Email of the account
        '''
        return self.api.getMyEmail()

    def get_my_user_handle(self):
    	'''need clarification'''
        return self.api.getMyUserHandle()

    def set_logger_object(self, mega_logger):
        '''Set a MegaLogger implementation to receive SDK logs.
        Logs received by this objects depends on the active log level.
        By default it is MegaApi.LOG_LEVEL_INFO.You can changed it using
        MegaApi.setLogLevel()
        :param mega_logger MegaLogger implementation
        '''
        new_logger = DelegateMegaLoggerListener(mega_logger)
        self.api.setLoggerObject(new_logger)
        self.logger = new_logger

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
        self.api.setLogLevel(log_level)

    def do_log(self, log_level, message, filename, line):
        '''Send a log to the logging system.
        This log will be received by the active logger object, the one in
        MegaApi.set_logger_object() if the log is the same or lower than the
        actual active log level in MegaApi.set_log_level().
        :param log_level Log level for this message
        :param message Message for the logging system
        :param filename Origin of the log message
        :param line Line of code where this message was generated
        '''
        self.api.log(log_level, message, filename, line)

    def do_log_no_line(self, log_level, message, filename):
        '''Send a log to the logging system.
        This log will be received by the active logger object, the one in
        MegaApi.set_logger_object() if the log is the same or lower than the
        actual active log level in MegaApi.set_log_level().
        :param log_level Log level for this message
        :param message Message for the logging system
        :param filename Origin of the log message
        '''
        self.api.log(log_level, message, filename)

    def do_log_no_line_filename(self, log_level, message):
        '''Send a log to the logging system.
        This log will be received by the active logger object, the one in
        MegaApi.set_logger_object() if the log is the same or lower than the
        actual active log level in MegaApi.set_log_level().
        :param log_level Log level for this message
        :param message Message for the logging system
        '''
        self.api.log(log_level, message)

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
        self.api.createFolder(name, parent, self.create_delegate_request_listener(listener, True))

    def create_folder(self, name, parent):
        '''Create a folder in the MEGA account.
        :param name - Name of the new folder
        :param parent - Parent folder
        '''
        self.api.createFolder(name, parent)

    def move_node_listener(self, node, new_parent, listener):
    	'''Move a node in the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_MOVE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to move
            MegaRequest.getParentHandle - Returns the handle of the new parent for the node
        :param node - Node to move
        :param new_parent - New parent for the node
        :param listener - MegaRequestListener to track this request
        '''
        self.api.moveNode(node, new_parent, self.create_delegate_request_listener(listener, True))

    def move_node(self, node, new_parent):
        '''Move a node in the MEGA account.
        :param node - Node to move
        :param new_parent - New parent for the node
        '''
        self.api.moveNode(node, new_parent)

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
        self.api.copyNode(node, new_parent, self.create_delegate_request_listener(listener, True))

    def copy_node(self, node, new_parent):
        '''Copy a node in the MEGA account.
        :param node - Node to copy
        :param new_parent - Parent for the new node
        '''
        self.api.copyNode(node, new_parent)

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
        self.api.copyNode(node, new_parent, new_name, self.create_delegate_request_listener(listener, True))

    def copy_node_new_name(self, new_parent, new_name):
        '''Copy a node in the MEGA account
        :param node - Node to copy
        :param new_parent - Parent for the new node
        :param new_name - Name for the new node
        '''
        self.api.copyNode(node, new_parent, new_name)

    def rename_node_listener(self, node, new_name, listener):
    	'''Rename a node in the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_RENAME Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to rename
            MegaRequest.getName - Returns the new name for the node
        :param node - Node to modify
        :param new_name - New name for the node
        :param listener - MegaRequestListener to track this request
        '''
        self.api.renameNode(node, new_name, self.create_delegate_request_listener(listener, True))

    def rename_node(self, node, new_name):
        '''Rename a node in the MEGA accoutn.
        :param node - Node to modify
        :param new_name - New name for the node
        '''
        self.api.renameNode(node, new_name)

    def remove_with_listener(self, node, listener):
    	'''Remove a node from the MEGA account.
        This function doesn't move the node to the Rubbish Bin, it fully removes the node. To move the node to the Rubbish Bin use MegaApi.moveNode
        The associated request type with this request is MegaRequest.TYPE_REMOVE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to remove
        :param node - Node to remove
        :param listener - MegaRequestListener to track this request
        '''
        self.api.remove(node, self.create_delegate_request_listener(listener, True))

    def remove_node(self, node):
        '''Remove a node from the MEGA account.
        :param node - Node to remove
        '''
        self.api.remove(node)

    def send_file_to_user_listener(self, node, user, listener):
    	'''Send a node to the Inbox of another MEGA user using a MegaUser.
        The associated request type with this request is MegaRequest.TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node to send
            MegaRequest.getEmail - Returns the email of the user that receives the node
        :param node - Node to send
        :param user - User that receives the node
        :param listener - MegaRequestListener to track this request
        '''
        self.api.sendFileToUser(node, user, self.create_delegate_request_listener(listener, True))

    def send_file_to_user(self, node, user):
        '''Send a node to the inbox of another MEGA user using a Megauser.
        :param node - Node to send
        :param user - User that receives the node
        '''
        self.api.sendFileToUser(node, user)

    def share_folder_with_listener(self, node, user, level, listener):
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
        self.api.share(node, user, level, self.create_delegate_request_listener(listener, True))

    def share_folder(self, node, user, level):
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
        self.api.share(node, user, level)

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
        self.api.share(node, email, level, self.create_delegate_request_listener(listener, True))

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
        self.api.share(node, email, level)

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
        self.api.importFileLink(mega_file_link, parent, self.create_delegate_request_listener(listener, True))

    def import_file_link(self, mega_file_link, parent):
        '''Import a public link to the account.
        :param mega_file_link - Public link to a file in MEGA
        :param parent - Parent folder for the imported file
        '''
        self.api.importFileLink(mega_file_link, parent)

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
        self.api.getPublicNode(mega_file_link, self.create_delegate_request_listener(listener, True))

    def get_public_node(self, mega_file_link):
        '''Get a MegaNode from a public link to a file.
        A public node can be imported using MegaApi.copy_node() or downloaded using MegaApi.start_download()
        :param mega_file_link - Public link to a file in MEGA
        '''
        self.api.getPublicNode(mega_file_link)

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
        self.api.getThumbnail(node, dst_file_path, self.create_delegate_request_listener(listener, True))

    def get_thumbnail(self, node, dst_file_path):
        '''Get the thumbnail of a node.
        If the node doesn't have a thumbnail the request fails with the MegaError.API_ENOENT error code
        :param node - Node to get the thumbnail
        :param dst_file_path - Destination path for the thumbnail. If this path is a local folder,
        it must end with a '\' or '/' character and (Base64-encoded handle + "0.jpg") will be used as the file name inside that folder.
        If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        '''
        self.api.getThumbnail(node, dst_file_path)

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
        self.api.getPreview(node, dst_file_path, self.create_delegate_request_listener(listener, True))

    def get_preview(self, node, dst_file_path):
    	'''Get the preview of a node.
        If the node doesn't have a preview the request fails with the MegaError.API_ENOENT error code
        :param node - Node to get the preview
        :param dst_file_path - Destination path for the preview. If this path is a local folder,
        it must end with a '\' or '/' character and (Base64-encoded handle + "1.jpg") will be used
        as the file name inside that folder. If the path doesn't finish with one of these
        characters, the file will be downloaded to a file in that path.
        '''
        self.api.getPreview(node, dst_file_path)

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
        self.api.getUserAvatar(user, dst_file_path, self.create_delegate_request_listener(listener, True))

    def get_user_avatar(self, user, dst_file_path):
        '''Get the avatar of a MegaUser.
        :param user - MegaUser to get the avatar
        :param dst_file_path - Destination path for the avatar. It has to be a path to a file, not to a folder.
        If this path is a local folder, it must end with a '\' or '/' character and (email + "0.jpg") will be
        used as the file name inside that folder. If the path doesn't finish with one of these characters,
        the file will be downloaded to a file in that path.
        '''
        self.api.getUserAvatar(user, dst_file_path)

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
        self.api.getUserAttribute(user, type, self.create_delegate_request_listener(listener, True))

    def get_user_attribute(self, user, type):
        '''Get an attribute of a MegaUser.
        :param user MegaUser to get the attribute
        :param type Attribute type. Valid values are:
            MegaApi.USER_ATTR_FIRSTNAME = 1 Get the firstname of the user
            MegaApi.USER_ATTR_LASTNAME = 2 Get the lastname of the user
        '''
        self.api.getUserAttribute(user, type)

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
        self.api.getUserAttribute(type, self.create_delegate_request_listener(listener, True))

    def get_user_attribute_by_type(self, type):
        '''Get an attribute of the current account.
        :param type Attribute type. Valid values are:
            MegaApi.USER_ATTR_FIRSTNAME = 1 Get the firstname of the user.
            MegaApi.USER_ATTR_LASTNAME = 2 Get the lastname of the user
        '''
        self.api.getUserAttribute(type)

    def cancel_get_thumbnail_with_listener(self, node, listener):
    	'''Cancel the retrieval of a thumbnail.
        The associated request type with this request is MegaRequest.TYPE_CANCEL_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_THUMBNAIL
        :param node - Node to cancel the retrieval of the preview
        :param listener - listener	MegaRequestListener to track this request
        '''
        self.api.cancelGetThumbnail(node, self.create_delegate_request_listener(listener, True))

    def cancel_get_thumbnail(self, node):
    	'''Cancel the retrieval of a thumbnail.
        :param node - Node to cancel the retrieval of the preview
        '''
        self.api.cancelGetThumbnail(node)

    def cancel_get_preview_with_listener(self, node, listener):
    	'''Cancel the retrieval of a preview.
        The associated request type with this request is MegaRequest.TYPE_CANCEL_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getParamType - Returns MegaApi.ATTR_TYPE_PREVIEW
        :param node - Node to cancel the retrieval of the preview
        :param listener - listener	MegaRequestListener to track this request
        '''
        self.api.cancelGetPreview(node, self.create_delegate_request_listener(listener, True))

    def cancel_get_preview(self, node):
    	'''Cancel the retrieval of a preview.
        :param node - Node to cancel the retrieval of the preview
        '''
        self.api.cancelGetPreview(node)

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
        self.api.setThumbnail(node, src_file_path, self.create_delegate_request_listener(listener, True))

    def set_thumbnail(self, node, src_file_path):
    	'''Set the thumbnail of a MegaNode.
        :param node - MegaNode to set the thumbnail
        :param src_file_path - Source path of the file that will be set as thumbnail
        '''
        self.api.setThumbnail(node, src_file_path)

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
        self.api.setPreview(node, src_file_path, self.create_delegate_mega_listener(listener))

    def set_preview(self, node, src_file_path):
    	'''Set the preview of a MegaNode.
        :param node - MegaNode to set the preview
        :param src_file_path - Source path of the file that will be set as preview
        '''
        self.api.setPreview(node, src_file_path)

    def set_avatar_with_listener(self, src_file_path, listener):
    	'''Set the avatar of the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_SET_ATTR_USER Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getFile - Returns the source path
        :param src_file_path - Source path of the file that will be set as avatar
        :param listener - MegaRequestListener to track this request
        '''
        self.api.setAvatar(src_file_path, self.create_delegate_request_listener(listener, True))

    def set_avatar(self, src_file_path):
    	'''Set the avatar of the MEGA account.
        :param src_file_path - Source path of the file that will be set as avatar
        '''
        self.api.setAvatar(src_file_path)

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
        self.api.setUserAttribute(type, value, self.create_delegate_request_listener(listener, True))

    def set_user_attribute(self, type, value):
        '''Set an attribute of the current user.
        :param type Attribute type. Valid values are:
                 USER_ATTR_FIRSTNAME = 1
                 Change the firstname of the user
                 USER_ATTR_LASTNAME = 2
                 Change the lastname of the user
        :param value  New attribute value
        '''
        self.api.setUserAttribute(type, value)

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
        self.api.exportNode(node, self.create_delegate_request_listener(listener, True))

    def export_node(self, node):
    	'''Generate a public link of a file/folder in MEGA.
        :param node - MegaNode to get the public link
        '''
        self.api.exportNode(node)

    def disable_export_with_listener(self, node, listener):
    	'''Stop sharing a file/folder.
        The associated request type with this request is MegaRequest.TYPE_EXPORT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle - Returns the handle of the node
            MegaRequest.getAccess - Returns false
        :param node - MegaNode to stop sharing
        :param listener - MegaRequestListener to track this request
        '''
        self.api.disableExport(node, self.create_delegate_request_listener(listener, True))

    def disable_export(self, node):
    	'''Stop sharing a file/folder.
        :param node - MegaNode to stop sharing
        '''
        self.api.disableExport(node)

    def fetch_nodes_with_listener(self, listener):
        '''Fetch the filesystem in MEGA.
        The MegaApi object must be logged in in an account or a public folder to successfully complete this request.
        The associated request type with this request is MegaRequest.TYPE_FETCH_NODES
        :param listener - MegaRequestListener to track this request
        '''
        self.api.fetchNodes(self.create_delegate_request_listener(listener, True))

    def fetch_nodes(self):
    	'''Fetch the filesystem in MEGA.
        The MegaApi object must be logged in in an account or a public folder to successfully complete this request.
        '''
        self.api.fetchNodes()

    def get_account_details_with_listener(self, listener):
    	'''Get details about the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_ACCOUNT_DETAILS
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getMegaAccountDetails - Details of the MEGA account
        :param listener - MegaRequestListener to track this request
        '''
        self.api.getAccountDetails(self.create_delegate_request_listener(listener, True))

    def get_account_details(self):
        '''Get details about the MEGA account.
        '''
        self.api.getAccountDetails()

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
        self.api.getExtendedAccountDetails(sessions, purchases, transactions, self.create_delegate_request_listener(listener, True))

    def get_extended_account_details(self, sessions, purchases, transactions):
        '''Get details about the MEGA account.
        This function allows to optionally get data about sessions, transactions and purchases related to the account.
        :param sessions Boolean. Get sessions history if true. Do not get sessions history if false
        :param purchases Boolean. Get purchase history if true. Do not get purchase history if false
        :param transactions Boolean. Get transactions history if true. Do not get transactions history if false
        '''
        self.api.getExtendedAccountDetails(sessions, purchases, transactions)

    def get_extended_account_details_no_transactions(self, sessions, purchases):
        '''Get details about the MEGA account.
        This function allows to optionally get data about sessions, transactions and purchases related to the account.
        :param sessions Boolean. Get sessions history if true. Do not get sessions history if false
        :param purchases Boolean. Get purchase history if true. Do not get purchase history if false
        '''
        self.api.getExtendedAccountDetails(sessions, purchases)

    def get_extended_account_details_only_sessions(self, sessions):
        '''Get details about the MEGA account.
        This function allows to optionally get data about sessions, transactions and purchases related to the account.
        :param sessions Boolean. Get sessions history if true. Do not get sessions history if false
        '''
        self.api.getExtendedAccountDetails(sessions)

    def get_all_extended_account_details(self):
        '''Get details about the MEGA account.
        '''
        self.api.getExtendedAccountDetails()

    def get_pricing_with_listener(self, listener):
    	'''Get the available pricing plans to upgrade a MEGA account.
        You can get a payment URL for any of the pricing plans provided by this function using MegaApi.get_payment_url()
        The associated request type with this request is MegaRequest.TYPE_GET_PRICING
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError.API_OK:
            MegaRequest.getPricing - MegaPricing object with all pricing plans
        :param listener - MegaRequestListener to track this request
        '''
        self.api.getPricing(self.create_delegate_request_listener(listener, True))

    def get_pricing(self):
    	'''Get the available pricing plans to upgrade a MEGA account.
        '''
        self.api.getPricing()

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
        self.api.getPaymentId(product_handle, self.create_delegate_request_listener(listener, True))

    def get_payment_id(self, product_handle):
    	'''Get the payment id for an upgrade.
        :param product_handle Handle of the product (see MegaApi.get_pricing())
        '''
        self.api.getPaymentId(product_handle)

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
        self.api.upgradeAccount(product_handle, payment_method, self.create_delegate_request_listener(listener, True))

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
        self.api.upgradeAccount(product_handle, payment_method)

    def submit_purchase_receipt_with_listener(self, receipt, listener):
    	'''Send the Google Play receipt after a correct purchase of subscription.
        :param receipt String the complete receipt from Google Play
        :param listener MegaRequestListener to track this request
        '''
        self.api.submitPurchaseReceipt(receipt, self.create_delegate_request_listener(listener, True))

    def submit_purchase_receipt(self, receipt):
    	'''Send the Google Play receipt after a correct purchase of subscription.
        :param receipt String the complete receipt from Google Play
        '''
        self.api.submitPurchaseReceipt(receipt)

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
        self.api.creditCardStore(address_1, address_2, city, province, country, postal_code,
            first_name, last_name, credit_card, expire_month, expire_year, cv_2,
            self.create_delegate_request_listener(listener, True))

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
        self.api.creditCardStore(address_1, address_2, city, province, country, postal_code,
            first_name, last_name, credit_card, expire_month, expire_year, cv_2)

    def credit_card_query_subscriptions_with_listener(self, listener):
    	'''Get the credit card subscriptions of the account.
        The associated request type with this request is MegaRequest.TYPE_CREDIT_CARD_QUERY_SUBSCRIPTIONS
        Valid data in the MegaRequest object received in onRequestFinish() when the error code
        is MegaError.API_OK:
            MegaRequest.getNumber() - Number of credit card subscriptions
        :param listener MegaRequestListener to track this request
        '''
        self.api.creditCardQuerySubscriptions(self.create_delegate_request_listener(listener, True))

    def credit_card_query_subscriptions(self):
    	'''Get the credit card subscriptions of the account.
        '''
        self.api.creditCardQuerySubscriptions()

    def credit_card_cancel_subscriptions_with_listener(self, reason,  listener):
    	'''Cancel credit card subscriptions of the account.
        The associated request type with this request is MegaRequest.TYPE_CREDIT_CARD_CANCEL_SUBSCRIPTIONS
        :param reason for cancellation it can be None
        :param listener MegaRequestListener to track this request
        '''
        self.api.creditCardCancelSubscriptions(reason, self.create_delegate_request_listener(listener, True))

    def credit_card_cancel_subscriptions(self, reason):
    	'''Cancel credit card subscriptions of the account.
        :param reason for cancellation it can be None
        '''
        self.api.creditCardCancelSubscriptions(reason)

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
        self.api.getPaymentMethods(self.create_delegate_request_listener(listener, True))

    def get_payment_methods(self):
    	'''Get the available payment methods.
        '''
        self.api.getPaymentMethods()

    def export_master_key(self):
    	'''Export the master key of the account.
        The returned value is a Base64-encoded string
        With the master key, it's possible to start the recovery of an account when the password is lost:
            https://mega.co.nz/#recovery
        You take the ownership of the returned value.
        :Returns Base64-encoded master key
        '''
        return self.api.exportMasterKey()

    def change_password_with_listener(self, old_pass, new_pass, listener):
    	'''Change the password of the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_CHANGE_PW Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getPassword - Returns the old password
            MegaRequest.getNewPassword - Returns the new password
        :param old_pass - old password
        :param new_pass - new password
        :param listener - MegaRequestListener to track this request
        '''
        self.api.changePassword(old_pass, new_pass, self.create_delegate_request_listener(listener, True))

    def change_password(self, old_pass, new_pass):
    	'''Change the password of the MEGA account.
        :param old_pass - old password
        :param new_pass - new password
        '''
        self.api.changePassword(old_pass, new_pass)

    def add_contact_with_listener(self, email, listener):
    	'''Add a new contact to the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_ADD_CONTACT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail - Returns the email of the contact
        :param email - Email of the new contact
        :param listener - MegaRequestListener to track this request
        :deprecated
        '''
        self.api.addContact(email, self.create_delegate_request_listener(listener, True))

    def add_contact(self, email):
    	'''Add a new contact to the MEGA account.
        :param email - Email of the new contact
        :deprecated
        '''
        self.api.addContact(email)

    def invite_contact_with_listener(self, email, message, action, listener):
    	'''Invite another person to be your MEGA contact.
        The user does not need to be registered with MEGA. If the email is not associated with
        a MEGA account, an invitation email will be sent with the text in the "message" parameter.
        The associated request type with this request is MegaRequest.TYPE_INVITE_CONTACT.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail() - Returns the email of the contact
            MegaRequest.getText() - Returns the text of the invitation
        :param email Email of the new contact
        :param message Message for the user (can be null)
        :param action Action for this contact request. Valid values are:
            MegaContactRequest.INVITE_ACTION_ADD = 0
            MegaContactRequest.INVITE_ACTION_DELETE = 1
            MegaContactRequest.INVITE_ACTION_REMIND = 2
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.api.inviteContact(email, message, action, self.create_delegate_request_listener(listener, True))

    def invite_contact(self, email, message, action):
    	'''Invite another person to be your MEGA contact.
        The user does not need to be registered with MEGA. If the email is not associated with
        a MEGA account, an invitation email will be sent with the text in the "message" parameter.
        :param email Email of the new contact
        :param message Message for the user (can be null)
        :param action Action for this contact request. Valid values are:
            MegaContactRequest.INVITE_ACTION_ADD = 0
            MegaContactRequest.INVITE_ACTION_DELETE = 1
            MegaContactRequest.INVITE_ACTION_REMIND = 2
        '''
        self.api.inviteContact(email, message, action)

    def reply_contact_request_with_listener(self, request, action, listener):
    	'''Reply to a contact request.
        :param request Contact request. You can get your pending contact requests using
        MegaApi.get_incoming_contact_requests()
        :param action Action for this contact request. Valid values are:
            MegaContactRequest.REPLY_ACTION_ACCEPT = 0
            MegaContactRequest.REPLY_ACTION_DENY = 1
            MegaContactRequest.REPLY_ACTION_IGNORE = 2
        The associated request type with this request is MegaRequest.TYPE_REPLY_CONTACT_REQUEST.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getNodeHandle() - Returns the handle of the contact request
            MegaRequest.getNumber() - Returns the action
        :param listener MegaRequestListenerInterface to track this request
        '''
        self.api.replyContactRequest(request, action, self.create_delegate_request_listener(listener, True))

    def reply_contact_request(self, request, action):
        '''Reply to a contact request
        :param request Contact request. You can get your pending contact requests using
        MegaApi.get_incoming_contact_requests()
        :param action Action for this contact request. Valid values are:
            MegaContactRequest.REPLY_ACTION_ACCEPT = 0
            MegaContactRequest.REPLY_ACTION_DENY = 1
            MegaContactRequest.REPLY_ACTION_IGNORE = 2
        '''
        self.api.replyContactRequest(request, action)

    def remove_contact(self, user, listener):
    	'''Remove a contact to the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_REMOVE_CONTACT Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getEmail - Returns the email of the contact
        :param user - 	MegaUser of the contact (see MegaApi.getContact)
        :param listener - MegaRequestListener to track this request
        '''
        self.api.removeContact(user, self.create_delegate_request_listener(listener, True))

    def logout_from_account_with_listener(self, listener):
    	'''Logout of the MEGA account.
        The associated request type with this request is MegaRequest.TYPE_LOGOUT
        :param listener - MegaRequestListener to track this request
        '''
        self.api.logout(self.create_delegate_request_listener(listener, True))

    def logout_from_account(self):
        '''Logout of the MEGA account.
        '''
        self.api.logout()

    def local_logout_with_listener(self, listener):
    	'''Logout of the MEGA account without invalidating the session.
        The associated request type with this request is MegaRequest.TYPE_LOGOUT.
        :param listener MegaRequestListener to track this request
        '''
        self.api.localLogout(self.create_delegate_request_listener(listener, True))

    def local_logout():
        '''Logout of the MEGA account without invalidating the session.
        '''
        self.api.localLogout()

    def submit_feedback_with_listener(self, rating, comment, listener):
    	'''Submit feedback about the app.
        The user agent is used to identify the app. It can be set in MegaApi.MegaApi()
        The associated request type with this request if MegaRequest.TYPE_REPORT_EVENT.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest,getParamType() Returns MegaApi.EVENT_FEEDBACK
            MegaRequest.getText() Returns the comment about app
            MegaRequest.getNumber() Returns the raiting for the app.
        :param rating Integer to rate the app. Valid values: from 1 to 5.
        :param comment Comment about the app.
        :param listener MegaRequestListener to track this request
        :Deprecated for internal usage
        '''
        self.api.submitFeedback(rating, comment, self.create_delegate_request_listener(listener, True))

    def submit_feedback(self, rating, comment):
    	'''Submit feedback about the app.
        The user agent is used to identify the app. It can be set in MegaApi.MegaApi()
        :param rating Integer to rate the app. Valid values: from 1 to 5.
        :param comment Comment about the app.
        :Deprecated for internal usage
        '''
        self.api.submitFeedback(rating, comment)

    def report_debug_event_with_listener(self, text, listener):
    	'''Send a debug report.
        The user agent is used to identify the app. It can be set in MegaApi.MegaApi()
        The associated request type with this request if MegaRequest.TYPE_REPORT_EVENT.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest,getParamType() Returns MegaApi.EVENT_DEBUG
            MegaRequest.getText() Returns the debug message
        :param text Debug message.
        :param listener MegaRequestListener to track this request
        :Deprecated for internal usage
        '''
        self.api.reportDebugEvent(text, self.create_delegate_request_listener(listener, True))

    def report_debug_event(self, text):
    	'''Send a debug report.
        The user agent is used to identify the app. It can be set in MegaApi.MegaApi()
        The associated request type with this request if MegaRequest.TYPE_REPORT_EVENT.
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest,getParamType() Returns MegaApi.EVENT_DEBUG
            MegaRequest.getText() Returns the debug message
        :param text Debug message.
        :Deprecated for internal usage
        '''
        self.api.reportDebugEvent(text)

    # TRANSFERS

    def start_upload_with_listener(self, local_path, parent, listener):
    	'''Upload a file.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param listener - MegaTransferListener to track this transfer
        '''
        self.api.startUpload(local_path, parent, self.create_delegate_transfer_listener(listener, True))

    def start_upload(self, local_path, parent):
    	'''Upload a file.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        '''
        self.api.startUpload(local_path, parent)

    def start_upload_custom_modification_time_with_listener(self, local_path, parent, mtime, listener):
    	'''Upload a file with custom modification time.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param mtime Custom modification time for the file in MEGA (in seconds since the
        epoch)
        :param listener - MegaTransferListener to track this transfer
        '''
        self.api.startUpload(local_path, parent, mtime, self.create_delegate_transfer_listener(listener, True))

    def start_upload_custom_modification_time(self, local_path, parent, mtime):
    	'''Upload a file with custom modification time.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param mtime Custom modification time for the file in MEGA (in seconds since the
        epoch)
        '''
        self.api.startUpload(local_path, parent, mtime)

    def start_upload_custom_name_with_listener(self, local_path, parent, name, listener):
    	'''Upload a file with custom name.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param name Custom file name for the file in MEGA
        :param listener MegaTransferListener to track this transfer
        '''
        self.api.startUpload(local_path, parent, name, self.create_delegate_transfer_listener(listener, True))

    def start_upload_custom_name(self, local_path, parent, name):
    	'''Upload a file with custom name.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param name Custom file name for the file in MEGA
        '''
        self.api.startUpload(local_path, parent, name)

    def start_upload_custom_name_modification_time_with_listener(self, local_path, parent,
        name, mtime, listener):
    	'''Upload a file with custom name and modification time.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param name Custom file name for the file in MEGA
        :param mtime Custom modification time for the file in MEGA (in seconds since the
        epoch)
        :param listener MegaTransferListener to track this transfer
        '''
        self.api.startUpload(local_path, parent, name, mtime, self.create_delegate_transfer_listener(listener, True))

    def start_upload_custom_name_modification_time(self, local_path, parent,
        name, mtime):
    	'''Upload a file with custom name and modification time.
        :param local_path - Local path of the file
        :param parent - Parent node for the file in the MEGA account
        :param name Custom file name for the file in MEGA
        :param mtime Custom modification time for the file in MEGA (in seconds since the
        epoch)
        '''
        self.api.startUpload(local_path, parent, name, mtime)

    def start_download_with_listener(self, node, local_path, listener):
    	'''Download a file from MEGA.
        :param node - MegaNode that identifies the file
        :param local_path - Destination path for the file If this path is a local folder,
        it must end with a '\' or '/' character and the file name in MEGA will be used to
        store a file inside that folder. If the path doesn't finish with one of these characters,
        the file will be downloaded to a file in that path.
        :param listener - MegaTransferListener to track this transfer
        '''
        self.api.startDownload(node, local_path, self.create_delegate_transfer_listener(listener, True))

    def start_download(self, node, local_path):
    	'''Download a file from MEGA.
        :param node - MegaNode that identifies the file
        :param local_path - Destination path for the file If this path is a local folder,
        it must end with a '\' or '/' character and the file name in MEGA will be used to
        store a file inside that folder. If the path doesn't finish with one of these characters,
        the file will be downloaded to a file in that path.
        '''
        self.api.startDownload(node, local_path)

    def start_streaming(self, node, start_pos, size, listener):
    	'''Start a streaming download.
        Streaming downloads don't save the downloaded data into a local file. It is provided in MegaTransferListener.onTransferUpdate in a byte buffer.
        Only the MegaTransferListener passed to this function will receive MegaTransferListener.onTransferData callbacks.
        MegaTransferListener objects registered with MegaApi.addTransferListener won't receive them for performance reasons
        :param node - MegaNode that identifies the file (public nodes aren't supported yet)
        :param start_pos - First byte to download from the file
        :param size - Size of the data to download
        :param listener - MegaTransferListener to track this transfer
        '''
        self.api.startStreaming(node, start_pos, size, self.create_delegate_transfer_listener(listener, True))

    def cancel_transfer_with_listener(self, transfer, listener):
    	'''Cancel a transfer.
        When a transfer is cancelled, it will finish and will provide the error code MegaError.API_EINCOMPLETE
        in MegaTransferListener.onTransferFinish and MegaListener.onTransferFinish
        The associated request type with this request is MegaRequest.TYPE_CANCEL_TRANSFER Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getTransferTag - Returns the tag of the cancelled transfer (MegaTransfer.getTag)
        :param transfer - MegaTransfer object that identifies the transfer You can get this object
        in any MegaTransferListener callback or any MegaListener callback related to transfers.
        :param listener - MegaRequestListener to track this request
        '''
        self.api.cancelTransfer(transfer, self.create_delegate_request_listener(listener, True))

    def cancel_transfer(self, transfer):
    	'''Cancel a transfer.
        :param transfer - MegaTransfer object that identifies the transfer You can get this object
        in any MegaTransferListener callback or any MegaListener callback related to transfers.
        '''
        self.api.cancelTransfer(transfer)

    def cancel_transfer_by_tag_with_listener(self, transfer_tag, listener):
    	'''Cancel the transfer with a specific tag.
        When a transfer is cancelled, it will finish and will provide error code
        MegaError.API_EINCOMPLETE in MegaTransferListener.onTransferFinish() and
        MegaListener.onTransferFinish().
        The associated request type with this request is MegaRequest.TYPE_CANCEL_TRANSFER
        Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getTransferTag() Returns the tag of the cancelled transfer
            (MegaTransfer.getTag).
        :param transfer_tag tag that identifies the transfer. You can get this tag
        using MegaTransfer.getTag().
        :param listener MegaRequestListener to track this request
        '''
        self.api.cancelTransferByTag(transfer_tag, self.create_delegate_request_listener(listener, True))

    def cancel_transfer_by_tag(self, transfer_tag):
        '''Cancel transfer with a specific tag.
        :param transfer_tag tag that identifies the transfer. You can get this
        tag using MegaTransfer.getTag()
        '''
        self.api.cancelTransferByTag(transfer_tag)

    def cancel_transfers_with_listener(self, type, listener):
    	'''Cancel all transfers of the same type.
        The associated request type with this request is MegaRequest.TYPE_CANCEL_TRANSFERS Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getParamType - Returns the first parameter
        :param type - 	Type of transfers to cancel. Valid values are:
            MegaTransfer.TYPE_DOWNLOAD = 0
            MegaTransfer.TYPE_UPLOAD = 1
        :param listener - MegaRequestListener to track this request
        '''
        self.api.cancelTransfers(type, self.create_delegate_request_listener(listener, True))

    def cancel_transfers(self, type):
        '''Cancel all transfers of the same type.
        :param type - 	Type of transfers to cancel. Valid values are:
            MegaTransfer.TYPE_DOWNLOAD = 0
            MegaTransfer.TYPE_UPLOAD = 1
        '''
        self.api.cancel_transfers(type)

    def pause_transfers_with_listener(self, pause, listener):
    	'''Pause/resume all transfers.
        The associated request type with this request is MegaRequest.TYPE_PAUSE_TRANSFERS Valid data in the MegaRequest object received on callbacks:
            MegaRequest.getFlag - Returns the first parameter
        :param pause - True to pause all transfers or False to resume all transfers
        :param listener - MegaRequestListener to track this request
        '''
        self.api.pauseTransfers(pause, self.create_delegate_request_listener(listener, True))

    def pause_transfers(self, pause):
    	'''Pause/resume all transfers.
        :param pause - True to pause all transfers or False to resume all transfers
        '''
        self.api.pauseTransfers(pause)

    def set_upload_limit(self, bps_limit):
    	'''Set the upload speed limit.
        The limit will be applied on the server side when starting a transfer.
        Thus the limit won't be applied for already started uploads and it's applied per storage server.
        :param bps_limit - -1 to automatically select the limit, 0 for no limit,
        otherwise the speed limit in bytes per second
        '''
        self.api.setUploadLimit(bps_limit)

    def get_transfer_by_tag(self, transfer_tag):
    	'''Get the transfer with a transfer tag.
        MegaTransfer.getTag() can be used to get transfer tag.
        :param transfer_tag
        :Returns MegaTransfer object with the tag, or null if there is not any
        active transfers with it.
        '''
        return self.api.getTransferByTag(self.api, args)

    def do_update(self):
    	'''Force a loop of the SDK thread.
        :Deprecated
        '''
        self.api.update()

    def is_waiting(self):
    	'''Check if the SDK is waiting for the server.
		:Returns True if the SDK is waiting for the server to complete a request
		'''
        return self.api.isWaiting()

    def get_num_pending_uploads(self):
    	'''Get the number of pending uploads.
		:Returns the number of pending uploads.
        :Deprecated
		'''
        return self.api.getNumPendingUploads()

    def get_num_pending_downloads(self):
    	'''Get the number of pending downloads.
		:Returns the number of pending downloads.
        :Deprecated
		'''
        return self.api.getNumPendingDownloads()

    def get_total_uploads(self):
    	'''Get the number of queued uploads since the last call to MegaApi.resetTotalUploads.
		:Returns number of queued uploads since the last call to MegaApi.resetTotalUploads
        :Deprecated
		'''
        return self.api.getTotalUploads()

    def get_total_downloads(self):
    	'''Get the number of queued uploads since the last call to MegaApi.resetTotalDownloads.
		:Returns number of queued uploads since the last call to MegaApi.resetTotalDownloads
        :Deprecated
		'''
        return self.api.getTotalDownloads()

    def reset_total_downloads(self):
    	'''Reset the number of total downloads This function resets the number returned by MegaApi.get_total_downloads().
        :Deprecated
		'''
        self.api.resetTotalDownloads()

    def reset_total_uploads(self):
    	'''Reset the number of total uploads This function resets the number returned by MegaApi.get_total_uploads().
        :Deprecated
		'''
        self.api.resetTotalUploads()

    def get_total_downloaded_bytes(self):
    	'''Get the total downloaded bytes since the creation of the MegaApi object.
		:Returns total downloaded bytes since the creation of the MegaApi object
        :Deprecated
		'''
        return self.api.getTotalDownloadedBytes()

    def get_total_uploaded_bytes(self):
    	'''Get the total uploaded bytes since the creation of the MegaApi object.
		:Returns total uploaded bytes since the creation of the MegaApi object
        :Deprecated
		'''
        return self.api.getTotalUploadedBytes()

    def update_stats(self):
    	'''Force a loop of the SDK thread. '''
        self.api.updateStats()

    def get_transfers(self):
    	'''Get all active transfers.
		You take the ownership of the returned value
		:Returns list with all active downloads or uploads
		'''
        return self.api.transfer_list_to_array(self.getTransfers())

    def get_transfers_based_on_type(self, type):
    	'''Get all active transfers based on type.
		You take the ownership of the returned value
		:Returns list with all active downloads or uploads
		'''
        return self.api.transfer_list_to_array(self.getTransfers(type))

    # FILESYSTEM METHODS

    def get_num_children(self, parent):
    	'''Get the number of child nodes.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child nodes.
        :param parent - Parent node
        :Returns Number of child nodes
        '''
        return self.api.getNumChildren(parent)

    def get_num_child_files(self, parent):
    	'''Get the number of child files of a node.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child files.
        :parent parent - Parent node
        :Returns Number of child files
        '''
        return self.api.getNumChildFiles(parent)

    def get_num_child_folders(self, parent):
    	'''Get the number of child folders of a node.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child folders.
        :param parent - Parent node
        :Returns Number of child folders
        '''
        return self.api.getNumChildFolders(parent)

    def get_index_with_order(self, node, order):
    	'''Get the current index of the node in the parent folder for a specific sorting order.
        If the node doesn't exist or it doesn't have a parent node (because it's a root node) this function returns -1
        :param node - Node to check
        :param order - Sorting order to use
        :Returns index of the node in its parent folder
        '''
        return self.api.getIndex(node, order)

    def get_index(self, node):
    	'''Get the current index of the node in the parent folder.
        If the node doesn't exist or it doesn't have a parent node (because it's a root node) this function returns -1
        :param node - Node to check
        :Returns index of the node in its parent folder
        '''
        return self.api.getIndex(node)

    def get_child_node(self, parent, name):
    	'''Get the child node with the provided name.
        If the node doesn't exist, this function returns None
        You take the ownership of the returned value
        :param parent - Parent node
        :param name - name of the node
        :Returns The MegaNode that has the selected parent and name
        '''
        return self.api.getChildNode(parent, name)

    def get_parent_node(self, node):
    	'''Get the parent node of a MegaNode.
        If the node doesn't exist in the account or it is a root node, this function returns NULL
        You take the ownership of the returned value.
        :param node - MegaNode to get the parent
        :Returns the parent of the provided node
        '''
        return self.api.getParentNode(node)

    def get_node_path(self, node):
    	'''Get the path of a MegaNode.
        If the node doesn't exist, this function returns NULL. You can recoved the node later using MegaApi.getNodeByPath except if the path contains names with '/', '\' or ':' characters.
        You take the ownership of the returned value
        :param node - MegaNode for which the path will be returned
        :Returns the path of the node
        '''
        return self.api.getNodePath(node)

    def get_node_by_path_base_folder(self, path, base_folder):
    	'''Get the MegaNode in a specific path in the MEGA account.
        The path separator character is '/' The Root node is / The Inbox root node is //in/ The Rubbish root node is //bin/
        Paths with names containing '/', '\' or ':' aren't compatible with this function.
        :param path - Path to check
        :param base_node Base node if the path is relative
        :Returns The MegaNode object in the path, otherwise None
        '''
        return self.api.getNodeByPath(path, base_folder)

    def get_node_by_path(self, path):
    	'''Get the MegaNode in a specific path in the MEGA account.
        The path separator character is '/' The Root node is / The Inbox root node is //in/ The Rubbish root node is //bin/
        Paths with names containing '/', '\' or ':' aren't compatible with this function.
        :param path - Path to check
        :Returns The MegaNode object in the path, otherwise None
        '''
        return self.api.getNodeByPath(path)

    def get_node_by_handle(self, handle):
    	'''Get the MegaNode that has a specific handle.
        You can get the handle of a MegaNode using MegaNode.getHandle. The same handle can be got in a Base64-encoded string using MegaNode.getBase64Handle. Conversions between these formats can be done using MegaApi.base64ToHandle and MegaApi.handleToBase64.
        It is needed to be logged in and to have successfully completed a fetchNodes request before calling this function. Otherwise, it will return None.
        You take the ownership of the returned value.
        :param handle - Node handle to check
        :Returns MegaNode object with the handle, otherwise None
        '''
        return self.api.getNodeByHandle(handle)

    def get_contact_request_by_handle(self, handle):
    	'''Get the MegaContactRequest that has a specific handle.
        You can get the handle of a MegaContactRequest using MegaContactRequest.getHandle().
        You take the ownership of the returned value.
        :param handle Contact request handle to check.
        :Returns MegaContactRequest object with handle, otherwise None
        '''
        return self.api.getContactRequestByHandle(handle)


    def get_contact(self, email):
    	'''Get the MegaUser that has a specific email address.
        You can get the email of a MegaUser using MegaUser.getEmail
        You take the ownership of the returned value
        :param email - Email address to check
        :Returns MegaUser that has the email address, otherwise None
        '''
        return self.api.getContact(email)



    def is_shared(self, node):
    	'''Check if a MegaNode is being shared.
        For nodes that are being shared, you can get a a list of MegaShare objects using MegaApi.getOutShares
        :param node - Node to check
        :Returns True if the MegaNode is being shared, otherwise False
        '''
        return self.api.isShared(node)


    def get_access(self, node):
    	'''Get the access level of a MegaNode.
        :param node - MegaNode to check
        :Returns Access level of the node Valid values are:
            MegaShare.ACCESS_OWNER
            MegaShare.ACCESS_FULL
            MegaShare.ACCESS_READWRITE
            MegaShare.ACCESS_READ
            MegaShare.ACCESS_UNKNOWN
        '''
        return self.api.getAccess(node)

    def get_size(self, node):
    	'''Get the size of a node tree.
        If the MegaNode is a file, this function returns the size of the file. If it's a folder, this fuction returns the sum of the sizes of all nodes in the node tree.
        :param node - Parent node
        :Returns size of the node tree
        '''
        return self.api.getSize(node)

    def get_fingerprint_node(self, node):
    	'''Get a Base64-encoded fingerprint for a node.
        If the node doesn't exist or doesn't have a fingerprint, this function returns None.
        You take the ownership of the returned value
        :param node - Node for which we want to get the fingerprint
        :Returns Base64-encoded fingerprint for the file
        '''
        return self.api.getFingerprint(node)

    def get_fingerprint_filepath(self, file_path):
    	'''Get a Base64-encoded fingerprint for a local file.
        The fingerprint is created taking into account the modification time of
        the file and file contents. This fingerprint can be used to get a
        corresponding node in MEGA using MegaApi.get_node_by_fingerprint()
        If the file can't be found or can't be opened, this function returns
        None.
        :param file_path - Local file path
        :Returns Base64-encoded fingerprint for the file
        '''
        return self.api.getFingerprint(file_path)

    def get_node_by_fingerprint(self, fingerprint):
    	'''Returns a node with the provided fingerprint.
        If there isn't any node in the account with that fingerprint, this function returns None.
        You take the ownership of the returned value.
        :param fingerprint - Fingerprint to check
        :Returns MegaNode object with the provided fingerprint
        '''
        return self.api.getNodeByFingerprint(fingerprint)

    def get_node_by_fingerprint_preferred_parent(self, fingerprint, preferred_parent):
        return self.api.getNodeByFingerprint(fingerprint, preferred_parent)

    def has_fingerprint(self, fingerprint):
    	'''Check if the account already has a node with the provided fingerprint.
        A fingerprint for a local file can be generated using MegaApi.getFingerprint
        :param fingerprint - Fingerprint to check
        :Returns True if the account contains a node with the same fingerprint
        '''
        return self.api.hasFingerprint(fingerprint)

    def check_access(self, node, level):
    	'''Check if a node has an access level.
        :param node - Node to check
        :param level - Access level to check Valid values for this parameter are:
            MegaShare.ACCESS_OWNER
            MegaShare.ACCESS_FULL
            MegaShare.ACCESS_READWRITE
            MegaShare.ACCESS_READ
        :Returns MegaError object with the result.Valid values for the error code are:
            MegaError.API_OK - The node can be moved to the target
            MegaError.API_EACCESS - The node can't be moved because of permissions problems
            MegaError.API_ECIRCULAR - The node can't be moved because that would create a circular linkage
            MegaError.API_ENOENT - The node or the target doesn't exist in the account
            MegaError.API_EARGS - Invalid parameters
        '''
        return self.api.checkAccess(node, level)

    def check_move(self, node, target):
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
        return self.api.checkMove(node, target)

    def get_root_node(self):
    	'''Returns the root node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi.fetch_nodes before, this function returns None
        :Returns Root node of the account
        '''
        return self.api.getRootNode()

    def get_inbox_node(self):
    	'''Returns the inbox node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi.fetch_nodes before, this function returns None
        :Returns Inbox node of the account
        '''
        return self.api.getInboxNode()

    def get_rubbish_node(self):
    	'''Returns the rubbish node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi.fetch_nodes before, this function returns None
        :Returns Rubbish node of the account
        '''
        return self.api.getRubbishNode()

    def get_version(self):
    	'''Get the SDK version.
        :Returns the SDK version
        '''
        return self.api.getVersion()

    def get_user_agent(self):
    	'''Get the User-Agent header used by the SDK.
        :Returns User-Agent used by the SDK.
        '''
        return self.api.getUserAgent()

    def change_api_url(self, api_url):
    	'''Changed the API URL.
        Please note, this method does not disable public key pinning.
        :param api_url The API URL to change
        '''
        self.api.changeApiUrl(api_url)

    def change_api_url_disable_pkp(self, api_url, disable_pkp):
    	'''Changed the API URL.
        Please note, this method does not disable public key pinning.
        :param api_url The API URL to change
        :param disable_pkp boolean. Disable public key pinning if True. Do not
        disable public key binning if False.
        '''
        self.api.changeApiUrl(api_url, disable_pkp)

    def escape_fs_incompatible(self, name):
    	'''Make a name suitable for a file name in the local filesystem.
        This function escapes (%xx) forbidden characters in the local
        filesystem if needed.You can revert this operation using
        MegaApi.unescape_fs_incompatible()
        :param name Name to convert
        :Returns Converted name
        '''
        return self.api.escapeFsIncompatible(name)

    def unescape_fs_incompatible(self, local_name):
    	'''Unescape a file name escaped with MegaApi.unescape_fs_incompatible().
        :param local_name Escape name to convert
        :Returns Converted name
        '''
        return self.api.unescapeFsIncompatible(local_name)

    def create_thumbnail(self, image_path, dst_path):
    	'''Create a thumbnail for an image.
        :param image_path Image path.
        :param dst_path Destination path for the thumbnail (including the file name).
        :Returns True if the thumbnail was successfully created, otherwise False.
        '''
        return self.api.createThumbnail(image_path, dst_path)

    def create_preview(self, image_path, dst_path):
    	'''Create a preview for an image.
        :param image_path Image path.
        :param dst_path Destination path for the preview (including the file name).
        :Returns True if the preview was successfully created, otherwise False.
        '''
        return self.api.createPreview(image_path, dst_path)

    def base64_to_base32(self, base64):
        '''Convert a Base64 string to Base32.
        If the input pointer is None, function will return None.
        If the input character array is not valid base64 string the
        effect is undefined
        :param base64 null-terminated base64 character array.
        :Returns null-terminated base32 character array.
        '''
        return self.api.base64ToBase32(base64)

    def base32_to_base64(base32):
        '''Convert a Base32 string to Base64.
        If the input pointer is None, function will return None.
        If the input character array is not valid base32 string the
        effect is undefined
        :param base32 null-terminated base64 character array.
        :Returns null-terminated base64 character array.
        '''
        return self.api.base32ToBase64(base32)

    def remove_recursively(self, local_path):
        '''Recursively removes a file
        :param local_path path to file
        '''
        self.api.removeRecursively(local_path)

    def get_contacts(self):
    	'''Get all contacts of this MEGA account.
        You take the ownership of the returned value
        :Returns List of MegaUser object with all contacts of this account
        '''
        return self.user_list_to_array(self.api.getContacts())

    def get_in_shares(self, user):
    	'''Get a list with all inbound sharings from one MegaUser.
        You take the ownership of the returned value
        :param user - MegaUser sharing folders with this account
        :Returns List of MegaNode objects that this user is sharing with this account
        '''
        return self.node_list_to_array(self.api.getInShares(user))

    def get_all_in_shares(self):
    	'''Get a list with all inbound sharings.
        You take the ownership of the returned value
        :Returns List of MegaNode objects that this user is sharing with this account
        '''
        return self.node_list_to_array(self.api.getInShares())

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
        return self.node_list_to_array(self.api.getChildren(parent, order))

    def get_out_shares(self, node):
    	'''Get a list with the active outbound sharings for a MegaNode.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :param node - MegaNode to check
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.api.getOutShares(node))

    def get_all_out_shares(self):
    	'''Get a list with the active outbound sharings for the current account.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.api.getOutShares())

    def get_pending_out_shares(self, node):
    	'''Get a list with the pending outbound sharings for a MegaNode.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :param node - MegaNode to check
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.api.getPendingOutShares(node))

    def get_all_pending_out_shares(self):
    	'''Get a list with the pending outbound sharings for the current account.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :Returns List of MegaShare objects
        '''
        return self.share_list_to_array(self.api.getPendingOutShares())

    def get_incoming_contact_requests(self):
        '''Get a list with all incoming contact requests
        :Returns list of MegaContactRequest objects
        '''
        return self.contact_request_list_to_array(self.api.getIncomingContactRequests())

    def get_outgoing_contact_requests(self):
        '''Get a list with all outgoing contact requests
        :Returns list of MegaContactRequest objects
        '''
        return self.contact_request_list_to_array(self.api.getOutgoingContactRequests())

    def search_item(self, parent, search_string):
    	'''Search nodes containing a search string in their name.
		The search is case-insensitive.
    	:param node	The parent node of the tree to explore
    	:param searchString	Search string. The search is case-insensitive
		:Returns list of nodes that contain the desired string in their name
    	'''
        return self.node_list_to_array(self.api.search(parent, search_string))

    def search_recursively(self, parent, search_string, recursive):
    	'''Search nodes containing a search string in their name.
		The search is case-insensitive.
    	:param node	The parent node of the tree to explore
    	:param searchString	Search string. The search is case-insensitive
    	:param recursive	True if you want to seach recursively in the node tree. False if you want to seach in the children of the node only
		:Returns list of nodes that contain the desired string in their name
    	'''
        return self.node_list_to_array(self.api.search(parent, search_string, recursive))

    ### PRIVATE METHODS ###

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

    def onRequestStart(self, api, request):
        '''This function is called when a request is about to start being processed.
        The SDK retains the ownership of the request parameter. Do not it use after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the request
        :param request Information about the request.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            self.listener.onRequestStart(self.mega_api, mega_request)



    def onRequestFinish(self, api, request, error):
        '''This function is called when a request has finished.
        There will be no further callbacks related to this request.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the request
        :param request Information about the request
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            mega_error = error.copy()
            self.listener.onRequestFinish(self.mega_api, mega_request, mega_error)
        if single_listener:
            self.mega_api.free_request_listener()

    def onRequestUpdate(self, api, request):
        '''This function is called to get details about the progress of a request.
        Currently, this callback is only used for fetchNodes requests (MegaRequest.TYPE_FETCH_NODES).
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the request
        :param request Information about the request
        '''
        if self.listener is not None:
            mega_request = request.copy()
            self.listener.onRequestUpdate(self.mega_api, mega_request)



    def onRequestTemporaryError(self, api, request, error):
        '''This function is called when there is a temporary error processing a request.
        The request continues after this callback, so expect more MegaRequestListener.onRequestTemporaryError or
        a MegaRequestListener.onRequestFinish callback.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the request
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


    def onTransferStart(self, api, transfer):
        '''This function is called when a transfer is about to start being processed.
        The SDK retains the ownership of the transfer parameter. Do not it use after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param transfer Information about the transfer.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferStart(self.mega_api, mega_transfer)



    def onTransferFinish(self, api, transfer, error):
        '''This function is called when a transfer has finished.
        There will be no further callbacks related to this transfer. The last parameter provides the result of the transfer.
        If the transfer completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the transfer and error parameters. Do not use them after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param transfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferFinish(self.mega_api, mega_transfer, mega_error)


    def onTransferUpdate(self, api, transfer):
        '''This function is called to get details about the progress of a transfer.
        The SDK retains the ownership of the transfer parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param transfer Information about the transfer
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferUpdate(self.mega_api, mega_transfer)



    def onTransferTemporaryError(self, api, transfer, error):
        '''This function is called when there is a temporary error processing a transfer.
        The transfer continues after this callback, so expect more MegaRequestListener.onTransferTemporaryError or
        a MegaRequestListener.onTransfertFinish callback.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param transfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferTemporaryError(self.mega_api, mega_transfer, mega_error)



    def onTransferData(self, api, transfer, buffer):
        '''This function is called to provide the last read bytes of streaming downloads.
        This function will not be called for non streaming downloads. You can get the same buffer provided
        by this function in MegaTransferListener.onTransferUpdate(), using MegaTransfer.getLastBytes() and
        MegaTransfer.getDeltaSize(). The SDK retains the ownership of this transfer and buffer parameters. Do not
        use them after this function returns.
        :param api API object that started the transfer.
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

    def onRequestStart(self, api, request):
        '''This function is called when a request is about to start being processed.
        The SDK retains the ownership of the request parameter. Do not it use after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the request
        :param request Information about the request.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            self.listener.onRequestStart(self.mega_api, mega_request)

    def onRequestFinish(self, api, request, error):
        '''This function is called when a request has finished.
        There will be no further callbacks related to this request.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the request
        :param request Information about the request
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            mega_error = error.copy()
            self.listener.onRequestFinish(self.mega_api, mega_request, mega_error)

    def onRequestTemporaryError(self, api, request, error):
        '''This function is called when there is a temporary error processing a request.
        The request continues after this callback, so expect more MegaRequestListener.onRequestTemporaryError or
        a MegaRequestListener.onRequestFinish callback.
        If the request completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the request
        :param request Information about the request
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_request = request.copy()
            mega_error = error.copy()
            self.listener.onRequestTemporaryError(self.mega_api, mega_request, mega_error)

    def onTransferStart(self, api, transfer):
        '''This function is called when a transfer is about to start being processed.
        The SDK retains the ownership of the transfer parameter. Do not it use after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param transfer Information about the transfer.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferStart(self.mega_api, mega_transfer)

    def onTransferFinish(self, api, transfer, error):
        '''This function is called when a transfer has finished.
        There will be no further callbacks related to this transfer. The last parameter provides the result of the transfer.
        If the transfer completed without problems, the error code will be API_OK.
        The SDK retains the ownership of the transfer and error parameters. Do not use them after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param transfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferFinish(self.mega_api, mega_transfer, mega_error)

    def onTransferUpdate(self, api, transfer):
        '''This function is called to get details about the progress of a transfer.
        The SDK retains the ownership of the transfer parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param transfer Information about the transfer
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferUpdate(self.mega_api, mega_transfer)

    def onTransferTemporaryError(self, api, transfer, error):
        '''This function is called when there is a temporary error processing a transfer.
        The transfer continues after this callback, so expect more MegaRequestListener.onTransferTemporaryError or
        a MegaRequestListener.onTransfertFinish callback.
        The SDK retains the ownership of the request parameter. Do not use it after this function returns.
        The api object is the one created by the application, it will be valid until the application deletes it.
        :param api API that started the transfer
        :param rtransfer Information about the transfer
        :param error Information about error.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            mega_error = error.copy()
            self.listener.onTransferTemporaryError(self.mega_api, mega_transfer, mega_error)

    def onUsersUpdate(self, api, user_list):
        '''This function is called when there are new or updated contacts in the account.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaUser objects that it contains will be valid until this function returns.
        If you want to save the list, use user_list.copy().
        If you want to save only some of the MegaUser objects, use MegaUser.copy() for those objects.
        :param api API object connected to account.
        :param user_list List that contains the new or updated contacts.
        '''
        if self.listener is not None:
            updated_user_list =  self.mega_api.user_list_to_array(user_list)
            self.listener.onUsersUpdate(self.mega_api, updated_user_list)

    def onNodesUpdate(self, api, node_list):
        '''This function is called when there are new or updated nodes in the account.
        When the full account is reloaded or a large number of server notifications arrive at once,
        the second parameter will be null.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaNode objects that it contains will be valid until this function returns.
        If you want to save the list, use node_list.copy().
        If you want to save only some of the MegaNode objects, use MegaNode.copy() for those objects.
        :param api API object connected to account.
        :param node_list List that contains the new or updated nodes.
        '''
        if self.listener is not None:
            updated_node_list = self.mega_api.node_list_to_array(node_list)
            self.listener.onNodesUpdate(self.mega_api, updated_node_list)

    def onReloadNeeded(self, api):
        '''This function is called when an inconsistency is detected in the local cache.
        You should call MegaApiPython.fetch_nodes() when this callback is received.
        :param api API object connected to account.
        '''
        if self.listener is not None:
            self.listener.onReloadNeeded(self.mega_api)

    def onAccountUpdate(self, api):
        if self.listener is not None:
            self.listener.onAccountUpdate(self.mega_api)

    def onContactRequestsUpdate(self, api, contact_request_list):
        '''This function is called when there are new contact requests in the account.
        If you want to save the list, use contact_request_list.copy().
        If you want to save only some of the MegaContactRequest objects, use MegaContactRequest.copy() for those objects.
        :param api API object connected to the account
        :param contact_request_list List that contains new contact requests
        '''
        if self.listener is not None:
            contact_list = self.mega_api.contact_request_list_to_array(contact_list)
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

    def onUsersUpdate(self, api, user_list):
        '''This function is called when there are new or updated contacts in the account.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaUser objects that it contains will be valid until this function returns.
        If you want to save the list, use user_list.copy().
        If you want to save only some of the MegaUser objects, use MegaUser.copy() for those objects.
        :param api API object connected to account.
        :param user_list List that contains the new or updated contacts.
        '''
        if self.listener is not None:
            updated_user_list =  self.mega_api.user_list_to_array(user_list)
            self.listener.onUsersUpdate(self.mega_api, updated_user_list)

    def onNodesUpdate(self, api, node_list):
        '''This function is called when there are new or updated nodes in the account.
        When the full account is reloaded or a large number of server notifications arrive at once,
        the second parameter will be null.
        The SDK retains the ownership of the user_list in the second parameter.
        The list and all the MegaNode objects that it contains will be valid until this function returns.
        If you want to save the list, use node_list.copy().
        If you want to save only some of the MegaNode objects, use MegaNode.copy() for those objects.
        :param api API object connected to account.
        :param node_list List that contains the new or updated nodes.
        '''
        if self.listener is not None:
            updated_node_list = self.mega_api.node_list_to_array(node_list)
            self.listener.onNodesUpdate(self.mega_api, updated_node_list)

    def onReloadNeeded(self, api):
        '''This function is called when an inconsistency is detected in the local cache.
        You should call MegaApiPython.fetch_nodes() when this callback is received.
        :param api API object connected to account.
        '''
        if self.listener is not None:
            self.istener.onReloadNeeded(self.mega_api)

    def onAccountUpdate(self, api):
        if self.listener is not None:
            self.listener.onAccountUpdate(self.mega_api)

    def onContactRequestsUpdate(self, api, contact_request_list):
        '''This function is called when there are new contact requests in the account.
        If you want to save the list, use contact_request_list.copy().
        If you want to save only some of the MegaContactRequest objects, use MegaContactRequest.copy() for those objects.
        :param api API object connected to the account
        :param contact_request_list List that contains new contact requests
        '''
        if self.listener is not None:
            contact_list = self.mega_api.contact_request_list_to_array(contact_list)
            self.listener.onContactRequestsUpdate(self.mega_api, contact_list)
