from mega import *
MegaGfxProcessor.read_bitmap = MegaGfxProcessor.readBitmap
MegaGfxProcessor.get_width = MegaGfxProcessor.getWidth
MegaGfxProcessor.get_height = MegaGfxProcessor.getHeight
MegaGfxProcessor.get_bitmap_data_size = MegaGfxProcessor.getBitmapDataSize
MegaGfxProcessor.get_bitmap_data = MegaGfxProcessor.getBitmapData 
MegaGfxProcessor.free_bitmap = MegaGfxProcessor.freeBitmap

MegaProxy.set_proxy_type = MegaProxy.setProxyType
MegaProxy.set_proxy_url = MegaProxy.setProxyURL
MegaProxy.set_credentials = MegaProxy.setCredentials
MegaProxy.get_proxy_type = MegaProxy.getProxyType
MegaProxy.get_proxy_url = MegaProxy.getProxyURL
MegaProxy.credentials_needed = MegaProxy.credentialsNeeded
MegaProxy.get_username = MegaProxy.getUsername
MegaProxy.get_password = MegaProxy.getPassword

MegaNode.get_type = MegaNode.getType
MegaNode.get_name = MegaNode.getName
MegaNode.get_base64_handle = MegaNode.getBase64Handle
MegaNode.get_size = MegaNode.getSize
MegaNode.get_creation_time = MegaNode.getCreationTime
MegaNode.get_modification_time = MegaNode.getModificationTime
MegaNode.get_handle = MegaNode.getHandle
MegaNode.get_parent_handle = MegaNode.getParentHandle
MegaNode.get_base64_key = MegaNode.getBase64Key
MegaNode.get_tag = MegaNode.getTag
MegaNode.is_file = MegaNode.isFile
MegaNode.is_folder = MegaNode.isFolder
MegaNode.is_removed = MegaNode.isRemoved
MegaNode.has_changed = MegaNode.hasChanged
MegaNode.get_changes = MegaNode.getChanges
MegaNode.has_thumbnail = MegaNode.hasThumbnail
MegaNode.has_preview = MegaNode.hasPreview
MegaNode.is_public = MegaNode.isPublic

MegaUser.get_email = MegaUser.getEmail
MegaUser.get_visibility = MegaUser.getVisibility
MegaUser.get_timestamp = MegaUser.getTimesamp

MegaShare.get_user = MegaShare.getUser
MegaShare.get_node_handle = MegaShare.getNodeHandle
MegaShare.get_access = MegaShare.getAccess
MegaShare.get_timestamp = MegaShare.getTimestamp

MegaRequest.get_type = MegaRequest.getType
MegaRequest.get_request_string = MegaRequest.getRequestString
MegaRequest.to_string = MegaRequest.toString
MegaRequest.get_node_handle = MegaRequest.getNodeHandle
MegaRequest.get_link = MegaRequest.getLink
MegaRequest.get_parent_handle = MegaRequest.getParentHandle
MegaRequest.get_session_key = MegaRequest.getSessionKey
MegaRequest.get_name = MegaRequest.getName
MegaRequest.get_email = MegaRequest.getEmail
MegaRequest.get_password = MegaRequest.getPassword
MegaRequest.get_new_password = MegaRequest.getNewPassword
MegaRequest.get_private_key = MegaRequest.getPrivateKey
MegaRequest.get_access = MegaRequest.getAccess
MegaRequest.get_file = MegaRequest.getFile
MegaRequest.get_num_retry = MegaRequest.getNumRetry
MegaRequest.get_public_node = MegaRequest.getPublicNode
MegaRequest.get_param_type = MegaRequest.getParamType
MegaRequest.get_text = MegaRequest.getText
MegaRequest.get_number = MegaRequest.getNumber
MegaRequest.get_flag = MegaRequest.getFlag
MegaRequest.get_transferred_bytes = MegaRequest.getTransferredBytes
MegaRequest.get_total_bytes = MegaRequest.getTotalBytes
MegaRequest.get_mega_account_details = MegaRequest.getMegaAccountDetails
MegaRequest.get_pricing = MegaRequest.getPricing
MegaRequest.get_transfer_tag = MegaRequest.getTransferTag
MegaRequest.get_num_details = MegaRequest.getNumDetails

