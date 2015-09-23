#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple CRUD example for the Python bindings."""

## Created: 16 May 2015 Guy Kloss <gk@mega.co.nz>
##
## (c) 2015 by Mega Limited, Auckland, New Zealand
##     https://mega.nz/
##     Simplified (2-clause) BSD License.
##
## You should have received a copy of the license along with this
## program.
##
## This file is part of the Mega SDK Python bindings example code.
##
## This code is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

__author__ = 'Guy Kloss <gk@mega.co.nz>'

import sys
import os
import logging
import time
import threading
import json
import getpass

from mega import (MegaApi, Mega_Api_Python, MegaListener, MegaError, MegaRequest, MegaNode)

# Mega SDK application key.
# Generate one for free here: https://mega.nz/#sdk
APP_KEY = 'ox8xnQZL'

# Credentials file to look for login info.
CREDENTIALS_FILE = 'credentials.json'


class AppListener(MegaListener):
    """
    A listener that will contain callback methods called upon events
    from the asyncrhonous API. Only a certain number of usefuul
    callbacks are implemented.
    """

    # Inhibit sending an event on callbacks from these requests.
    _NO_EVENT_ON = (MegaRequest.TYPE_LOGIN,
                    MegaRequest.TYPE_FETCH_NODES)

    def __init__(self, continue_event):
        """
        Constructor.

        :param continue_event: Event to use for notifying our main code
            upon completion of the asyncrhonous operation.
        """
        self.continue_event = continue_event
        self.root_node = None
        super(AppListener, self).__init__()


    def onRequestStart(self, api, request):
        """
        Called upon starting the async API operation.

        :param api: Reference to the API object.
        :param request: Reference to the request this operation belongs to.
        """
        logging.info('Request start ({})'.format(request))


    def onRequestFinish(self, api, request, error):
        """
        Called upon finishing the async API operation.

        :param api: Reference to the API object.
        :param request: Reference to the request this operation belongs to.
        :param eror: Error information. API_OK if it finishes without a
            problem.
        """
        logging.info('Request finished ({}); Result: {}'
                     .format(request, error))

        request_type = request.getType()
        if request_type == MegaRequest.TYPE_LOGIN:
            api.fetch_nodes()
        elif request_type == MegaRequest.TYPE_FETCH_NODES:
            self.root_node = api.get_root_node()
        elif request_type == MegaRequest.TYPE_ACCOUNT_DETAILS:
            account_details = request.getMegaAccountDetails()
            logging.info('Account details received')
            logging.info('Storage: {} of {} ({} %)'
                         .format(account_details.getStorageUsed(),
                                 account_details.getStorageMax(),
                                 100 * account_details.getStorageUsed()
                                 / account_details.getStorageMax()))
            logging.info('Pro level: {}'.format(account_details.getProLevel()))

        # Notify other thread to go on.
        if request_type not in self._NO_EVENT_ON:
            self.continue_event.set()


    def onRequestTemporaryError(self, api, request, error):
        """
        Called upon a temprary error of the API operation. To be continued
        (involving further callbacks).

        :param api: Reference to the API object.
        :param request: Reference to the request this operation belongs to.
        :param eror: Error information.
        """
        logging.info('Request temporary error ({}); Error: {}'
                     .format(request, error))


    def onTransferFinish(self, api, transfer, error):
        """
        Called upon finishing the async API transfer operation.

        :param api: Reference to the API object.
        :param request: Reference to the request this operation belongs to.
        :param eror: Error information. API_OK if it finishes without a
            problem.
        """
        logging.info('Transfer finished ({}); Result: {}'
                     .format(transfer, transfer.getFileName(), error))
        self.continue_event.set()


    def onTransferUpdate(self, api, transfer):
        """
        Called intermittently to provide updates on the async API transfer
        operation.

        :param api: Reference to the API object.
        :param transfer: Information about the transfer.
        """
        logging.info('Transfer update ({} {});'
                     ' Progress: {} KB of {} KB, {} KB/s'
                     .format(transfer,
                             transfer.getFileName(),
                             transfer.getTransferredBytes() / 1024,
                             transfer.getTotalBytes() / 1024,
                             transfer.getSpeed() / 1024))


    def onTransferTemporaryError(self, api, transfer, error):
        """
        Called upon a temprary error of the API transfer operation. To be
        continued (involving further callbacks).

        :param api: Reference to the API object.
        :param transfer: Information about the transfer.
        :param eror: Error information.
        """
        logging.info('Transfer temporary error ({} {}); Error: {}'
                     .format(transfer, transfer.getFileName(), error))


    def onUsersUpdate(self, api, users):
        """
        Called upon an update from the API to a user's contacts.

        :param api: Reference to the API object.
        :param users: List that contains the new or updated contacts.
        """
        logging.info('Users updated ({})'.format(users.size()))


    def onNodesUpdate(self, api, nodes):
        """
        Called upon an update from the API for changed/updated storage nodes.

        :param api: Reference to the API object.
        :param nodes: List that contains the new or updated nodes.
        """
        if nodes != None:
            logging.info('Nodes updated ({})'.format(nodes.size()))
        self.continue_event.set()


class AsyncExecutor(object):
    """
    Simple helper that will wrap asynchronous invocations of API operations
    to notify the caller via an event upon completion.

    This executor is "simple", it is not suitable for overlapping executions,
    but only for a sequential chaining of API calls.
    """

    def __init__(self):
        """
        Constructor that creates an event used for notification from the
        API thread.
        """
        self.continue_event = threading.Event()

    def do(self, function, args):
        """
        Performs the asynchronous operation and waits for a signal from the
        Mega API using the event.

        :param function: Callable Mega API operation.
        :param args: Arguments to the callable.
        """
        self.continue_event.clear()
        function(*args)
        self.continue_event.wait()


