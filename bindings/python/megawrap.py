#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Temporary name as SWIG auto-generated file name is mega.

import sys
import os
import logging
import time
import threading
import json
import getpass

_wrapper_dir = os.path.join(os.getcwd(), '..', '..', 'bindings', 'python')
_libs_dir = os.path.join(_wrapper_dir, '.libs')
_shared_lib = os.path.join(_libs_dir, '_mega.so')
if os.path.isdir(_wrapper_dir) and os.path.isfile(_shared_lib):
    sys.path.insert(0, _wrapper_dir)  # mega.py
    sys.path.insert(0, _libs_dir)     # _mega.so

import mega



class MegaApi(object):     
    ''' Allows to control a MEGA account or a shared folder.
    You must provide an appKey to use this SDK. You can generate an appKey for your app for free here:
    https://mega.co.nz/#sdk
    You can enable local node caching by passing a local path in the constructor of this class. That saves many data usage and many time starting your app because the entire filesystem won't have to  be    downloaded each time. The persistent node cache will only be loaded by logging in with a session key. To take advantage of this feature, apart of passing the local path to the constructor, your  application have to save the session key after login (MegaApi::dumpSession) and use it to log in the next time. This is highly recommended also to enhance the security, because in this was the access     password doesn't have to be stored by the application.
To access MEGA using this SDK, you have to create an object of this class and use one of the MegaApi::login options (to log in to a MEGA account or a public folder). If the login request succeed, you must call MegaApi::fetchNodes to get the filesystem in MEGA. After successfully completing that request, you can use all other functions, manage the files and start transfers.
After using MegaApi::logout you can reuse the same MegaApi object to log in to another MEGA account or a public folder. 
    '''    
    def __init__(self, a, b, c, d):
    	'''Constructor''' 
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.api = mega.MegaApi(self.a, self.b, self.c, self.d)
        
    def add_listener(self, *args):
    	'''Register a listener to receive all events (requests, transfers, global, 	synchronization)
        You can use MegaApi::removeListener to stop receiving events. 
        :param listener - Listener that will receive all events (requests, transfers, global, synchronization) 
        ''' 
        return mega.MegaApi.addListener(self.api, *args)

    def add_request_listener(self, *args):
    	'''Register a listener to receive all events about requests.
        You can use MegaApi::removeRequestListener to stop receiving events.
        :param listener - Listener that will receive all events about requests 
        ''' 
        return mega.MegaApi.addRequestListener(self.api, *args)
    
    def add_transfer_listener(self, *args):
    	'''Register a listener to receive all events about transfers.
        You can use MegaApi::removeTransferListener to stop receiving events.
        :param listener - Listener that will receive all events about transfers  
        ''' 
        return mega.MegaApi.addTransferListener(self.api, *args)
    
    def add_global_listener(self, *args):
    	'''Register a listener to receive global events. 
        You can use MegaApi::removeGlobalListener to stop receiving events.
        :param listener - Listener that will receive global events 
        ''' 
        return mega.MegaApi.addGlobalListener(self.api, *args)
    
    def remove_listener(self, *args):
    	'''Unregister a listener. 
        This listener won't receive more events.
        :param listener - Object that is unregistered 
        '''  
        return mega.MegaApi.removeListener(self.api, *args)
    
    def remove_request_listener(self, *args):
    	'''Unregister a MegaRequest listener.
		This listener won't receive any more requests.
		:param listener - Object that is unregistered.
		''' 
        return mega.MegaApi.removeRequestListener(self.api, *args)
    
    def remove_transfer_listener(self, *args):
    	'''Unregister a MegaTransferListener. 
        This listener won't receive more events.
        :param listener - Object that is unregistered 
        ''' 
        return mega.MegaApi.removeTransferListener(self.api, *args)
    
    def remove_global_listener(self, *args):
    	'''Unregister a MegaGlobalListener.
		This listener won't receive more events.
		''' 
        return mega.MegaApi.removeGlobalListener(self.api, *args)
    
    def get_current_request(self): 
    	'''need clarification'''
        return mega.MegaApi.getCurrentRequest(self.api)
    
    def get_current_transfer(self):
    	'''need clarification''' 
        return mega.MegaApi.getCurrentTransfer(self.api)
    
    def get_current_error(self):
    	'''need clarification''' 
        return mega.MegaApi.getCurrentError(self.api)
    
    def get_current_nodes(self):
    	'''need clarification''' 
        return mega.MegaApi.getCurrentNodes(self.api)
    
    def get_current_users(self):
    	'''need clarification''' 
        return mega.MegaApi.getCurrentUsers(self.api)
    
    def get_base64_pw_key(self, *args):
    	'''Generates a private key based on the access password. This is a time consuming operation (specially for low-end mobile devices).  Since the resulting key is required to log in, this function   allows to do this step in a separate function. You should run this function in a background thread, to prevent UI hangs. The resulting key can be used in MegaApi::fastLogin. 
        You take the ownership of the returned value. 
        :param password - Access password 
        :Returns - Base64-encoded private key 
        ''' 
        return mega.MegaApi.getBase64PwKey(self.api, *args)
    
    def get_string_hash(self, *args):
    	'''Generates a hash based in the provided private key and email.
This is a time consuming operation (specially for low-end mobile devices). Since the resulting key is required to log in, this function allows to do this step in a separate function. You should run this function in a background thread, to prevent UI hangs. The resulting key can be used in MegaApi::fastLogin
        You take the ownership of the returned value.
        :param base64pwkey- Private key returned by MegaApi::getBase64PwKey
        :param email - Email to create the hash 
        :Returns - Base64-encoded hash
        ''' 
        return mega.MegaApi.getStringHash(self.api, *args)
    
    def get_session_transfer_URL(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.getSessionTransferURL(self.api, *args)
    
    def retry_pending_connections(self, disconnect=False, includexfers=False, listener=None):
    	'''Retry all pending requests.
		When requests fails they wait some time before being retried. That delay grows exponentially if the request fails again. For this reason, and since this request is very lightweight, it's recommended to call it with the default parameters on every user interaction with the application. This will prevent very big delays completing requests.
		The associated request type with this request is MegaRequest::TYPE_RETRY_PENDING_CONNECTIONS. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest::getFlag - Returns the first parameter
    		MegaRequest::getNumber - Returns the second parameter
		:param disconnect -true if you want to disconnect already connected requests It's not recommended to set this flag to true if you are not fully sure about what are you doing. If you send a request that needs some time to complete and you disconnect it in a loop without giving it enough time, it could be retrying forever.
		:param includexfers - true to retry also transfers It's not recommended to set this flag. Transfer has a retry counter and are aborted after a number of retries MegaTransfer::getMaxRetries. Setting this flag to true, you will force more immediate retries and your transfers could fail faster.
		:param listener - MegaRequestListener to track this request 
       	''' 
        return mega.MegaApi.retryPendingConnections(self.api, disconnect, includexfers, listener)
    
    def login(self, *args):
    	'''Log in to a MEGA account.
		The associated request type with this request is MegaRequest::TYPE_LOGIN. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest::getEmail - Returns the first parameter
    		MegaRequest::getPassword - Returns the second parameter
		If the email/password aren't valid the error code provided in onRequestFinish is MegaError::API_ENOENT.
        :param email -Email of the user
        :param password - Password  
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.login(self.api, *args)
    
    def login_to_folder(self, *args):
    	'''Log in to a public folder using a folder link.
		After a successful login, you should call MegaApi::fetchNodes to get filesystem and start working with the folder.
		The associated request type with this request is MegaRequest::TYPE_LOGIN. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest::getEmail - Retuns the string "FOLDER"
    		MegaRequest::getLink - Returns the public link to the folder
		:param megaFolderLink - Public link to a folder in MEGA
    	:param listener - MegaRequestListener to track this request        
        ''' 
        return mega.MegaApi.loginToFolder(self.api, *args)
    
    def fast_login(self, *args):
    	'''Initialize the creation of a new MEGA account with precomputed keys.
	The associated request type with this request is MegaRequest::TYPE_CREATE_ACCOUNT. Valid data in the MegaRequest object received on callbacks:
    		MegaRequest::getEmail - Returns the email for the account
		MegaRequest::getPrivateKey - Returns the private key calculated with 			MegaApi::getBase64PwKey
    		MegaRequest::getName - Returns the name of the user
	If this request succeed, a confirmation email will be sent to the users. If an account with the same email already exists, you will get the error code MegaError::API_EEXIST in onRequestFinish
    	:param email - Email for the account
    	:param base64pwkey	- Private key calculated with MegaApi::getBase64PwKey
    	:param name - Name of the user
    	:param listener - MegaRequestListener to track this request     
        ''' 
        return mega.MegaApi.fastLogin(self.api, *args)
    
    def kill_session(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.killSession(self.api, *args)
    
    def get_user_data(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.getUserData(self.api, *args)
    
    def dump_session(self):
    	'''Returns the current session key.
        You have to be logged in to get a valid session key. Otherwise, this function returns NULL.
        You take the ownership of the returned value.
        :Returns current session key   
        ''' 
        return mega.MegaApi.dumpSession(self.api)
    
    def dump_XMPP_session(self):
    	'''need clarification''' 
        return mega.MegaApi.dumpXMPPSession(self.api)
    
    def create_account(self, *args):
    	'''Initialize the creation of a new MEGA account.
        The associated request type with this request is MegaRequest::TYPE_CREATE_ACCOUNT. Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getEmail - Returns the email for the account
            MegaRequest::getPassword - Returns the password for the account
            MegaRequest::getName - Returns the name of the user
        If this request succeed, a confirmation email will be sent to the users. If an account with the same email already exists, you will get the error code MegaError::API_EEXIST in onRequestFinish
        :param email - Email for the account
        :param password - Password for the account
        :param name - Name of the user
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.createAccount(self.api, *args)
    
    def fast_create_account(self, *args):
    	'''Initialize the creation of a new MEGA account with precomputed keys.
        The associated request type with this request is MegaRequest::TYPE_CREATE_ACCOUNT. Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getEmail - Returns the email for the account
            MegaRequest::getPrivateKey - Returns the private key calculated with MegaApi::getBase64PwKey
            MegaRequest::getName - Returns the name of the user
        If this request succeed, a confirmation email will be sent to the users. If an account with the same email already exists, you will get the error code MegaError::API_EEXIST in onRequestFinish
        :param email - Email for the account
        :param base64pwkey - Private key calculated with MegaApi::getBase64PwKey
        :param name - Name of the user
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.fastCreateAccount(self.api, *args)
    
    def query_signup_link(self, *args): 
    	'''Get information about a confirmation link.
        The associated request type with this request is MegaRequest::TYPE_QUERY_SIGNUP_LINK. Valid data in the MegaRequest object received on all callbacks:
            MegaRequest::getLink - Returns the confirmation link
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getEmail - Return the email associated with the confirmation link
            MegaRequest::getName - Returns the name associated with the confirmation link
        :param link - Confirmation link
        :param listener - MegaRequestListener to track this request    
        '''
        return mega.MegaApi.querySignupLink(self.api, *args)
    
    def confirm_account(self, *args):
    	'''Confirm a MEGA account using a confirmation link and the user password.
        The associated request type with this request is MegaRequest::TYPE_CONFIRM_ACCOUNT Valid data in the MegaRequest object received on callbacks:
        MegaRequest::getLink - Returns the confirmation link
        MegaRequest::getPassword - Returns the password
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getEmail - Email of the account
            MegaRequest::getName - Name of the user
        :param link - Confirmation link
        :param password - Password of the account
        :param listener - MegaRequestListener to track this request        
        ''' 
        return mega.MegaApi.confirmAccount(self.api, *args)
    
    def fast_confirm_account(self, *args): 
    	'''Confirm a MEGA account using a confirmation link and a precomputed key.
        The associated request type with this request is MegaRequest::TYPE_CONFIRM_ACCOUNT Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getLink - Returns the confirmation link
            MegaRequest::getPrivateKey - Returns the base64pwkey parameter
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getEmail - Email of the account
            MegaRequest::getName - Name of the user
        :param link - Confirmation link
        :param base64pwkey - Private key precomputed with MegaApi::getBase64PwKey
        :param listener - MegaRequestListener to track this request         
        '''
        return mega.MegaApi.fastConfirmAccount(self.api, *args)
    
    def set_proxy_settings(self, *args):
    	'''Set proxy settings.
        The SDK will start using the provided proxy settings as soon as this function returns.
        :param proxySettings - Proxy settings 
        ''' 
        return mega.MegaApi.setProxySettings(self.api, *args)
    
    def get_auto_proxy_settings(self):
    	'''Try to detect the system's proxy settings.
        Automatic proxy detection is currently supported on Windows only. On other platforms, this fuction will return a MegaProxy object of type MegaProxy::PROXY_NONE
        You take the ownership of the returned value.
        :param Returns MegaProxy object with the detected proxy settings.
        ''' 
        return mega.MegaApi.getAutoProxySettings(self.api)
    
    def is_logged_in(self):
    	'''Check if the MegaApi object is logged in.
        :Returns 0 if not logged in, else a number >= 0
        ''' 
        return mega.MegaApi.isLoggedIn(self.api)
    
    def get_my_email(self):
    	'''Retuns the email of the currently open account.
        If the MegaApi object isn't logged in or the email isn't available, this function returns None
        You take the ownership of the returned value
        :Returns Email of the account
        ''' 
        return mega.MegaApi.getMyEmail(self.api)
    
    def get_my_user_handle(self):
    	'''need clarification''' 
        return mega.MegaApi.getMyUserHandle(self.api)
    
    def create_folder(self, *args):
    	'''Create a folder in the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_CREATE_FOLDER Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getParentHandle - Returns the handle of the parent folder
            MegaRequest::getName - Returns the name of the new folder
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getNodeHandle - Handle of the new folder
        :param name - Name of the new folder
        :param parent - Parent folder
        :param listener - MegaRequestListener to track this request         
        ''' 
        return mega.MegaApi.createFolder(self.api, *args)
    
    def move_node(self, *args):
    	'''Move a node in the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_MOVE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node to move
            MegaRequest::getParentHandle - Returns the handle of the new parent for the node
        :param node - Node to move
        :param newParent - New parent for the node
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.moveNode(self.api, *args)
    
    def copy_node(self, *args):
    	'''Copy a node in the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node to copy
            MegaRequest::getParentHandle - Returns the handle of the new parent for the new node
            MegaRequest::getPublicMegaNode - Returns the node to copy (if it is a public node)
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getNodeHandle - Handle of the new node
        :param node - Node to copy
        :param newParent - Parent for the new node
        :param listener - MegaRequestListener to track this request        
        ''' 
        return mega.MegaApi.copyNode(self.api, *args)
    
    def rename_node(self, *args): 
    	'''Rename a node in the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_RENAME Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node to rename
            MegaRequest::getName - Returns the new name for the node
        :param node - Node to modify
        :param newName - New name for the node
        :param listener - MegaRequestListener to track this request     
        '''
        return mega.MegaApi.renameNode(self.api, *args)
    
    def remove(self, *args): 
    	'''Remove a node from the MEGA account.
        This function doesn't move the node to the Rubbish Bin, it fully removes the node. To move the node to the Rubbish Bin use MegaApi::moveNode
        The associated request type with this request is MegaRequest::TYPE_REMOVE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node to remove
        :param node - Node to remove
        :param listener - MegaRequestListener to track this request         
        '''
        return mega.MegaApi.remove(self.api, *args)
    
    def send_file_to_user(self, *args): 
    	'''Send a node to the Inbox of another MEGA user using a MegaUser.
        The associated request type with this request is MegaRequest::TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node to send
            MegaRequest::getEmail - Returns the email of the user that receives the node
        :param node - Node to send
        :param user - User that receives the node
        :param listener - MegaRequestListener to track this request        
        '''
        return mega.MegaApi.sendFileToUser(self.api, *args)
    
    def share(self, *args):
    	'''Share or stop sharing a folder in MEGA with another user using a MegaUser.
        To share a folder with an user, set the desired access level in the level parameter. If you want to stop sharing a folder use the access level MegaShare::ACCESS_UNKNOWN
        The associated request type with this request is MegaRequest::TYPE_COPY Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the folder to share
            MegaRequest::getEmail - Returns the email of the user that receives the shared folder
            MegaRequest::getAccess - Returns the access that is granted to the user
        :param node - The folder to share. It must be a non-root folder
        :param user - User that receives the shared folder
        :param level - Permissions that are granted to the user Valid values for this parameter:
            MegaShare::ACCESS_UNKNOWN = -1 Stop sharing a folder with this user
            MegaShare::ACCESS_READ = 0
            MegaShare::ACCESS_READWRITE = 1
            MegaShare::ACCESS_FULL = 2
            MegaShare::ACCESS_OWNER = 3
        :param listener - MegaRequestListener to track this request         
        ''' 
        return mega.MegaApi.share(self.api, *args)
    
    def import_file_link(self, *args):
    	'''Import a public link to the account.
        The associated request type with this request is MegaRequest::TYPE_IMPORT_LINK Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getLink - Returns the public link to the file
            MegaRequest::getParentHandle - Returns the folder that receives the imported file
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getNodeHandle - Handle of the new node in the account
        :param megaFileLink - Public link to a file in MEGA
        :param parent - Parent folder for the imported file
        :param listener - MegaRequestListener to track this request         
        ''' 
        return mega.MegaApi.importFileLink(self.api, *args)
    
    def get_public_node(self, *args):
    	'''Get a MegaNode from a public link to a file.
        A public node can be imported using MegaApi::copyNode or downloaded using MegaApi::startDownload
        The associated request type with this request is MegaRequest::TYPE_GET_PUBLIC_NODE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getLink - Returns the public link to the file
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getPublicMegaNode - Public MegaNode corresponding to the public link
        :param megaFileLink - Public link to a file in MEGA
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.getPublicNode(self.api, *args)
    
    def get_thumbnail(self, *args):
    	'''Get the thumbnail of a node.
        If the node doesn't have a thumbnail the request fails with the MegaError::API_ENOENT error code
        The associated request type with this request is MegaRequest::TYPE_GET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getFile - Returns the destination path
            MegaRequest::getParamType - Returns MegaApi::ATTR_TYPE_THUMBNAIL
        :param node - Node to get the thumbnail
        :param dstFilePath - Destination path for the thumbnail. If this path is a local folder, it must end with a '\' or '/' character and (Base64-encoded handle + "0.jpg") will be used as the file name inside that folder. If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.getThumbnail(self.api, *args)
    
    def get_preview(self, *args):
    	'''Get the preview of a node.
        If the node doesn't have a preview the request fails with the MegaError::API_ENOENT error code
        The associated request type with this request is MegaRequest::TYPE_GET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getFile - Returns the destination path
            MegaRequest::getParamType - Returns MegaApi::ATTR_TYPE_PREVIEW
        :param node - Node to get the preview
        :param dstFilePath - Destination path for the preview. If this path is a local folder, it must end with a '\' or '/' character and (Base64-encoded handle + "1.jpg") will be used as the file name inside that folder. If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        :param listener - MegaRequestListener to track this request         
        ''' 
        return mega.MegaApi.getPreview(self.api, *args)
    
    def get_user_avatar(self, *args):
    	'''Get the avatar of a MegaUser.
        The associated request type with this request is MegaRequest::TYPE_GET_ATTR_USER Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getFile - Returns the destination path
            MegaRequest::getEmail - Returns the email of the user
        :param user - MegaUser to get the avatar
        :param dstFilePath - Destination path for the avatar. It has to be a path to a file, not to a folder. If this path is a local folder, it must end with a '\' or '/' character and (email + "0.jpg") will be used as the file name inside that folder. If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        :param listener - MegaRequestListener to track this request        
        ''' 
        return mega.MegaApi.getUserAvatar(self.api, *args)
    
    def get_user_attribute(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.getUserAttribute(self.api, *args)
    
    def cancel_get_thumbnail(self, *args):
    	'''Cancel the retrieval of a thumbnail.
        The associated request type with this request is MegaRequest::TYPE_CANCEL_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getParamType - Returns MegaApi::ATTR_TYPE_THUMBNAIL
        :param node - Node to cancel the retrieval of the preview
        :param listener - listener	MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.cancelGetThumbnail(self.api, *args)
    
    def cancel_get_preview(self, *args):
    	'''Cancel the retrieval of a preview.
        The associated request type with this request is MegaRequest::TYPE_CANCEL_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getParamType - Returns MegaApi::ATTR_TYPE_PREVIEW
        :param node - Node to cancel the retrieval of the preview
        :param listener - listener	MegaRequestListener to track this request       
        ''' 
        return mega.MegaApi.cancelGetPreview(self.api, *args)
    
    def set_thumbnail(self, *args):
    	'''Set the thumbnail of a MegaNode.
        The associated request type with this request is MegaRequest::TYPE_SET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getFile - Returns the source path
            MegaRequest::getParamType - Returns MegaApi::ATTR_TYPE_THUMBNAIL
        :param node - MegaNode to set the thumbnail
        :param srcFilePath - Source path of the file that will be set as thumbnail 
        :param listener - MegaRequestListener to track this request        
        ''' 
        return mega.MegaApi.setThumbnail(self.api, *args)
    
    def set_preview(self, *args):
    	'''Set the preview of a MegaNode.
        The associated request type with this request is MegaRequest::TYPE_SET_ATTR_FILE Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getFile - Returns the source path
            MegaRequest::getParamType - Returns MegaApi::ATTR_TYPE_PREVIEW
        :param node - MegaNode to set the preview
        :param srcFilePath - Source path of the file that will be set as preview 
        :param listener - MegaRequestListener to track this request
        ''' 
        return mega.MegaApi.setPreview(self.api, *args)
    
    def set_avatar(self, *args):
    	'''Set the avatar of the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_SET_ATTR_USER Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getFile - Returns the source path
        :param srcFilePath - Source path of the file that will be set as avatar 
        :param listener - MegaRequestListener to track this request
        ''' 
        return mega.MegaApi.setAvatar(self.api, *args)
    
    def set_user_attribute(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.setUserAttribute(self.api, *args)
    
    def export_node(self, *args):
    	'''Generate a public link of a file/folder in MEGA.
        The associated request type with this request is MegaRequest::TYPE_EXPORT Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getAccess - Returns true
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getLink - Public link
        :param node - MegaNode to get the public link
        :param listener - MegaRequestListener to track this request        
        ''' 
        return mega.MegaApi.exportNode(self.api, *args)
    
    def disable_export(self, *args):
    	'''Stop sharing a file/folder.
        The associated request type with this request is MegaRequest::TYPE_EXPORT Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getNodeHandle - Returns the handle of the node
            MegaRequest::getAccess - Returns false
        :param node - MegaNode to stop sharing
        :param listener - MegaRequestListener to track this request
        ''' 
        return mega.MegaApi.disableExport(self.api, *args)
    
    def fetch_nodes(self, listener=None): 
    	'''Fetch the filesystem in MEGA.
        The MegaApi object must be logged in in an account or a public folder to successfully complete this request.
        The associated request type with this request is MegaRequest::TYPE_FETCH_NODES
        :param listener - MegaRequestListener to track this request       
        '''
        return mega.MegaApi.fetchNodes(self.api, listener)
    
    def get_account_details(self, listener=None):
    	'''Get details about the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_ACCOUNT_DETAILS
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getMegaAccountDetails - Details of the MEGA account
        :param listener - MegaRequestListener to track this request
        ''' 
        return mega.MegaApi.getAccountDetails(self.api, listener)
    
    def get_extendedAccount_details(self, sessions=False, purchases=False, transactions=False, listener=None):
    	'''need clarification''' 
        return mega.MegaApi.getExtendedAccountDetails(self.api, sessions, purchases, transactions, listener)
    
    def get_pricing(self, listener=None):
    	'''Get the available pricing plans to upgrade a MEGA account.
        You can get a payment URL for any of the pricing plans provided by this function using MegaApi::getPaymentUrl
        The associated request type with this request is MegaRequest::TYPE_GET_PRICING
        Valid data in the MegaRequest object received in onRequestFinish when the error code is MegaError::API_OK:
            MegaRequest::getPricing - MegaPricing object with all pricing plans
        :param listener - MegaRequestListener to track this request
        ''' 
        return mega.MegaApi.getPricing(self.api, listener)
    
    def get_payment_id(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.getPaymentId(self.api, *args)
    
    def upgrade_account(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.upgradeAccount(self.api, *args)
    
    def submit_purchase_receipt(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.submitPurchaseReceipt(self.api, *args)
    
    def credit_card_store(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.creditCardStore(self.api, *args)
    
    def credit_card_query_subscriptions(self, listener=None):
    	'''need clarification''' 
        return mega.MegaApi.creditCardQuerySubscriptions(self.api, listener)
    
    def credit_card_cancel_subscriptions(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.creditCardCancelSubscriptions(self.api, *args)
    
    def get_payment_methods(self, listener=None): 
    	'''need clarification'''
        return mega.MegaApi.getPaymentMethods(self.api, listener)
    
    def export_master_key(self): 
    	'''Export the master key of the account.
        The returned value is a Base64-encoded string
        With the master key, it's possible to start the recovery of an account when the password is lost:
            https://mega.co.nz/#recovery
        You take the ownership of the returned value.
        :Returns Base64-encoded master key
        '''
        return mega.MegaApi.exportMasterKey(self.api)
    
    def change_password(self, *args):
    	'''Change the password of the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_CHANGE_PW Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getPassword - Returns the old password
            MegaRequest::getNewPassword - Returns the new password
        :param oldPassword - old password
        :param newPassword - new password
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.changePassword(self.api, *args)
    
    def add_contact(self, *args):
    	'''Add a new contact to the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_ADD_CONTACT Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getEmail - Returns the email of the contact
        :param email - Email of the new contact
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.addContact(self.api, *args)
    
    def invite_contact(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.inviteContact(self.api, *args)
    
    def reply_contact_request(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.replyContactRequest(self.api, *args)
    
    def remove_contact(self, *args):
    	'''Remove a contact to the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_REMOVE_CONTACT Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getEmail - Returns the email of the contact
        :param user - 	MegaUser of the contact (see MegaApi::getContact) 
        :param listener - MegaRequestListener to track this request
        ''' 
        return mega.MegaApi.removeContact(self.api, *args)
    
    def logout(self, listener=None):
    	'''Logout of the MEGA account.
        The associated request type with this request is MegaRequest::TYPE_LOGOUT 
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.logout(self.api, listener)
    
    def local_logout(self, listener=None):
    	'''need clarification''' 
        return mega.MegaApi.localLogout(self.api, listener)
    
    def submit_feedback(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.submitFeedback(self.api, *args)
    
    def report_debug_event(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.reportDebugEvent(self.api, *args)
    
    def start_upload(self, *args):
    	'''Upload a file. 
        :param localPath - Local path of the file 
        :param parent - Parent node for the file in the MEGA account
        :param listener - MegaTransferListener to track this transfer 
        ''' 
        return mega.MegaApi.startUpload(self.api, *args)
    
    def start_download(self, *args):
    	'''Download a file from MEGA.
        :param node - MegaNode that identifies the file 
        :param localPath - Destination path for the file If this path is a local folder, it must end with a '\' or '/' character and the file name in MEGA will be used to store a file inside that folder. If the path doesn't finish with one of these characters, the file will be downloaded to a file in that path.
        :param listener - MegaTransferListener to track this transfer 
        ''' 
        return mega.MegaApi.startDownload(self.api, *args)
    
    def start_streaming(self, *args):
    	'''Start an streaming download. 
        Streaming downloads don't save the downloaded data into a local file. It is provided in MegaTransferListener::onTransferUpdate in a byte buffer. 
        Only the MegaTransferListener passed to this function will receive MegaTransferListener::onTransferData callbacks. MegaTransferListener objects registered with MegaApi::addTransferListener won't receive them for performance reasons
        :param node - MegaNode that identifies the file (public nodes aren't supported yet)
        :param startPos - First byte to download from the file
        :param size - Size of the data to download
        :param listener - MegaTransferListener to track this transfer 
        ''' 
        return mega.MegaApi.startStreaming(self.api, *args)
    
    def cancel_transfer(self, *args): 
    	'''Cancel a transfer.
        When a transfer is cancelled, it will finish and will provide the error code MegaError::API_EINCOMPLETE in MegaTransferListener::onTransferFinish and MegaListener::onTransferFinish
        The associated request type with this request is MegaRequest::TYPE_CANCEL_TRANSFER Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getTransferTag - Returns the tag of the cancelled transfer (MegaTransfer::getTag)
        :param transfer - MegaTransfer object that identifies the transfer You can get this object in any MegaTransferListener callback or any MegaListener callback related to transfers.
        :param listener - MegaRequestListener to track this request 
        '''
        return mega.MegaApi.cancelTransfer(self.api, *args)
    
    def cancel_transfer_by_tag(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.cancelTransferByTag(self.api, *args)
    
    def cancel_transfers(self, *args):
    	'''Cancel all transfers of the same type.
        The associated request type with this request is MegaRequest::TYPE_CANCEL_TRANSFERS Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getParamType - Returns the first parameter
        :param type - 	Type of transfers to cancel. Valid values are:
            MegaTransfer::TYPE_DOWNLOAD = 0
            MegaTransfer::TYPE_UPLOAD = 1
        :param listener - MegaRequestListener to track this request 
        ''' 
        return mega.MegaApi.cancelTransfers(self.api, *args)
    
    def pause_transfers(self, *args): 
    	'''Pause/resume all transfers.
        The associated request type with this request is MegaRequest::TYPE_PAUSE_TRANSFERS Valid data in the MegaRequest object received on callbacks:
            MegaRequest::getFlag - Returns the first parameter
        :param pause - True to pause all transfers or False to resume all transfers
        :param listener - MegaRequestListener to track this request        
        '''
        return mega.MegaApi.pauseTransfers(self.api, *args)
    
    def are_tansfers_paused(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.areTansfersPaused(self.api, *args)
    
    def set_upload_limit(self, *args):
    	'''Set the upload speed limit.
        The limit will be applied on the server side when starting a transfer. Thus the limit won't be applied for already started uploads and it's applied per storage server.
        :param bpslimit - -1 to automatically select the limit, 0 for no limit, otherwise the speed limit in bytes per second 
        ''' 
        return mega.MegaApi.setUploadLimit(self.api, *args)
    
    def set_download_method(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.setDownloadMethod(self.api, *args)
    
    def set_upload_method(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.setUploadMethod(self.api, *args)
    
    def get_download_method(self):
    	'''need clarification''' 
        return mega.MegaApi.getDownloadMethod(self.api)
    
    def get_upload_method(self): 
    	'''need clarification'''
        return mega.MegaApi.getUploadMethod(self.api)
    
    def get_transfer_by_tag(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.getTransferByTag(self.api, *args)
    
    def get_transfers(self, *args): 
    	'''Get all active transfers.
		You take the ownership of the returned value
		:Returns list with all active transfers 
		'''
        return mega.MegaApi.getTransfers(self.api, *args)
    
    def update(self): 
    	'''Force a loop of the SDK thread.'''
        return mega.MegaApi.update(self.api)
    
    def is_waiting(self): 
    	'''Check if the SDK is waiting for the server.
		:Returns true if the SDK is waiting for the server to complete a request 
		'''
        return mega.MegaApi.isWaiting(self.api)
    
    def get_num_pending_uploads(self):
    	'''Get the number of pending uploads.
		:Returns the number of pending uploads.
		''' 
        return mega.MegaApi.getNumPendingUploads(self.api)
    
    def get_num_pending_downloads(self):
    	'''Get the number of pending downloads.
		:Returns the number of pending downloads.
		''' 
        return mega.MegaApi.getNumPendingDownloads(self.api)
    
    def get_total_uploads(self):
    	'''Get the number of queued uploads since the last call to MegaApi::resetTotalUploads.
		:Returns number of queued uploads since the last call to MegaApi::resetTotalUploads
		''' 
        return mega.MegaApi.getTotalUploads(self.api)
    
    def get_total_downloads(self):
    	'''Get the number of queued uploads since the last call to MegaApi::resetTotalDownloads.
		:Returns number of queued uploads since the last call to MegaApi::resetTotalDownloads
		''' 
        return mega.MegaApi.getTotalDownloads(self.api)
    
    def reset_total_downloads(self):
    	'''Reset the number of total downloads This function resets the number returned by MegaApi::getTotalDownloads.
		''' 
        return mega.MegaApi.resetTotalDownloads(self.api)
    
    def reset_total_uploads(self):
    	'''Reset the number of total uploads This function resets the number returned by MegaApi::getTotalUploads.
		''' 
        return mega.MegaApi.resetTotalUploads(self.api)
    
    def get_total_downloaded_bytes(self):
    	'''Get the total downloaded bytes since the creation of the MegaApi object.
		:Returns total downloaded bytes since the creation of the MegaApi object
		''' 
        return mega.MegaApi.getTotalDownloadedBytes(self.api)
    
    def getTotalUploadedBytes(self):
    	'''Get the total uploaded bytes since the creation of the MegaApi object.
		:Returns total uploaded bytes since the creation of the MegaApi object
		''' 
        return mega.MegaApi.getTotalUploadedBytes(self.api)
    
    def updateStats(self):
    	'''Force a loop of the SDK thread. ''' 
        return mega.MegaApi.updateStats(self.api)
    
    def get_num_children(self, *args):
    	'''Get the number of child nodes.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child nodes.
        :param parent - Parent node 
        :Returns Number of child nodes
        ''' 
        return mega.MegaApi.getNumChildren(self.api, *args)
    
    def get_num_child_files(self, *args):
    	'''Get the number of child files of a node.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child files.
        :parent parent - Parent node 
        :Returns Number of child files
        ''' 
        return mega.MegaApi.getNumChildFiles(self.api, *args)
    
    def get_num_child_folders(self, *args):
    	'''Get the number of child folders of a node.
        If the node doesn't exist in MEGA or isn't a folder, this function returns 0
        This function doesn't search recursively, only returns the direct child folders.
        :param parent - Parent node 
        :Returns Number of child folders
        ''' 
        return mega.MegaApi.getNumChildFolders(self.api, *args)
    
    def get_children(self, *args):
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
        ''' 
        return mega.MegaApi.getChildren(self.api, *args)
    
    def get_index(self, *args):
    	'''Get the current index of the node in the parent folder for a specific sorting order.
        If the node doesn't exist or it doesn't have a parent node (because it's a root node) this function returns -1 
        :param node - Node to check
        :param order - Sorting order to use
        :Returns index of the node in its parent folder
        ''' 
        return mega.MegaApi.getIndex(self.api, *args)
    
    def get_child_node(self, *args):
    	'''Get the child node with the provided name.
        If the node doesn't exist, this function returns None
        You take the ownership of the returned value
        :param parent - Parent node
        :param name - name of the node
        :Returns The MegaNode that has the selected parent and name
        ''' 
        return mega.MegaApi.getChildNode(self.api, *args)
    
    def get_parent_node(self, *args):
    	'''Get the parent node of a MegaNode.
        If the node doesn't exist in the account or it is a root node, this function returns NULL
        You take the ownership of the returned value.
        :param node - MegaNode to get the parent
        :Returns the parent of the provided node  
        ''' 
        return mega.MegaApi.getParentNode(self, *args)
    
    def get_node_path(self, *args): 
    	'''Get the path of a MegaNode.
        If the node doesn't exist, this function returns NULL. You can recoved the node later using MegaApi::getNodeByPath except if the path contains names with '/', '\' or ':' characters.
        You take the ownership of the returned value
        :param node - MegaNode for which the path will be returned 
        :Returns the path of the node 
        '''
        return mega.MegaApi.getNodePath(self.api, *args)
    
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
        return mega.MegaApi.getNodeByPath(self.api, *args)
    
    def get_node_by_handle(self, *args):
    	'''Get the MegaNode that has a specific handle. 
        You can get the handle of a MegaNode using MegaNode::getHandle. The same handle can be got in a Base64-encoded string using MegaNode::getBase64Handle. Conversions between these formats can be done using MegaApi::base64ToHandle and MegaApi::handleToBase64.
        It is needed to be logged in and to have successfully completed a fetchNodes request before calling this function. Otherwise, it will return None.
        You take the ownership of the returned value.
        :param MegaHandler - Node handle to check 
        :Returns MegaNode object with the handle, otherwise None
        ''' 
        return mega.MegaApi.getNodeByHandle(self.api, *args)
    
    def get_contact_request_by_handle(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.getContactRequestByHandle(self.api, *args)
    
    def get_contacts(self): 
    	'''Get all contacts of this MEGA account.
        You take the ownership of the returned value
        :Returns List of MegaUser object with all contacts of this account 
        '''
        return mega.MegaApi.getContacts(self.api)
    
    def get_contact(self, *args): 
    	'''Get the MegaUser that has a specific email address.
        You can get the email of a MegaUser using MegaUser::getEmail
        You take the ownership of the returned value
        :param email - Email address to check 
        :Returns MegaUser that has the email address, otherwise None 
        '''
        return mega.MegaApi.getContact(self.api, *args)
    
    def get_in_shares(self, *args):
    	'''Get a list with all inbound sharings from one MegaUser.
        You take the ownership of the returned value
        :param user - MegaUser sharing folders with this account
        :Returns List of MegaNode objects that this user is sharing with this account  
        ''' 
        return mega.MegaApi.getInShares(self.api, *args)
    
    def is_shared(self, *args):
    	'''Check if a MegaNode is being shared.
        For nodes that are being shared, you can get a a list of MegaShare objects using MegaApi::getOutShares
        :param node - Node to check 
        :Returns True if the MegaNode is being shared, otherwise false 
        ''' 
        return mega.MegaApi.isShared(self.api, *args)
    
    def get_out_shares(self, *args): 
    	'''Get a list with the active outbound sharings for a MegaNode.
        If the node doesn't exist in the account, this function returns an empty list.
        You take the ownership of the returned value
        :param node - MegaNode to check
        :Returns List of MegaShare objects  
        '''
        return mega.MegaApi.getOutShares(self.api, *args)
    
    def get_pending_out_shares(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.getPendingOutShares(self.api, *args)
    
    def get_incoming_contact_requests(self):
    	'''need clarification''' 
        return mega.MegaApi.getIncomingContactRequests(self.api)
    
    def get_outgoing_contact_requests(self):
    	'''need clarification'''
        return mega.MegaApi.getOutgoingContactRequests(self.api)
    
    def get_access(self, *args):
    	'''Get the access level of a MegaNode. 
        :param node - MegaNode to check 
        :Returns Access level of the node Valid values are:           
            MegaShare::ACCESS_OWNER
            MegaShare::ACCESS_FULL
            MegaShare::ACCESS_READWRITE
            MegaShare::ACCESS_READ
            MegaShare::ACCESS_UNKNOWN
        ''' 
        return mega.MegaApi.getAccess(self.api, *args)
    
    def get_size(self, *args):
    	'''Get the size of a node tree.
        If the MegaNode is a file, this function returns the size of the file. If it's a folder, this fuction returns the sum of the sizes of all nodes in the node tree.
        :param node - Parent node
        :Returns size of the node tree 
        ''' 
        return mega.MegaApi.getSize(self.api, *args)
    
    def get_fingerprint(self, *args):
    	'''Get a Base64-encoded fingerprint for a node.
        If the node doesn't exist or doesn't have a fingerprint, this function returns None.
        You take the ownership of the returned value
        :param node - Node for which we want to get the fingerprint
        :Returns Base64-encoded fingerprint for the file 
        ''' 
        return mega.MegaApi.getFingerprint(self.api, *args)
    
    def get_node_by_fingerprint(self, *args):
    	'''Returns a node with the provided fingerprint.
        If there isn't any node in the account with that fingerprint, this function returns None.
        You take the ownership of the returned value.
        :param fingerprint - Fingerprint to check
        :Returns MegaNode object with the provided fingerprint
        ''' 
        return mega.MegaApi.getNodeByFingerprint(self.api, *args)
    
    def has_fingerprint(self, *args): 
    	'''Check if the account already has a node with the provided fingerprint.
        A fingerprint for a local file can be generated using MegaApi::getFingerprint
        :param fingerprint - Fingerprint to check 
        :Returns True if the account contains a node with the same fingerprint 
        '''
        return mega.MegaApi.hasFingerprint(self.api, *args)
    
    def get_CRC(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.getCRC(self.api, *args)
    
    def get_node_by_CRC(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.getNodeByCRC(self.api, *args)
    
    def check_access(self, *args):
    	'''Check if a node has an access level. 
        :param node - Node to check
        :param level - Access level to check Valid values for this parameter are:        
            MegaShare::ACCESS_OWNER
            MegaShare::ACCESS_FULL
            MegaShare::ACCESS_READWRITE
            MegaShare::ACCESS_READ
        :Returns MegaError object with the result: Valid values for the error code are:        
            MegaError::API_OK - The node can be moved to the target
            MegaError::API_EACCESS - The node can't be moved because of permissions problems
            MegaError::API_ECIRCULAR - The node can't be moved because that would create a circular linkage
            MegaError::API_ENOENT - The node or the target doesn't exist in the account
            MegaError::API_EARGS - Invalid parameters
        ''' 
        return mega.MegaApi.checkAccess(self.api, *args)
    
    def check_move(self, *args):
    	'''Check if a node can be moved to a target node.
        node - Node to check
        target - Target for the move operation
        :Returns MegaError object with the result: Valid values for the error code are:        
            MegaError::API_OK - The node can be moved to the target
            MegaError::API_EACCESS - The node can't be moved because of permissions problems
            MegaError::API_ECIRCULAR - The node can't be moved because that would create a circular linkage
            MegaError::API_ENOENT - The node or the target doesn't exist in the account
            MegaError::API_EARGS - Invalid parameters
        ''' 
        return mega.MegaApi.checkMove(self.api, *args)
    
    def get_root_node(self):
    	'''Returns the root node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi::fetchNodes before, this function returns None
        :Returns Root node of the account
        ''' 
        return mega.MegaApi.getRootNode(self.api)
    
    def get_inbox_node(self):
    	'''Returns the inbox node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi::fetchNodes before, this function returns None
        :Returns Inbox node of the account
        ''' 
        return mega.MegaApi.getInboxNode(self.api)
    
    def get_rubbish_node(self): 
    	'''Returns the rubbish node of the account.
        You take the ownership of the returned value
        If you haven't successfully called MegaApi::fetchNodes before, this function returns None
        :Returns Rubbish node of the account
        '''
        return mega.MegaApi.getRubbishNode(self.api)
    
    def search(self, *args): 
    	'''Search nodes containing a search string in their name.
		The search is case-insensitive.
    	:param node	The parent node of the tree to explore
    	:param searchString	Search string. The search is case-insensitive
    	:param recursive	True if you want to seach recursively in the node tree. False if you want to seach in the children of the node only

		:Returns list of nodes that contain the desired string in their name  	
    	'''
        return mega.MegaApi.search(self.api, *args)
    
    def process_mega_tree(self, *args):
    	'''Process a node tree using a MegaTreeProcessor implementation. 
		:param node - The parent node of the tree to explore
		:param processor - MegaTreeProcessor that will receive callbacks for every node in the tree
		:param recursive - True if you want to recursively process the whole node tree. False if you want to process the children of the node only
		:Returns True  if all nodes were processed. False otherwise (the operation can be cancelled by MegaTreeProcessor::processMegaNode()) 
        ''' 
        return mega.MegaApi.processMegaTree(self.api, *args)
    
    def create_public_file_node(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.createPublicFileNode(self.api, *args)
    
    def create_public_folder_node(self, *args): 
    	'''need clarification'''
        return mega.MegaApi.createPublicFolderNode(self.api, *args)
    
    def get_version(self): 
    	'''need clarification'''
        return mega.MegaApi.getVersion(self.api)
    
    def get_user_agent(self): 
    	'''need clarification'''
        return mega.MegaApi.getUserAgent(self.api)
    
    def change_api_url(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.changeApiUrl(self.api, *args)
    
    def escape_fs_incompatible(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.escapeFsIncompatible(self.api, *args)
    
    def unescape_fs_incompatible(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.unescapeFsIncompatible(self.api, *args)
    
    def create_thumbnail(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.createThumbnail(self.api, *args)
    
    def create_preview(self, *args):
    	'''need clarification''' 
        return mega.MegaApi.createPreview(self.api, *args)
#MegaGfxProcessor.read_bitmap = MegaGfxProcessor.readBitmap
#MegaGfxProcessor.get_width = MegaGfxProcessor.getWidth
#MegaGfxProcessor.get_height = MegaGfxProcessor.getHeight
#MegaGfxProcessor.get_bitmap_data_size = MegaGfxProcessor.getBitmapDataSize
#MegaGfxProcessor.get_bitmap_data = MegaGfxProcessor.getBitmapData 
#MegaGfxProcessor.free_bitmap = MegaGfxProcessor.freeBitmap

#MegaProxy.set_proxy_type = MegaProxy.setProxyType
#MegaProxy.set_proxy_url = MegaProxy.setProxyURL
#MegaProxy.set_credentials = MegaProxy.setCredentials
#MegaProxy.get_proxy_type = MegaProxy.getProxyType
#MegaProxy.get_proxy_url = MegaProxy.getProxyURL
#MegaProxy.credentials_needed = MegaProxy.credentialsNeeded
#MegaProxy.get_username = MegaProxy.getUsername
#MegaProxy.get_password = MegaProxy.getPassword

#MegaNode.get_type = MegaNode.getType
#MegaNode.get_name = MegaNode.getName
#MegaNode.get_base64_handle = MegaNode.getBase64Handle
#MegaNode.get_size = MegaNode.getSize
#MegaNode.get_creation_time = MegaNode.getCreationTime
#MegaNode.get_modification_time = MegaNode.getModificationTime
#MegaNode.get_handle = MegaNode.getHandle
#MegaNode.get_parent_handle = MegaNode.getParentHandle
#MegaNode.get_base64_key = MegaNode.getBase64Key
#MegaNode.get_tag = MegaNode.getTag
#MegaNode.is_file = MegaNode.isFile
#MegaNode.is_folder = MegaNode.isFolder
#MegaNode.is_removed = MegaNode.isRemoved
#MegaNode.has_changed = MegaNode.hasChanged
#MegaNode.get_changes = MegaNode.getChanges
#MegaNode.has_thumbnail = MegaNode.hasThumbnail
#MegaNode.has_preview = MegaNode.hasPreview
#MegaNode.is_public = MegaNode.isPublic

#MegaUser.get_email = MegaUser.getEmail
#MegaUser.get_visibility = MegaUser.getVisibility
#MegaUser.get_timestamp = MegaUser.getTimesamp

#MegaShare.get_user = MegaShare.getUser
#MegaShare.get_node_handle = MegaShare.getNodeHandle
#MegaShare.get_access = MegaShare.getAccess
#MegaShare.get_timestamp = MegaShare.getTimestamp

#MegaRequest.get_type = MegaRequest.getType
#MegaRequest.get_request_string = MegaRequest.getRequestString
#MegaRequest.to_string = MegaRequest.toString
#MegaRequest.get_node_handle = MegaRequest.getNodeHandle
#MegaRequest.get_link = MegaRequest.getLink
#MegaRequest.get_parent_handle = MegaRequest.getParentHandle
#MegaRequest.get_session_key = MegaRequest.getSessionKey
#MegaRequest.get_name = MegaRequest.getName
#MegaRequest.get_email = MegaRequest.getEmail
#MegaRequest.get_password = MegaRequest.getPassword
#MegaRequest.get_new_password = MegaRequest.getNewPassword
#MegaRequest.get_private_key = MegaRequest.getPrivateKey
#MegaRequest.get_access = MegaRequest.getAccess
#MegaRequest.get_file = MegaRequest.getFile
#MegaRequest.get_num_retry = MegaRequest.getNumRetry
#MegaRequest.get_public_node = MegaRequest.getPublicNode
#MegaRequest.get_param_type = MegaRequest.getParamType
#MegaRequest.get_text = MegaRequest.getText
#MegaRequest.get_number = MegaRequest.getNumber
#MegaRequest.get_flag = MegaRequest.getFlag
#MegaRequest.get_transferred_bytes = MegaRequest.getTransferredBytes
#MegaRequest.get_total_bytes = MegaRequest.getTotalBytes
#MegaRequest.get_mega_account_details = MegaRequest.getMegaAccountDetails
#MegaRequest.get_pricing = MegaRequest.getPricing
#MegaRequest.get_transfer_tag = MegaRequest.getTransferTag
#MegaRequest.get_num_details = MegaRequest.getNumDetails

#MegaTransfer.get_type = MegaTransfer.getType
#MegaTransfer.get_transfer_string = MegaTransfer.getTransferString
#MegaTransfer.to_string = MegaTransfer.toString
#MegaTransfer.get_start_time = MegaTransfer.getStartTime
#MegaTransfer.get_transferred_bytes = MegaTransfer.getTransferredBytes
#MegaTransfer.get_total_bytes = MegaTransfer.getTotalBytes
#MegaTransfer.get_path = MegaTransfer.getPath
#MegaTransfer.get_parent_handle = MegaTransfer.getParentHandle
#MegaTransfer.get_node_handle = MegaTransfer.getNodeHandle
#MegaTransfer.get_parent_path = MegaTransfer.getParentPath
#MegaTransfer.get_start_pos = MegaTransfer.getStartPos
#MegaTransfer.get_end_pos = MegaTransfer.getEndPos
#MegaTransfer.get_file_name = MegaTransfer.getFileName
#MegaTransfer.get_num_retry = MegaTransfer.getNumRetry
#MegaTransfer.get_max_retries = MegaTransfer.getMaxRetries
#MegaTransfer.get_tag = MegaTransfer.getTag
#MegaTransfer.get_speed = MegaTransfer.getSpeed
#MegaTransfer.get_#delta_size = MegaTransfer.get#deltaSize
#MegaTransfer.get_update_time = MegaTransfer.getUpdateTime
#MegaTransfer.get_public_mega_node = MegaTransfer.getPublicMegaNode
#MegaTransfer.is_sync_transfer = MegaTransfer.isSyncTransfer
#MegaTransfer.is_streaming_transfer = MegaTransfer.isStreamingTransfer
#MegaTransfer.get_last_bytes = MegaTransfer.getLastBytes

#MegaContactRequest.get_handle = MegaContactRequest.getHandle
#MegaContactRequest.get_source_email = MegaContactRequest.getSourceEmail
#MegaContactRequest.get_source_message = MegaContactRequest.getSourceMessage
#MegaContactRequest.get_target_email = MegaContactRequest.getTargetEmail
#MegaContactRequest.get_creation_time = MegaContactRequest.getCreationTime
#MegaContactRequest.get_modification_time = MegaContactRequest.getModificationTime
#MegaContactRequest.get_status = MegaContactRequest.getStatus
#MegaContactRequest.is_outgoing = MegaContactRequest.isOutgoing

#MegaError.get_error_code = MegaError.getErrorCode
#MegaError.to_string = MegaError.toString

#MegaTreeProcessor.process_mega_node = MegaTreeProcessor.processMegaNode

#MegaRequestListener.on_request_start = MegaRequestListener.onRequestStart
#MegaRequestListener.on_request_finish = MegaRequestListener.onRequestFinish
#MegaRequestListener.on_request_update = MegaRequestListener.onRequestUpdate
#MegaRequestListener.on_request_temporary_error = MegaRequestListener.onRequestTemporaryError

#MegaTransferListener.on_transfer_start = MegaTransferListener.onTransferStart
#MegaTransferListener.on_transfer_finish = MegaTransferListener.onTransferFinish
#MegaTransferListener.on_transfer_update = MegaTransferListener.onTransferUpdate
#MegaTransferListener.on_transfer_temporary_error = MegaTransferListener.onTransferTemporaryError
#MegaTransferListener.on_transfer_data = MegaTransferListener.onTransferData

#MegaGlobalListener.on_users_update = MegaGlobalListener.onUsersUpdate
#MegaGlobalListener.on_nodes_update = MegaGlobalListener.onNodesUpdate
#MegaGlobalListener.on_account_update = MegaGlobalListener.onAccountUpdate
#MegaGlobalListener.on_contact_requests_update = MegaGlobalListener.onContactRequestsUpdate
#MegaGlobalListener.on_reload_needed = MegaGlobalListener.onReloadNeeded

#MegaListener.on_request_start = MegaListener.onRequestStart
#MegaListener.on_request_finish = MegaListener.onRequestFinish
#MegaListener.on_request_update = MegaListener.onRequestUpdate
#MegaListener.on_request_temporary_error = MegaListener.onRequestTemporaryError
#MegaListener.on_transfer_start = MegaListener.onTransferStart
#MegaListener.on_transfer_finish = MegaListener.onTransferFinish
#MegaListener.on_transfer_update = MegaListener.onTransferUpdate
#MegaListener.on_transfer_temporary_error = MegaListener.onTransferTemporaryError
#MegaListener.on_users_update = MegaListener.onUsersUpdate
#MegaListener.on_nodes_update = MegaListener.onNodesUpdate
#MegaListener.on_account_update = MegaListener.onAccountUpdate
#MegaListener.on_contact_requests_update = MegaListener.onContactRequestsUpdate
#MegaListener.on_reload_needed = MegaListener.onReloadNeeded
#MegaAccountBalance.get_amount = MegaAccountBalance.getAmount
#MegaAccountBalance.get_currency = MegaAccountBalance.getCurrency

#MegaAccountSession.get_creation_timestamp = MegaAccountSession.getCreationTimestamp
#MegaAccountSession.get_most_recent_usage = MegaAccountSession.getMostRecentUsage
#MegaAccountSession.get_user_agent = MegaAccountSession.getUserAgent
#MegaAccountSession.get_ip = MegaAccountSession.getIP
#MegaAccountSession.get_country = MegaAccountSession.getCountry
#MegaAccountSession.is_current = MegaAccountSession.isCurrent
#MegaAccountSession.is_alive = MegaAccountSession.isAlive
#MegaAccountSession.get_handle = MegaAccountSession.getHandle

#MegaAccountPurchase.get_timestamp = MegaAccountPurchase.getTimestamp
#MegaAccountPurchase.get_handle = MegaAccountPurchase.getHandle
#MegaAccountPurchase.get_currency = MegaAccountPurchase.getCurrency
#MegaAccountPurchase.get_amount = MegaAccountPurchase.getAmount
#MegaAccountPurchase.get_method = MegaAccountPurchase.getMethod

#MegaAccountTransaction.get_timestamp = MegaAccountTransaction.getTimestamp
#MegaAccountTransaction.get_handle = MegaAccountTransaction.getHandle
#MegaAccountTransaction.get_currency = MegaAccountTransaction.getCurrency
#MegaAccountTransaction.get_amount = MegaAccountTransaction.getAmount

#MegaAccountDetails.get_pro_level = MegaAccountDetails.getProLevel
#MegaAccountDetails.get_pro_expiration = MegaAccountDetails.getProExpiration
#MegaAccountDetails.get_subscription_status = MegaAccountDetails.getSubscriptionStatus
#MegaAccountDetails.get_subscription_renew_time = MegaAccountDetails.getSubscriptionRenewTime
#MegaAccountDetails.get_subscription_method = MegaAccountDetails.getSubscriptionMethod
#MegaAccountDetails.get_subscription_cycle = MegaAccountDetails.getSubscriptionCycle
#MegaAccountDetails.get_storage_max = MegaAccountDetails.getStorageMax
#MegaAccountDetails.get_transfer_max = MegaAccountDetails.getTransferMax
#MegaAccountDetails.get_transfer_own_used = MegaAccountDetails.getTransferOwnUsed
#MegaAccountDetails.get_num_usage_items = MegaAccountDetails.getNumUsageItems
#MegaAccountDetails.get_storage_used = MegaAccountDetails.getStorageUsed
#MegaAccountDetails.get_num_files = MegaAccountDetails.getNumFiles
#MegaAccountDetails.get_num_folders = MegaAccountDetails.getNumFolders
#MegaAccountDetails.get_num_balances = MegaAccountDetails.getNumBalances
#MegaAccountDetails.get_balance = MegaAccountDetails.getBalance
#MegaAccountDetails.get_num_sessions = MegaAccountDetails.getNumSessions
#MegaAccountDetails.get_session = MegaAccountDetails.getSession
#MegaAccountDetails.get_num_purchases = MegaAccountDetails.getNumPurchases
#MegaAccountDetails.get_purchase = MegaAccountDetails.getPurchase
#MegaAccountDetails.get_num_transactions = MegaAccountDetails.getNumTransactions
#MegaAccountDetails.get_transaction = MegaAccountDetails.getTransaction

#MegaPricing.get_num_products = MegaPricing.getNumProducts
#MegaPricing.get_handle = MegaPricing.getHandle
#MegaPricing.get_pro_level = MegaPricing.getProLevel
#MegaPricing.get_gb_storage = MegaPricing.getGBStorage
#MegaPricing.get_gb_transfer = MegaPricing.getGBTransfer
#MegaPricing.get_months = MegaPricing.getMonths
#MegaPricing.get_amount = MegaPricing.getAmount
#MegaPricing.get_currency = MegaPricing.getCurrency
#MegaPricing.get_description = MegaPricing.getDescription
#MegaPricing.get_ios_id = MegaPricing.getIosID
#MegaPricing.get_android_id = MegaPricing.getAndroidID

#del MegaGfxProcessor.readBitmap
#del MegaGfxProcessor.getWidth
#del MegaGfxProcessor.getHeight
#del MegaGfxProcessor.getBitmapDataSize
#del MegaGfxProcessor.getBitmapData
#del MegaGfxProcessor.freeBitmap 

#del MegaProxy.setProxyType
#del MegaProxy.setProxyURL
#del MegaProxy.setCredentials
#del MegaProxy.getProxyType
#del MegaProxy.getProxyURL
#del MegaProxy.credentialsNeeded
#del MegaProxy.getUsername
#del MegaProxy.getPassword

#del MegaNode.getType
#del MegaNode.getName
#del MegaNode.getBase64Handle
#del MegaNode.getSize
#del MegaNode.getCreationTime
#del MegaNode.getModificationTime
#del MegaNode.getHandle
#del MegaNode.getParentHandle
#del MegaNode.getBase64Key
#del MegaNode.getTag
#del MegaNode.isFile
#del MegaNode.isFolder
#del MegaNode.isRemoved
#del MegaNode.hasChanged
#del MegaNode.getChanges
#del MegaNode.hasThumbnail
#del MegaNode.hasPreview
#del MegaNode.isPublic

#del MegaUser.getEmail
#del MegaUser.getVisibility
#del MegaUser.getTimesamp

#del MegaShare.getUser
#del MegaShare.getNodeHandle
#del MegaShare.getAccess
#del MegaShare.getTimestamp

#del MegaRequest.getType
#del MegaRequest.getRequestString
#del MegaRequest.toString
#del MegaRequest.getNodeHandle
#del MegaRequest.getLink
#del MegaRequest.getParentHandle
#del MegaRequest.getSessionKey
#del MegaRequest.getName
#del MegaRequest.getEmail
#del MegaRequest.getPassword
#del MegaRequest.getNewPassword
#del MegaRequest.getPrivateKey
#del MegaRequest.getAccess
#del MegaRequest.getFile
#del MegaRequest.getNumRetry
#del MegaRequest.getPublicNode
#del MegaRequest.getParamType
#del MegaRequest.getText
#del MegaRequest.getNumber
#del MegaRequest.getFlag
#del MegaRequest.getTransferredBytes
#del MegaRequest.getTotalBytes
#del MegaRequest.getMegaAccountDetails
#del MegaRequest.getPricing
#del MegaRequest.getTransferTag
#del MegaRequest.getNumDetails

#del MegaTransfer.getType
#del MegaTransfer.getTransferString
#del MegaTransfer.toString
#del MegaTransfer.getStartTime
#del MegaTransfer.getTransferredBytes
#del MegaTransfer.getTotalBytes
#del MegaTransfer.getPath
#del MegaTransfer.getParentHandle
#del MegaTransfer.getNodeHandle
#del MegaTransfer.getParentPath
#del MegaTransfer.getStartPos
#del MegaTransfer.getEndPos
#del MegaTransfer.getFileName
#del MegaTransfer.getNumRetry
#del MegaTransfer.getMaxRetries
#del MegaTransfer.getTag
#del MegaTransfer.getSpeed
#del MegaTransfer.get#deltaSize
#del MegaTransfer.getUpdateTime
#del MegaTransfer.getPublicMegaNode
#del MegaTransfer.isSyncTransfer
#del MegaTransfer.isStreamingTransfer
#del MegaTransfer.getLastBytes

#del MegaContactRequest.getHandle
#del MegaContactRequest.getSourceEmail
#del MegaContactRequest.getSourceMessage
#del MegaContactRequest.getTargetEmail
#del MegaContactRequest.getCreationTime
#del MegaContactRequest.getModificationTime
#del MegaContactRequest.getStatus
#del MegaContactRequest.isOutgoing

#del MegaError.getErrorCode
#del MegaError.toString

#del MegaTreeProcessor.processMegaNode

#del MegaRequestListener.onRequestStart
#del MegaRequestListener.onRequestFinish
#del MegaRequestListener.onRequestUpdate
#del MegaRequestListener.onRequestTemporaryError

#del MegaTransferListener.onTransferStart
#del MegaTransferListener.onTransferFinish
#del MegaTransferListener.onTransferUpdate
#del MegaTransferListener.onTransferTemporaryError
#del MegaTransferListener.onTransferData

#del MegaGlobalListener.onUsersUpdate
#del MegaGlobalListener.onNodesUpdate
#del MegaGlobalListener.onAccountUpdate
#del MegaGlobalListener.onContactRequestsUpdate
#del MegaGlobalListener.onReloadNeeded

#del MegaListener.onRequestStart
#del MegaListener.onRequestFinish
#del MegaListener.onRequestUpdate
#del MegaListener.onRequestTemporaryError
#del MegaListener.onTransferStart
#del MegaListener.onTransferFinish
#del MegaListener.onTransferUpdate
#del MegaListener.onTransferTemporaryError
#del MegaListener.onUsersUpdate
#del MegaListener.onNodesUpdate
#del MegaListener.onAccountUpdate
#del MegaListener.onContactRequestsUpdate
#del MegaListener.onReloadNeeded
#del MegaAccountBalance.getAmount
#del MegaAccountBalance.getCurrency

#del MegaAccountSession.getCreationTimestamp
#del MegaAccountSession.getMostRecentUsage
#del MegaAccountSession.getUserAgent
#del MegaAccountSession.getIP
#del MegaAccountSession.getCountry
#del MegaAccountSession.isCurrent
#del MegaAccountSession.isAlive
#del MegaAccountSession.getHandle

#del MegaAccountPurchase.getTimestamp
#del MegaAccountPurchase.getHandle
#del MegaAccountPurchase.getCurrency
#del MegaAccountPurchase.getAmount
#del MegaAccountPurchase.getMethod

#del MegaAccountTransaction.getTimestamp
#del MegaAccountTransaction.getHandle
#del MegaAccountTransaction.getCurrency
#del MegaAccountTransaction.getAmount

#del MegaAccountDetails.getProLevel
#del MegaAccountDetails.getProExpiration
#del MegaAccountDetails.getSubscriptionStatus
#del MegaAccountDetails.getSubscriptionRenewTime
#del MegaAccountDetails.getSubscriptionMethod
#del MegaAccountDetails.getSubscriptionCycle
#del MegaAccountDetails.getStorageMax
#del MegaAccountDetails.getTransferMax
#del MegaAccountDetails.getTransferOwnUsed
#del MegaAccountDetails.getNumUsageItems
#del MegaAccountDetails.getStorageUsed
#del MegaAccountDetails.getNumFiles
#del MegaAccountDetails.getNumFolders
#del MegaAccountDetails.getNumBalances
#del MegaAccountDetails.getBalance
#del MegaAccountDetails.getNumSessions
#del MegaAccountDetails.getSession
#del MegaAccountDetails.getNumPurchases
#del MegaAccountDetails.getPurchase
#del MegaAccountDetails.getNumTransactions
#del MegaAccountDetails.getTransaction

#del MegaPricing.getNumProducts
#del MegaPricing.getHandle
#del MegaPricing.getProLevel
#del MegaPricing.getGBStorage
#del MegaPricing.getGBTransfer
#del MegaPricing.getMonths
#del MegaPricing.getAmount
#del MegaPricing.getCurrency
#del MegaPricing.getDescription
#del MegaPricing.getIosID
#del MegaPricing.getAndroidID


    
    
#class DelegateMegaGlobalListener(MegaGlobalListener):

#    def __init__(self, MegaApi megaApi, MegaGlobalListener listener):
 #       self.megaApi = megaApi
  #      self.listener = listener
        
   # def get_user_listener(self):
    #    return listener  