MegaTransfer.get_type = MegaTransfer.getType
MegaTransfer.get_transfer_string = MegaTransfer.getTransferString
MegaTransfer.to_string = MegaTransfer.toString
MegaTransfer.get_start_time = MegaTransfer.getStartTime
MegaTransfer.get_transferred_bytes = MegaTransfer.getTransferredBytes
MegaTransfer.get_total_bytes = MegaTransfer.getTotalBytes
MegaTransfer.get_path = MegaTransfer.getPath
MegaTransfer.get_parent_handle = MegaTransfer.getParentHandle
MegaTransfer.get_node_handle = MegaTransfer.getNodeHandle
MegaTransfer.get_parent_path = MegaTransfer.getParentPath
MegaTransfer.get_start_pos = MegaTransfer.getStartPos
MegaTransfer.get_end_pos = MegaTransfer.getEndPos
MegaTransfer.get_file_name = MegaTransfer.getFileName
MegaTransfer.get_num_retry = MegaTransfer.getNumRetry
MegaTransfer.get_max_retries = MegaTransfer.getMaxRetries
MegaTransfer.get_tag = MegaTransfer.getTag
MegaTransfer.get_speed = MegaTransfer.getSpeed
MegaTransfer.get_delta_size = MegaTransfer.getDeltaSize
MegaTransfer.get_update_time = MegaTransfer.getUpdateTime
MegaTransfer.get_public_mega_node = MegaTransfer.getPublicMegaNode
MegaTransfer.is_sync_transfer = MegaTransfer.isSyncTransfer
MegaTransfer.is_streaming_transfer = MegaTransfer.isStreamingTransfer
MegaTransfer.get_last_bytes = MegaTransfer.getLastBytes

MegaContactRequest.get_handle = MegaContactRequest.getHandle
MegaContactRequest.get_source_email = MegaContactRequest.getSourceEmail
MegaContactRequest.get_source_message = MegaContactRequest.getSourceMessage
MegaContactRequest.get_target_email = MegaContactRequest.getTargetEmail
MegaContactRequest.get_creation_time = MegaContactRequest.getCreationTime
MegaContactRequest.get_modification_time = MegaContactRequest.getModificationTime
MegaContactRequest.get_status = MegaContactRequest.getStatus
MegaContactRequest.is_outgoing = MegaContactRequest.isOutgoing

MegaError.get_error_code = MegaError.getErrorCode
MegaError.to_string = MegaError.toString

MegaTreeProcessor.process_mega_node = MegaTreeProcessor.processMegaNode

MegaRequestListener.on_request_start = MegaRequestListener.onRequestStart
MegaRequestListener.on_request_finish = MegaRequestListener.onRequestFinish
MegaRequestListener.on_request_update = MegaRequestListener.onRequestUpdate
MegaRequestListener.on_request_temporary_error = MegaRequestListener.onRequestTemporaryError

MegaTransferListener.on_transfer_start = MegaTransferListener.onTransferStart
MegaTransferListener.on_transfer_finish = MegaTransferListener.onTransferFinish
MegaTransferListener.on_transfer_update = MegaTransferListener.onTransferUpdate
MegaTransferListener.on_transfer_temporary_error = MegaTransferListener.onTransferTemporaryError
MegaTransferListener.on_transfer_data = MegaTransferListener.onTransferData

MegaGlobalListener.on_users_update = MegaGlobalListener.onUsersUpdate
MegaGlobalListener.on_nodes_update = MegaGlobalListener.onNodesUpdate
MegaGlobalListener.on_account_update = MegaGlobalListener.onAccountUpdate
MegaGlobalListener.on_contact_requests_update = MegaGlobalListener.onContactRequestsUpdate
MegaGlobalListener.on_reload_needed = MegaGlobalListener.onReloadNeeded

