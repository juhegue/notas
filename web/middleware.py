# coding: utf-8

import threading


def get_request():
    thread_local = RequestMiddleware.thread_local
    if hasattr(thread_local, 'request'):
        return thread_local.request


class RequestMiddleware(object):
    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.thread_local.request = request

        response = self.get_response(request)
        return response
