from mega import *

class Mega_Api_Python(MegaApi):

    def __init__(self, appKey, processor, basePath, userAgent):
        super(Mega_Api_Python, self).__init__(appKey, processor, basePath, userAgent)

    # Api methods

    def get_contacts(self):
    	'''Get all contacts of this MEGA account.
        You take the ownership of the returned value
        :Returns List of MegaUser object with all contacts of this account
        '''
        return self.get_contact_list()

    def get_in_shares(self, user):
    	'''Get a list with all inbound sharings from one MegaUser.
        You take the ownership of the returned value
        :param user - MegaUser sharing folders with this account
        :Returns List of MegaNode objects that this user is sharing with this account
        '''
        return self.get_in_shares_list(user)

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
        return self.get_children_list(parent, order)

    def get_out_shares(self, node):
    	'''Get a list with the active outbound sharings for a MegaNode.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :param node - MegaNode to check
        :Returns List of MegaShare objects
        '''
        return self.get_node_out_share_list(node)

    def get_all_out_shares(self):
    	'''Get a list with the active outbound sharings for the current account.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :Returns List of MegaShare objects
        '''
        return self.get_all_out_share_list()

    def get_pending_out_shares(self, node):
    	'''Get a list with the pending outbound sharings for a MegaNode.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :param node - MegaNode to check
        :Returns List of MegaShare objects
        '''
        return self.get_node_pending_out_share_list(node)

    def get_all_pending_out_shares(self):
    	'''Get a list with the pending outbound sharings for the current account.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :Returns List of MegaShare objects
        '''
        return self.get_all_pending_out_share_list()

    def get_incoming_contact_requests(self):
        '''Get a list with all incoming contact requests
        :Returns list of MegaContactRequest objects
        '''
        return self.get_incoming_contact_request_list()

    def get_outgoing_contact_requests(self):
        '''Get a list with all outgoing contact requests
        :Returns list of MegaContactRequest objects
        '''
        return self.get_outgoing_contact_request_list()

    def search(self, parent, searchString):
    	'''Search nodes containing a search string in their name.
		The search is case-insensitive.
    	:param node	The parent node of the tree to explore
    	:param searchString	Search string. The search is case-insensitive
		:Returns list of nodes that contain the desired string in their name
    	'''
        return self.get_search_list(parent, searchString)

    def search_recursively(self, parent, searchString, recursive):
    	'''Search nodes containing a search string in their name.
		The search is case-insensitive.
    	:param node	The parent node of the tree to explore
    	:param searchString	Search string. The search is case-insensitive
    	:param recursive	True if you want to seach recursively in the node tree. False if you want to seach in the children of the node only
		:Returns list of nodes that contain the desired string in their name
    	'''
        return self.get_search_list_recursively(parent, searchString, recursive)

    def get_transfers(self):
    	'''Get all active transfers.
		You take the ownership of the returned value
		:Returns list with all active downloads or uploads
		'''
        return self.get_list_of_transfers()

    def get_transfers_based_on_type(self, type):
    	'''Get all active transfers based on type.
		You take the ownership of the returned value
		:Returns list with all active downloads or uploads
		'''
        return self.get_list_of_transfers_based_on_type(type)

    # Internal methods

    def get_contact_list(self):
        user_list = super(Mega_Api_Python, self).getContacts()
        if user_list is None:
            return None
        result = []
        for user in range(user_list.size()):
            result.append(user_list.get(user).copy())
        return result

    def get_in_shares_list(self, user):
        share_list = super(Mega_Api_Python, self).getInShares(user)
        if share_list is None:
            return None
        result = []
        for share in range(share_list.size()):
            result.append(share_list.get(share).copy())
        return result

    def get_children_list(self, parent, order):
        child_list = super(Mega_Api_Python, self).getChildren(parent, order)
        if child_list is None:
            return None
        result = []
        for child in range(child_list.size()):
            result.append(child_list.get(child).copy())
        return result

    def get_node_out_share_list(self, node):
        share_list = super(Mega_Api_Python, self).getOutShares(node)
        if share_list is None:
            return None
        result = []
        for share in range(share_list.size()):
            result.append(share_list.get(share).copy())
        return result

    def get_all_out_share_list(self):
        share_list = super(Mega_Api_Python, self).getOutShares()
        if share_list is None:
            return None
        result = []
        for share in range(share_list.size()):
            result.append(share_list.get(share).copy())
        return result

    def get_node_pending_out_share_list(self, node):
        share_list = super(Mega_Api_Python, self).getPendingOutShares(node)
        if share_list is None:
            return None
        result = []
        for share in range(share_list.size()):
            result.append(share_list.get(share).copy())
        return result

    def get_all_pending_out_share_list(self):
        share_list = super(Mega_Api_Python, self).getPendingOutShares()
        if share_list is None:
            return None
        result = []
        for share in range(share_list.size()):
            result.append(share_list.get(share).copy())
        return result

    def get_incoming_contact_request_list(self):
        contact_list = super(Mega_Api_Python, self).getIncomingContactRequests()
        if contact_list is None:
            return None
        result = []
        for contact in range(contact_list.size()):
            result.append(contact_list.get(contact).copy())
        return result

    def get_outgoing_contact_request_list(self):
        contact_list = super(Mega_Api_Python, self).getOutgoingContactRequests()
        if contact_list is None:
            return None
        result = []
        for contact in range(contact_list.size()):
            result.append(contact_list.get(contact).copy())
        return result

    def get_search_list(self, parent, searchString):
        search_list = super(Mega_Api_Python, self).search(parent, searchString)
        if search_list is None:
            return None
        result = []
        for node in range(search_list.size()):
            result.append(search_list.get(node).copy())
        return result

    def get_search_list_recursively(self, parent, searchString, recursive):
        search_list = super(Mega_Api_Python, self).search(parent, searchString, recursive)
        if search_list is None:
            return None
        result = []
        for node in range(search_list.size()):
            result.append(search_list.get(node).copy())
        return result

    def get_list_of_transfers(self):
        transfers_list = super(Mega_Api_Python, self).getTransfers()
        if transfers_list is None:
            return None
        result = []
        for transfer in range(transfers_list.size()):
            result.append(transfers_list.get(transfer).copy())
        return result

    def get_list_of_transfers_based_on_type(self, type):
        transfers_list = super(Mega_Api_Python, self).getTransfers(type)
        if transfers_list is None:
            return None
        result = []
        for transfer in range(transfers_list.size()):
            result.append(transfers_list.get(transfer).copy())
        return result








