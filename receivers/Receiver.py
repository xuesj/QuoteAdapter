# -*- coding: utf-8 -*-
"""A program to simulate quote receiver receiving message from Exchange Server"""

import datetime
from multiprocessing import Process
import os.path
import time
from utils import Protocol
from utils.observer import Event
import fcntl


class ExchangeServer(object):
    def __init__(self,
                 exchange,
                 protocol,
                 pub_port,
                 ret_port,
                 timeout,
                 trans_cal):
        self._exchange = exchange
        self._protocol = protocol
        self._pub_port = pub_port
        self._last_msg_time = None
        self._ret_port = ret_port
        self._timeout = timeout
        self._trans_cal = trans_cal

    @property
    def exchange(self):
        return self._exchange

    @property
    def pub_port(self):
        return self._pub_port

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, val):
        self._timeout = val

    @property
    def last_msg_time(self):
        return self._last_msg_time

    @last_msg_time.setter
    def last_msg_time(self, val):
        self._last_msg_time = val

    def is_open(self, dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        if self._trans_cal.is_trans_day(dt) and self._trans_cal.is_trans_time(dt):
            return True
        else:
            return False

    @staticmethod
    def is_close(dt=None):
        pass

    def has_msg(self):
        if self._protocol == Protocol.FILE:
            msg_time = os.path.getmtime(self._pub_port)
            if msg_time > self._last_msg_time:
                return True
            else:
                return False
        else:
            return True


class QuoteReceiver(Process):
    """Exchange quote service to provide real time quote of all its market"""

    def __init__(self, exchange_server, queue):
        super(QuoteReceiver, self).__init__()
        self._exchange_server = exchange_server
        self._port = self._exchange_server.pub_port
        # self._quote = None
        self._queue = queue
        self._msg_event = Event()
        self._msg_event.subscribe(self.on_msg)

    @property
    def queue(self):
        return self._queue

    def get_msg(self):
        with open(self._port, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            msg = f.read()
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        return msg

    def login(self):
        pass

    def logout(self):
        pass

    def dispatch(self):
        waiting_time = 0
        start_time = time.time()
        while waiting_time < self._exchange_server.timeout:
            if self._exchange_server.has_msg():
                self._exchange_server.last_msg_time = os.path.getmtime(self._port)
                msg = self.get_msg()
                self._msg_event.emit(msg)
                waiting_time = 0
                start_time = time.time()
            else:
                waiting_time += time.time() - start_time

    def run(self):
        while self._exchange_server.is_open():
            self.login()
            self.dispatch()
            self.logout()

    def on_msg(self, msg):
        self._queue.put(msg)
