#!/usr/bin/python3
from PyQt5.QtCore import QObject, pyqtSignal
import serial
from enum import Enum
import struct
import time
import sys
sys.path.append('/home/robot/projects/2025/rpi/generated')
import lidar_data_pb2  as pbl
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber

class Ecal(QObject):

    lidar_data_sig = pyqtSignal(list)

    def __init__(self, parent):
        QObject.__init__(self, parent)
        ecal_core.initialize(sys.argv, "RadarQt receiver")
        self.lidar_sub = ProtoSubscriber("lidar_data", pbl.Lidar)
        self.lidar_sub.set_callback(self.handle_lidar_data)

    def handle_lidar_data(self, topic_name, msg, time):
        data = list(zip(msg.angles, msg.distances, msg.quality))
        self.lidar_data_sig.emit(data)