MegaApi.add_listener = MegaApi.addListener
MegaApi.add_request_listener = MegaApi.addRequestListener
MegaApi.add_transfer_listener = MegaApi.addTransferListener
MegaApi.add_global_listener = MegaApi.addGlobalListener
MegaApi.remove_listener = MegaApi.removeListener
MegaApi.remove_request_listener = MegaApi.removeRequestListener
MegaApi.remove_transfer_listener = MegaApi.removeTransferListener
MegaApi.remove_global_listener = MegaApi.removeGlobalListener
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
#MegaApi.get_transfers = MegaApi.getTransfers
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
#MegaApi.get_children = MegaApi.getChildren
MegaApi.get_index = MegaApi.getIndex
MegaApi.get_child_node = MegaApi.getChildNode
MegaApi.get_parent_node = MegaApi.getParentNode
MegaApi.get_node_path = MegaApi.getNodePath
MegaApi.get_node_by_path = MegaApi.getNodeByPath
MegaApi.get_node_by_handle = MegaApi.getNodeByHandle
MegaApi.get_contact_request_by_handle = MegaApi.getContactRequestByHandle
#MegaApi.get_contacts = MegaApi.getContacts
MegaApi.get_contact = MegaApi.getContact
#MegaApi.get_in_shares = MegaApi.getInShares
MegaApi.is_shared = MegaApi.isShared
#MegaApi.get_out_shares = MegaApi.getOutShares
#MegaApi.get_pending_out_shares = MegaApi.getPendingOutShares
#MegaApi.get_incoming_contact_requests = MegaApi.getIncomingContactRequests
#MegaApi.get_outgoing_contact_requests = MegaApi.getOutgoingContactRequests
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


del MegaApi.addListener
del MegaApi.addRequestListener
del MegaApi.addTransferListener
del MegaApi.addGlobalListener
del MegaApi.removeListener
del MegaApi.removeRequestListener
del MegaApi.removeTransferListener
del MegaApi.removeGlobalListener
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
#del MegaApi.getTransfers
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
#del MegaApi.getChildren
del MegaApi.getIndex
del MegaApi.getChildNode
del MegaApi.getParentNode
del MegaApi.getNodePath
del MegaApi.getNodeByPath
del MegaApi.getNodeByHandle
del MegaApi.getContactRequestByHandle
#del MegaApi.getContacts
del MegaApi.getContact
#del MegaApi.getInShares
del MegaApi.isShared
#del MegaApi.getOutShares
#del MegaApi.getPendingOutShares
#del MegaApi.getIncomingContactRequests
#del MegaApi.getOutgoingContactRequests
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
