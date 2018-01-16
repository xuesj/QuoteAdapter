# -*- coding: UTF-8 -*-

import socket

HOST, PORT = "localhost", 9129


class MsgStatus(object):
    B = 0
    H = 1
    I = 2
    E = 3


class TCPMessage(object):
    def __init__(self, head_str='HEADER|MTP1.00', tail_str='TRAILER|ABC'):
        self._status = MsgStatus.B
        self._head = ''
        self._info = ''
        self._tail = ''
        self._head_str = head_str
        self._tail_str = tail_str

    @property
    def status(self):
        return self._status

    def feed_info(self, rec):
        head_sep = rec.find(self._head_str)
        tail_sep = rec.find(self._tail_str)
        if head_sep == -1 and tail_sep == -1:
            if self._status == MsgStatus.H or MsgStatus.I:
                self._info += rec
                self._status = MsgStatus.I
            else:
                raise ValueError
            return '', rec, ''
        elif head_sep >= 0 and tail_sep == -1:
            prev = rec[0:head_sep]
            info = rec[head_sep:]
            body_sep = info.find('\n')
            if self._status == MsgStatus.B or MsgStatus.E:
                self._head = info[0:body_sep]
                self._info += info[body_sep:]
                self._status = MsgStatus.I
            else:
                raise ValueError
            return prev, info[0:body_sep], ''
        elif head_sep == -1 and tail_sep >= 0:
            prev = rec[0:tail_sep]
            info = rec[tail_sep:]
            tail_end = info.find('\n')
            if self._status == MsgStatus.I:
                self._info += prev
                self._tail = info[0:tail_end]
                left = info[tail_end:]
                self._status = MsgStatus.E
            else:
                raise ValueError
            return prev, info[0:tail_end], left
        elif head_sep >= 0 and tail_sep >= 0:
            prev = rec[0:head_sep]
            info = rec[head_sep:]
            head_end = info.find('\n')
            head = info[0:head_end]
            body = info[head_end:tail_sep]
            left = info[tail_sep:]
            tail_end = left.find('\n')
            tail = left[0:tail_end]
            left = left[tail_end:]
            if self._status == MsgStatus.B or self._status == MsgStatus.E:
                self._head = head
                self._info = body
                self._tail = tail
                self._status = MsgStatus.E
            else:
                raise ValueError
            return prev, head+body+tail, left

    @property
    def msg(self):
        return self._head + self._info + self._tail


if __name__ == '__main__':
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        msg_status = MsgStatus.B

        # Receive data from the server and shut down
        i = 1
        left = ''
        while i <= 5:
            msg = TCPMessage()
            while msg.status != MsgStatus.E:
                received = left + sock.recv(1024)
                prev, info, left = msg.feed_info(received)
            print "Received: {}\n{}".format(str(i), msg.msg)
            i += 1
    finally:
        sock.close()