MegaListener.on_request_start = MegaListener.onRequestStart
MegaListener.on_request_finish = MegaListener.onRequestFinish
MegaListener.on_request_update = MegaListener.onRequestUpdate
MegaListener.on_request_temporary_error = MegaListener.onRequestTemporaryError
MegaListener.on_transfer_start = MegaListener.onTransferStart
MegaListener.on_transfer_finish = MegaListener.onTransferFinish
MegaListener.on_transfer_update = MegaListener.onTransferUpdate
MegaListener.on_transfer_temporary_error = MegaListener.onTransferTemporaryError
MegaListener.on_users_update = MegaListener.onUsersUpdate
MegaListener.on_nodes_update = MegaListener.onNodesUpdate
MegaListener.on_account_update = MegaListener.onAccountUpdate
MegaListener.on_contact_requests_update = MegaListener.onContactRequestsUpdate
MegaListener.on_reload_needed = MegaListener.onReloadNeeded

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
MegaApi.are_transfers_paused = MegaApi.areTansfersPaused
MegaApi.set_upload_limit = MegaApi.setUploadLimit
MegaApi.set_download_method = MegaApi.setDownloadMethod
MegaApi.set_upload_method = MegaApi.setUploadMethod
MegaApi.get_download_method = MegaApi.getDownloadMethod
MegaApi.get_upload_method = MegaApi.getUploadMethod
MegaApi.get_transfer_by_tag = MegaApi.getTransferByTag
MegaApi.get_transfers = MegaApi.getTransfers
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
MegaApi.get_children = MegaApi.getChildren
MegaApi.get_index = MegaApi.getIndex
MegaApi.get_child_node = MegaApi.getChildNode
MegaApi.get_parent_node = MegaApi.getParentNode
MegaApi.get_node_path = MegaApi.getNodePath
MegaApi.get_node_by_path = MegaApi.getNodeByPath
MegaApi.get_node_by_handle = MegaApi.getNodeByHandle
MegaApi.get_contact_request_by_handle = MegaApi.getContactRequestByHandle
MegaApi.get_contacts = MegaApi.getContacts
MegaApi.get_contact = MegaApi.getContact
MegaApi.get_in_shares = MegaApi.getInShares
MegaApi.is_shared = MegaApi.isShared
MegaApi.get_out_shares = MegaApi.getOutShares
MegaApi.get_pending_out_shares = MegaApi.getPendingOutShares
MegaApi.get_incoming_contact_requests = MegaApi.getIncomingContactRequests
MegaApi.get_outgoing_contact_requests = MegaApi.getOutgoingContactRequests
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

MegaAccountBalance.get_amount = MegaAccountBalance.getAmount
MegaAccountBalance.get_currency = MegaAccountBalance.getCurrency

MegaAccountSession.get_creation_timestamp = MegaAccountSession.getCreationTimestamp
MegaAccountSession.get_most_recent_usage = MegaAccountSession.getMostRecentUsage
MegaAccountSession.get_user_agent = MegaAccountSession.getUserAgent
MegaAccountSession.get_ip = MegaAccountSession.getIP
MegaAccountSession.get_country = MegaAccountSession.getCountry
MegaAccountSession.is_current = MegaAccountSession.isCurrent
MegaAccountSession.is_alive = MegaAccountSession.isAlive
MegaAccountSession.get_handle = MegaAccountSession.getHandle

MegaAccountPurchase.get_timestamp = MegaAccountPurchase.getTimestamp
MegaAccountPurchase.get_handle = MegaAccountPurchase.getHandle
MegaAccountPurchase.get_currency = MegaAccountPurchase.getCurrency
MegaAccountPurchase.get_amount = MegaAccountPurchase.getAmount
MegaAccountPurchase.get_method = MegaAccountPurchase.getMethod

MegaAccountTransaction.get_timestamp = MegaAccountTransaction.getTimestamp
MegaAccountTransaction.get_handle = MegaAccountTransaction.getHandle
MegaAccountTransaction.get_currency = MegaAccountTransaction.getCurrency
MegaAccountTransaction.get_amount = MegaAccountTransaction.getAmount

MegaAccountDetails.get_pro_level = MegaAccountDetails.getProLevel
MegaAccountDetails.get_pro_expiration = MegaAccountDetails.getProExpiration
MegaAccountDetails.get_subscription_status = MegaAccountDetails.getSubscriptionStatus
MegaAccountDetails.get_subscription_renew_time = MegaAccountDetails.getSubscriptionRenewTime
MegaAccountDetails.get_subscription_method = MegaAccountDetails.getSubscriptionMethod
MegaAccountDetails.get_subscription_cycle = MegaAccountDetails.getSubscriptionCycle
MegaAccountDetails.get_storage_max = MegaAccountDetails.getStorageMax
MegaAccountDetails.get_transfer_max = MegaAccountDetails.getTransferMax
MegaAccountDetails.get_transfer_own_used = MegaAccountDetails.getTransferOwnUsed
MegaAccountDetails.get_num_usage_items = MegaAccountDetails.getNumUsageItems
MegaAccountDetails.get_storage_used = MegaAccountDetails.getStorageUsed
MegaAccountDetails.get_num_files = MegaAccountDetails.getNumFiles
MegaAccountDetails.get_num_folders = MegaAccountDetails.getNumFolders
MegaAccountDetails.get_num_balances = MegaAccountDetails.getNumBalances
MegaAccountDetails.get_balance = MegaAccountDetails.getBalance
MegaAccountDetails.get_num_sessions = MegaAccountDetails.getNumSessions
MegaAccountDetails.get_session = MegaAccountDetails.getSession
MegaAccountDetails.get_num_purchases = MegaAccountDetails.getNumPurchases
MegaAccountDetails.get_purchase = MegaAccountDetails.getPurchase
MegaAccountDetails.get_num_transactions = MegaAccountDetails.getNumTransactions
MegaAccountDetails.get_transaction = MegaAccountDetails.getTransaction

