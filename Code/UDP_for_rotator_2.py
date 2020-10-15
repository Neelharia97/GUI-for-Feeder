"""
Name: feeder.py
Author: ZHANG Yu

Description:
set/get feeder status.
"""

import socket
import binascii
import time


class MjkFeederControl(object):

    def __init__(self):
        self.bus = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bus_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bus_server.bind(('192.6.94.22', 8002))
        self.bus_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer_size = 1024
        self.connection_method = ''
        self.address = ''
        self.bytes_transferred = 0




    def __del__(self):
        self.bus.close()

    def open(self, connection_method='TCP', address='127.0.0.1', **kwargs):
        self.connection_method = connection_method
        if 'port' in kwargs:
            self.address = (address, int(kwargs['port']))
        else:
            self.address = (address, 7000)
        self.bus.connect(self.address)

    def write(self, buffer):
        buf = bytes.fromhex(buffer.replace(' ', ''))
        self.bus_client.sendto(buf,('192.6.94.17', 4001))

    def read(self):
        ret = self.bus_server.recv(self.buffer_size)
        ret = binascii.b2a_hex(ret)
        return ret

    def query(self, buffer):
        self.write(buffer)
        return self.read()

    def close(self):
        try:
            self.__del__()
        except Exception as e:
            print(f'MJK Feeder Closed failed: {e}')

    def set_position(self, position, speed=5):
        cmd = control_command(speed, position)
        self.write(cmd)
        return self.read()

    def get_position(self):
        cmd = get_position_cmd()
        self.write(cmd)
        ret = self.read()
        position = read_position(ret)
        return position

    def stop(self):

        self.write(stop_command)
        return self.read()

    def search_zero(self):
        self.query(search_zero)
        last_position = self.get_position()
        while True:
            time.sleep(2)
            current_position = self.get_position()
            if int(last_position) == int(current_position):
                break
            else:
                last_position = current_position
        return True

    def set_zero(self):
        self.write(reset_zero)
        return self.read()


def control_command(speed, position):
    '''

    :param speed: degree per second
    :param position:  target angle
    :return: commands of setting speed and position
    '''
    buf = list()
    buf.append(1)  # axis
    buf.append(0x10)  # function_code
    buf.append(0x00)  # control_code_0
    buf.append(0x14)  # control_code_1
    buf.append(0x00)  # control_code_2
    buf.append(0x04)  # control_code_3
    buf.append(0x08)  # control_code_4
    speed = speed * 60
    position = position * 1000
    buf.append(speed >> 8 & 0xFF)  # speed_m
    buf.append(speed >> 0 & 0xFF)  # speed_l
    buf.append(speed >> 24 & 0xFF)  # speed_h
    buf.append(speed >> 16 & 0xFF)  # speed_h_s
    buf.append(position >> 8 & 0xFF)  # speed_m
    buf.append(position >> 0 & 0xFF)  # speed_l
    buf.append(position >> 24 & 0xFF)  # speed_h
    buf.append(position >> 16 & 0xFF)  # speed_h_s
    buf += crc_calc(buf[:15])
    s = generate_command(buf)
    return s


def generate_command(buf_list):
    return ' '.join([f'{x:02x}' for x in buf_list])


def crc_calc(crc_buf):
    crc = 0xFFFF
    for pos in crc_buf:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return [crc & 0xff, crc >> 8]


stop_command = '01 10 03 e8 00 01 02 00 0b c3 bf'  # stop two times?
search_zero = '01 10 01 f5 00 01 02 00 01 63 f5'  # searching 0 position
reset_zero = '01 10 01 f6 00 01 02 00 01 63 c6'


def get_position_cmd():
    '''

    :return: commands of get feeder position
    '''
    buf = list()
    buf.append(1)  # axis
    buf.append(0x03)  # function_code
    buf.append(0x04)  # control_code_0
    buf.append(0x62)  # control_code_1
    buf.append(0x00)  # control_code_2
    buf.append(0x02)  # control_code_3
    buf += crc_calc(buf[:6])
    s = generate_command(buf)
    return s


def read_position(buf):
    axis = int(buf[:2], 16)
    function_code = int(buf[2:4], 16)
    control_code = int(buf[4:6], 16)
    p_m = int(buf[6:8], 16)
    p_l = int(buf[8:10], 16)
    p_h_s = int(buf[10:12], 16)
    p_h = int(buf[12:14], 16)
    crc_l = int(buf[14:16], 16)
    crc_l = int(buf[16:18], 16)
    position = ((p_h_s << 24) + (p_h << 16) + (p_m << 8) + p_l) / 1000
    return round(position, 2)