def worker(api, listener, executor, credentials):
    """
    Sequential collection of (CRUD) operations on the Mega API.

    :param api: Reference to the Mega API object.
    :param listener: Listener to receie callbacks and results from the
        Mega API.
    :param executor: Simple asynchronous API command executor to enable
        a sequential/synchronous flow of operations in this function.
    :param credentials: Dictionary containing a `user` and a `password`
        string to log into the Mega account.
    """
    # Log in.
    logging.info('*** start: login ***')
    executor.do(api.login, (str(credentials['user']),
                            str(credentials['password'])))
    cwd = listener.root_node
    logging.info('*** done: login ***')

    # Who am I.
    logging.info('*** start: whoami ***')
    logging.info('My email: {}'.format(api.get_my_email()))
    executor.do(api.get_account_details, ())
    contacts = api.get_contacts()
    print api.get_account_details(api.create_delegate_mega_listener())
    shares = api.get_in_shares(contacts[0])
    children = api.get_children(api.get_node_by_path("sandbox", cwd), 1)
    search_list = api.search(api.get_node_by_path("Test", cwd), "AHCI")
    recursive_search_list = api.search_recursively(api.get_node_by_path("Test, cwd"),"AHCI", True)
    incoming_contacts = api.get_incoming_contact_requests()
    outgoing_contacts = api.get_outgoing_contact_requests()
    out_share_list = api.get_all_out_shares()
    for item in out_share_list:
        print "The outgoing share is: " + str(item)
    for item in incoming_contacts:
        print "The incoming contact is: " + str(item)
    for item in outgoing_contacts:
        print "The outgoing contact is: " + str(item)
    for search_item in search_list:
        print "The found item is: " + str(search_item.getType())
    for item in recursive_search_list:
        print "The recursively found item is: " + str(item.getType())
    for child in children:
        print "The child node type is: " + str(child.getType())
    if len(shares) > 0:
        for share in shares:
            print "The share object's and its address is: " + str(share)
            print "The type of the object is: " + str(share.getType())
    else:
        print 'There are no shares'
    if len(contacts) > 0:
        for contact in contacts:
            print "The user object and its address is: " + str(contact)
            print "The contact's email is: " + str(contact.getEmail())
            print "The contact's timestamp is " + str(contact.getTimestamp())
            print "The contact's visibility code is: " + str(contact.getVisibility())
    logging.info('*** done: whoami ***')
    # Make a directory.
    logging.info('*** start: mkdir ***')
    print '###', cwd.getName()
    check = api.get_node_by_path('sandbox', cwd)
    if check == None:
        executor.do(api.create_folder, ('sandbox', cwd))
    else:
        logging.info('Path already exists: {}'
                     .format(api.get_node_path(check)))
    logging.info('*** done: mkdir ***')

    # Now go and play in the sandbox.
    logging.info('*** start: cd ***')
    node = api.get_node_by_path('sandbox', cwd)
    if node == None:
        logging.warn('No such file or directory: sandbox')
    if node.getType() == MegaNode.TYPE_FOLDER:
        cwd = node
    else:
        logging.warn('Not a directory: sandbox')
    logging.info('*** done: cd ***')

    # Upload a file (create).
    logging.info('*** start: upload ***')
    executor.do(api.start_upload, ('README.md', cwd))
    logging.info('*** done: upload ***')

    # Download a file (read).
    logging.info('*** start: download ***')
    node = api.get_node_by_path('README.md', cwd)
    if node != None:
        executor.do(api.start_download, (node, 'README_returned.md'))
    else:
        logging.warn('Node not found: {}'.format('README.md'))
    logging.info('*** done: download ***')

    # Change a file (update).
    # Note: A new upload won't overwrite, but create a new node with same
    #       name!
    logging.info('*** start: update ***')
    old_node = api.get_node_by_path('README.md', cwd)
    executor.do(api.start_upload, ('README.md', cwd))
    if old_node != None:
        # Remove the old node with the same name.
        executor.do(api.remove, (old_node,))
    else:
        logging.info('No old file node needs removing')
    logging.info('*** done: update ***')

    # Delete a file.
    logging.info('*** start: delete ***')
    node = api.get_node_by_path('README.md', cwd)
    if node != None:
        executor.do(api.remove, (node,))
    else:
        logging.warn('Node not found: README.md')
    logging.info('*** done: delete ***')

    # Logout.
    logging.info('*** start: logout ***')
    executor.do(api.logout, ())
    listener.root_node = None
    logging.info('*** done: logout ***')


def main():
    """
    Sets up all that is needed to make (asynchronous) calls on the Mega API,
    then executs the worker to perform the desired operations.
    """
    # Get credentials.
    logging.info('Obtaining Mega login credentials.')
    credentials = {}
    if os.path.exists(CREDENTIALS_FILE):
        credentials = json.load(open(CREDENTIALS_FILE))
    else:
        credentials['user'] = raw_input('User: ')
        credentials['password'] = getpass.getpass()

    # Create the required Mega API objects.
    executor = AsyncExecutor()
    #api = MegaApi(APP_KEY, None, None, 'Python CRUD example')
    wrapApi = Mega_Api_Python(APP_KEY, None, None, 'Python CRUD example')
    listener = AppListener(executor.continue_event)
    wrapApi.add_listener(listener)
    # Run the operations.
    start_time = time.time()
    worker(wrapApi, listener, executor, credentials)
    logging.info('Total time taken: {} s'.format(time.time() - start_time))


if __name__ == '__main__':
    # Set up logging.
    logging.basicConfig(level=logging.INFO,
                        #filename='runner.log',
                        format='%(levelname)s\t%(asctime)s (%(threadName)-10s) %(message)s')

    # Do the work.
    main()
