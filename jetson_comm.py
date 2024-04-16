# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`jetson_comm`
====================================================

Library for interfacing with the Jetson through UART. Also gives access
to the GPIO pins for signaling
--------------------

TBD

"""
from struct import pack, unpack 

MAX_PACKETS = 0xFFFF
PKT_TYPE_HEADER = 0x00
PKT_TYPE_DATA = 0x01
PKT_TYPE_ACK = 0x02
PKT_TYPE_NACK = 0x03
PKT_TYPE_RESET = 0x04
PACKET_SIZE = 256
PKT_METADATA_SIZE = 4
HEADER_PAYLOAD_SIZE = 4
PAYLOAD_PER_PACKET = PACKET_SIZE - PKT_METADATA_SIZE
HEADER_PADDING_SIZE = PAYLOAD_PER_PACKET - HEADER_PAYLOAD_SIZE
ACK_PADDING_SIZE = PAYLOAD_PER_PACKET

class Message:
    def __init__(self, message_type, data):
        self.message_type = message_type
        self.data = data
        self.data_len = len(data)
        if self.data_len % PAYLOAD_PER_PACKET != 0:
            self.data += bytearray(PAYLOAD_PER_PACKET - (self.data_len % PAYLOAD_PER_PACKET))
            self.data_len = len(self.data) 
        self.num_packets = self.data_len // PAYLOAD_PER_PACKET
        if self.message_type > 0xFF or self.message_type < 0x00:
            raise ValueError("Message type out of range")
        if self.num_packets > MAX_PACKETS:
            raise ValueError("Data too large to send")
        self.packets = [self.data[i*PAYLOAD_PER_PACKET:(i+1)*PAYLOAD_PER_PACKET] 
                        for i in range(self.num_packets)]
        
        
    def create_header(self):
        header_seq = 0x00
        data = pack('@HBBBH', header_seq, PKT_TYPE_HEADER, HEADER_PAYLOAD_SIZE, 
             self.message_type, self.num_packets) + bytearray(HEADER_PADDING_SIZE)
        return data
    
    def create_packet(self, packet_seq):
        if packet_seq > self.num_packets or packet_seq <= 0:
            raise ValueError("Packet number out of range")
        if packet_seq == self.num_packets:
            packet_payload_size = self.data_len % PAYLOAD_PER_PACKET 
            if packet_payload_size == 0:
                packet_payload_size = PAYLOAD_PER_PACKET
        else:
            packet_payload_size = PAYLOAD_PER_PACKET
        metadata = pack('@HBB', packet_seq, PKT_TYPE_DATA, packet_payload_size)
        current_packet = self.packets[packet_seq - 1][:packet_payload_size]
        return metadata + current_packet
    
    @staticmethod
    def create_ack(packet_seq):
        if packet_seq > MAX_PACKETS or packet_seq < 0:
            raise ValueError("Packet number out of range")
        return pack('@HBB', packet_seq, PKT_TYPE_ACK, 0x00) 

    @staticmethod
    def create_nack(packet_seq):
        if packet_seq > MAX_PACKETS or packet_seq < 0:
            raise ValueError("Packet number out of range")
        return pack('@HBB', packet_seq, PKT_TYPE_NACK, 0x00) 

    @staticmethod
    def create_reset():
        return pack('@HBB', 0x00, PKT_TYPE_RESET, 0x00) 
    
    @staticmethod
    def parse_packet_meta(metadata):
        try:
            seq_num, packet_type, payload_size = unpack('@HBB', metadata)
        except:
            raise ValueError("Invalid packet format")
        return seq_num, packet_type, payload_size
    
    @staticmethod                                                                                                                                    
    def parse_header_payload(header_payload):
        message_type, num_packets = unpack('@BH', header_payload)
        return message_type, num_packets
    
import time 
class JetsonComm:
    def __init__(self, uart):
        self.uart = uart
        
    def send_message(self, message):
        done = False
        current_seq = 0
        total_packets = message.num_packets
        while(not done):
            if current_seq == 0:
                self.uart.write(message.create_header())
            else:
                self.uart.write(message.create_packet(current_seq))
            while(self.uart.in_waiting < PKT_METADATA_SIZE):
                continue
            response = self.uart.read(PKT_METADATA_SIZE)
            (seq_num, packet_type, _) = Message.parse_packet_meta(response)
            if packet_type == PKT_TYPE_ACK and seq_num == current_seq:
                if current_seq == total_packets:
                    done = True
                current_seq += 1
            elif packet_type == PKT_TYPE_NACK:
                continue
            elif packet_type == PKT_TYPE_RESET:
                current_seq = 0
            else:
                current_seq = 0

    def receive_message(self):
        expected_seq_num = 0
        while(self.uart.in_waiting < PACKET_SIZE):
            continue
        header = self.uart.read(PACKET_SIZE)
        (seq_num, packet_type, payload_size) = Message.parse_packet_meta(header[:PKT_METADATA_SIZE])
        if packet_type != PKT_TYPE_HEADER:
            raise ValueError("Invalid header")
        (message_type, num_packets) = Message.parse_header_payload(header[PKT_METADATA_SIZE:]
                                                                   [:HEADER_PAYLOAD_SIZE])
        self.uart.write(Message.create_ack(seq_num))
        expected_seq_num = seq_num + 1
        message = bytearray()
        print(num_packets)
        for i in range(num_packets):
            while(self.uart.in_waiting < PACKET_SIZE):
                continue
            packet = self.uart.read(PACKET_SIZE)
            (seq_num, packet_type, payload_size) = Message.parse_packet_meta(packet[:PKT_METADATA_SIZE])
            if packet_type != PKT_TYPE_DATA or seq_num != expected_seq_num:
                raise ValueError("Incorrect seq num")
            # print(f'Received seq_num {seq_num}')
            self.uart.write(Message.create_ack(seq_num))
            # print(f'Acked seq_num {seq_num}')
            expected_seq_num += 1
            # message += packet[PKT_METADATA_SIZE:][:payload_size]
        return message