MegaPricing.get_num_products = MegaPricing.getNumProducts
MegaPricing.get_handle = MegaPricing.getHandle
MegaPricing.get_pro_level = MegaPricing.getProLevel
MegaPricing.get_gb_storage = MegaPricing.getGBStorage
MegaPricing.get_gb_transfer = MegaPricing.getGBTransfer
MegaPricing.get_months = MegaPricing.getMonths
MegaPricing.get_amount = MegaPricing.getAmount
MegaPricing.get_currency = MegaPricing.getCurrency
MegaPricing.get_description = MegaPricing.getDescription
MegaPricing.get_ios_id = MegaPricing.getIosID
MegaPricing.get_android_id = MegaPricing.getAndroidID

del MegaGfxProcessor.readBitmap
del MegaGfxProcessor.getWidth
del MegaGfxProcessor.getHeight
del MegaGfxProcessor.getBitmapDataSize
del MegaGfxProcessor.getBitmapData
del MegaGfxProcessor.freeBitmap 

del MegaProxy.setProxyType
del MegaProxy.setProxyURL
del MegaProxy.setCredentials
del MegaProxy.getProxyType
del MegaProxy.getProxyURL
del MegaProxy.credentialsNeeded
del MegaProxy.getUsername
del MegaProxy.getPassword

del MegaNode.getType
del MegaNode.getName
del MegaNode.getBase64Handle
del MegaNode.getSize
del MegaNode.getCreationTime
del MegaNode.getModificationTime
del MegaNode.getHandle
del MegaNode.getParentHandle
del MegaNode.getBase64Key
del MegaNode.getTag
del MegaNode.isFile
del MegaNode.isFolder
del MegaNode.isRemoved
del MegaNode.hasChanged
del MegaNode.getChanges
del MegaNode.hasThumbnail
del MegaNode.hasPreview
del MegaNode.isPublic

del MegaUser.getEmail
del MegaUser.getVisibility
del MegaUser.getTimesamp

del MegaShare.getUser
del MegaShare.getNodeHandle
del MegaShare.getAccess
del MegaShare.getTimestamp

del MegaRequest.getType
del MegaRequest.getRequestString
del MegaRequest.toString
del MegaRequest.getNodeHandle
del MegaRequest.getLink
del MegaRequest.getParentHandle
del MegaRequest.getSessionKey
del MegaRequest.getName
del MegaRequest.getEmail
del MegaRequest.getPassword
del MegaRequest.getNewPassword
del MegaRequest.getPrivateKey
del MegaRequest.getAccess
del MegaRequest.getFile
del MegaRequest.getNumRetry
del MegaRequest.getPublicNode
del MegaRequest.getParamType
del MegaRequest.getText
del MegaRequest.getNumber
del MegaRequest.getFlag
del MegaRequest.getTransferredBytes
del MegaRequest.getTotalBytes
del MegaRequest.getMegaAccountDetails
del MegaRequest.getPricing
del MegaRequest.getTransferTag
del MegaRequest.getNumDetails

del MegaTransfer.getType
del MegaTransfer.getTransferString
del MegaTransfer.toString
del MegaTransfer.getStartTime
del MegaTransfer.getTransferredBytes
del MegaTransfer.getTotalBytes
del MegaTransfer.getPath
del MegaTransfer.getParentHandle
del MegaTransfer.getNodeHandle
del MegaTransfer.getParentPath
del MegaTransfer.getStartPos
del MegaTransfer.getEndPos
del MegaTransfer.getFileName
del MegaTransfer.getNumRetry
del MegaTransfer.getMaxRetries
del MegaTransfer.getTag
del MegaTransfer.getSpeed
del MegaTransfer.getDeltaSize
del MegaTransfer.getUpdateTime
del MegaTransfer.getPublicMegaNode
del MegaTransfer.isSyncTransfer
del MegaTransfer.isStreamingTransfer
del MegaTransfer.getLastBytes

del MegaContactRequest.getHandle
del MegaContactRequest.getSourceEmail
del MegaContactRequest.getSourceMessage
del MegaContactRequest.getTargetEmail
del MegaContactRequest.getCreationTime
del MegaContactRequest.getModificationTime
del MegaContactRequest.getStatus
del MegaContactRequest.isOutgoing

