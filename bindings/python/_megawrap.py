from mega import *
import threading
import logging


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
        # TODO, will use threading for callback
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
            MegaApi::ORDER_NONE = 0 Undefined order
            MegaApi::ORDER_DEFAULT_ASC = 1 Folders first in alphabetical order, then files in the same order
            MegaApi::ORDER_DEFAULT_DESC = 2 Files first in reverse alphabetical order, then folders in the same order
            MegaApi::ORDER_SIZE_ASC = 3 Sort by size, ascending
            MegaApi::ORDER_SIZE_DESC = 4 Sort by size, descending
            MegaApi::ORDER_CREATION_ASC = 5 Sort by creation time in MEGA, ascending
            MegaApi::ORDER_CREATION_DESC = 6 Sort by creation time in MEGA, descending
            MegaApi::ORDER_MODIFICATION_ASC = 7 Sort by modification time of the original file, ascending
            MegaApi::ORDER_MODIFICATION_DESC = 8 Sort by modification time of the original file, descending
            MegaApi::ORDER_ALPHABETICAL_ASC = 9 Sort in alphabetical order, ascending
            MegaApi::ORDER_ALPHABETICAL_DESC = 10 Sort in alphabetical order, descending
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
            self.listener.onRequestStart(mega_api, mega_request)



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
            self.listener.onRequestFinish(mega_api, mega_request, mega_error)
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
            self.listener.onRequestUpdate(mega_api, mega_request)



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
            self.listener.onRequestTemporaryError(mega_api, mega_request, mega_error)



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
            self.listener.onTransferStart(mega_api, mega_transfer)



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
            self.listener.onTransferFinish(mega_api, mega_transfer, mega_error)


    def onTransferUpdate(self, mega_api, transfer):
        '''This function is called to get details about the progress of a transfer.
        The SDK retains the ownership of the transfer parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferUpdate(mega_api, mega_transfer)



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
            self.listener.onTransferTemporaryError(mega_api, mega_transfer, mega_error)



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
            return self.listener.onTransferData(mega_api, mega_transfer, buffer)



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
            self.listener.onRequestStart(mega_api, mega_request)
            print "Success!"

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
            self.listener.onRequestFinish(mega_request, mega_error)
            print "Fail :("

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
            self.listener.onRequestTemporaryError(mega_api, mega_request, mega_error)



    def onTransferStart(self, mega_api, transfer):
        '''This function is called when a transfer is about to start being processed.
        The SDK retains the ownership of the transfer parameter. Do not it use after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer.
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferStart(mega_api, mega_transfer)



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
            self.listener.onTransferFinish(mega_api, mega_transfer, mega_error)


    def onTransferUpdate(self, mega_api, transfer):
        '''This function is called to get details about the progress of a transfer.
        The SDK retains the ownership of the transfer parameter. Do not use it after this function returns.
        The mega_api object is the one created by the application, it will be valid until the application deletes it.
        :param mega_api API that started the transfer
        :param transfer Information about the transfer
        '''
        if self.listener is not None:
            mega_transfer = transfer.copy()
            self.listener.onTransferUpdate(mega_api, mega_transfer)  # DONT DELETE THIS LINE


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
            self.listener.onTransferTemporaryError(mega_api, mega_transfer, mega_error)



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
            self.listener.onUsersUpdate(mega_api, updated_user_list)



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
            self.listener.onNodesUpdate(mega_api, updated_node_list)



    def onReloadNeeded(self, mega_api):
        '''This function is called when an inconsistency is detected in the local cache.
        You should call MegaApiPython.fetch_nodes() when this callback is received.
        :param mega_api API object connected to account.
        '''
        if self.listener is not None:
            self.listener.onReloadNeeded(mega_api)



    def onAccountUpdate(self, mega_api):
        if self.listener is not None:
            self.listener.onAccountUpdate(mega_api)



    def onContactRequestsUpdate(self, mega_api, contact_request_list):
        '''This function is called when there are new contact requests in the account.
        If you want to save the list, use contact_request_list.copy().
        If you want to save only some of the MegaContactRequest objects, use MegaContactRequest.copy() for those objects.
        :param mega_api API object connected to the account
        :param contact_request_list List that contains new contact requests
        '''
        if self.listener is not None:
            contact_list = mega_api.contact_request_list_to_array(contact_list)
            self.listener.onContactRequestsUpdate(mega_api, contact_list)



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
            self.listener.onUsersUpdate(mega_api, updated_user_list)



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
            self.listener.onNodesUpdate(mega_api, updated_node_list)


    def onReloadNeeded(self, mega_api):
        '''This function is called when an inconsistency is detected in the local cache.
        You should call MegaApiPython.fetch_nodes() when this callback is received.
        :param mega_api API object connected to account.
        '''
        if self.listener is not None:
            self.istener.onReloadNeeded(mega_api)


    def onAccountUpdate(self, mega_api):
        if self.listener is not None:
            self.listener.onAccountUpdate(mega_api)


    def onContactRequestsUpdate(self, mega_api, contact_request_list):
        '''This function is called when there are new contact requests in the account.
        If you want to save the list, use contact_request_list.copy().
        If you want to save only some of the MegaContactRequest objects, use MegaContactRequest.copy() for those objects.
        :param mega_api API object connected to the account
        :param contact_request_list List that contains new contact requests
        '''
        if self.listener is not None:
            contact_list = mega_api.contact_request_list_to_array(contact_list)
            self.listener.onContactRequestsUpdate(mega_api, contact_list)


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
