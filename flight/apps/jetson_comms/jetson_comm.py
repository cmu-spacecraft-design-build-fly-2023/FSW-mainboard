"""
`jetson_comm`
====================================================

Library for interfacing with the Jetson through UART. Also gives access
to the GPIO pins for signaling
--------------------

* Author(s): Sachit Goyal, Harry Rosmann
"""

from micropython import const

from .msg import Definitions, Message

MAX_RETRIES = const(3)


# TODO: Add comments
class JetsonComm:
    def __init__(self, uart):
        self.uart = uart

    def send_message(self, message):
        done = False
        current_seq = 0
        total_packets = message.num_packets
        while not done:
            if current_seq == 0:
                self.uart.write(message.create_header())
            else:
                self.uart.write(message.create_packet(current_seq))
            while self.uart.in_waiting != Definitions.PKT_METADATA_SIZE:
                continue
            response = self.uart.read(Definitions.PKT_METADATA_SIZE)
            (seq_num, packet_type, _) = Message.parse_packet_meta(response)
            if packet_type == Definitions.PKT_TYPE_ACK:
                current_seq = seq_num + 1
                if current_seq == total_packets:
                    done = True
            elif packet_type == Definitions.PKT_TYPE_RESET:
                current_seq = 0
            else:
                current_seq = 0

    def receive_message(self):
        expected_seq_num = 0
        retries = 0
        while self.uart.in_waiting != Definitions.HEADER_PKT_SIZE:
            continue
        header = self.uart.read(Definitions.PACKET_SIZE)
        (seq_num, packet_type, payload_size) = Message.parse_packet_meta(
            header
        )
        if packet_type != Definitions.PKT_TYPE_HEADER:
            # clear uart buffer
            raise RuntimeError("Invalid header")
        # do something with message type
        (message_type, num_packets) = Message.parse_header_payload(
            header[Definitions.PKT_METADATA_SIZE:]
        )
        self.uart.write(Message.create_ack(seq_num))
        expected_seq_num = seq_num + 1
        message = []
        while expected_seq_num != num_packets + 1:
            while self.uart.in_waiting != Definitions.PACKET_SIZE:
                continue
            packet = self.uart.read(Definitions.PACKET_SIZE)
            (seq_num, packet_type, payload_size) = Message.parse_packet_meta(
                packet
            )
            if packet_type == Definitions.PKT_TYPE_DATA and seq_num == expected_seq_num:
                expected_seq_num += 1
                retries = 0
            else:
                if retries >= MAX_RETRIES:
                    self.close_logger()
                    raise RuntimeError("Unable to receive message")
                # clear uart buffer
                retries += 1
            self.uart.write(Message.create_ack(expected_seq_num - 1))
            message += packet[Definitions.PKT_METADATA_SIZE:][:payload_size]
        return message