del MegaError.getErrorCode
del MegaError.toString

del MegaTreeProcessor.processMegaNode

del MegaRequestListener.onRequestStart
del MegaRequestListener.onRequestFinish
del MegaRequestListener.onRequestUpdate
del MegaRequestListener.onRequestTemporaryError

del MegaTransferListener.onTransferStart
del MegaTransferListener.onTransferFinish
del MegaTransferListener.onTransferUpdate
del MegaTransferListener.onTransferTemporaryError
del MegaTransferListener.onTransferData

del MegaGlobalListener.onUsersUpdate
del MegaGlobalListener.onNodesUpdate
del MegaGlobalListener.onAccountUpdate
del MegaGlobalListener.onContactRequestsUpdate
del MegaGlobalListener.onReloadNeeded

del MegaListener.onRequestStart
del MegaListener.onRequestFinish
del MegaListener.onRequestUpdate
del MegaListener.onRequestTemporaryError
del MegaListener.onTransferStart
del MegaListener.onTransferFinish
del MegaListener.onTransferUpdate
del MegaListener.onTransferTemporaryError
del MegaListener.onUsersUpdate
del MegaListener.onNodesUpdate
del MegaListener.onAccountUpdate
del MegaListener.onContactRequestsUpdate
del MegaListener.onReloadNeeded

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
del MegaApi.areTansfersPaused
del MegaApi.setUploadLimit
del MegaApi.setDownloadMethod
del MegaApi.setUploadMethod
del MegaApi.getDownloadMethod
del MegaApi.getUploadMethod
del MegaApi.getTransferByTag
del MegaApi.getTransfers
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
del MegaApi.getChildren
del MegaApi.getIndex
del MegaApi.getChildNode
del MegaApi.getParentNode
del MegaApi.getNodePath
del MegaApi.getNodeByPath
del MegaApi.getNodeByHandle
del MegaApi.getContactRequestByHandle
del MegaApi.getContacts
del MegaApi.getContact
del MegaApi.getInShares
del MegaApi.isShared
del MegaApi.getOutShares
del MegaApi.getPendingOutShares
del MegaApi.getIncomingContactRequests
del MegaApi.getOutgoingContactRequests
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

del MegaAccountBalance.getAmount
del MegaAccountBalance.getCurrency

del MegaAccountSession.getCreationTimestamp
del MegaAccountSession.getMostRecentUsage
del MegaAccountSession.getUserAgent
del MegaAccountSession.getIP
del MegaAccountSession.getCountry
del MegaAccountSession.isCurrent
del MegaAccountSession.isAlive
del MegaAccountSession.getHandle

del MegaAccountPurchase.getTimestamp
del MegaAccountPurchase.getHandle
del MegaAccountPurchase.getCurrency
del MegaAccountPurchase.getAmount
del MegaAccountPurchase.getMethod

del MegaAccountTransaction.getTimestamp
del MegaAccountTransaction.getHandle
del MegaAccountTransaction.getCurrency
del MegaAccountTransaction.getAmount

del MegaAccountDetails.getProLevel
del MegaAccountDetails.getProExpiration
del MegaAccountDetails.getSubscriptionStatus
del MegaAccountDetails.getSubscriptionRenewTime
del MegaAccountDetails.getSubscriptionMethod
del MegaAccountDetails.getSubscriptionCycle
del MegaAccountDetails.getStorageMax
del MegaAccountDetails.getTransferMax
del MegaAccountDetails.getTransferOwnUsed
del MegaAccountDetails.getNumUsageItems
del MegaAccountDetails.getStorageUsed
del MegaAccountDetails.getNumFiles
del MegaAccountDetails.getNumFolders
del MegaAccountDetails.getNumBalances
del MegaAccountDetails.getBalance
del MegaAccountDetails.getNumSessions
del MegaAccountDetails.getSession
del MegaAccountDetails.getNumPurchases
del MegaAccountDetails.getPurchase
del MegaAccountDetails.getNumTransactions
del MegaAccountDetails.getTransaction

del MegaPricing.getNumProducts
del MegaPricing.getHandle
del MegaPricing.getProLevel
del MegaPricing.getGBStorage
del MegaPricing.getGBTransfer
del MegaPricing.getMonths
del MegaPricing.getAmount
del MegaPricing.getCurrency
del MegaPricing.getDescription
del MegaPricing.getIosID
del MegaPricing.getAndroidID
            
