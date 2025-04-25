#!/usr/bin/python3
from PyQt5.QtCore import QObject, pyqtSignal
import serial
from enum import Enum
import struct
import time
import sys
from generated import lidar_data_pb2  as pbl
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber

class Ecal(QObject):

    lidar_data_sig = pyqtSignal(list)
    amalgame_sig = pyqtSignal(list)
    balises_odom_sig=pyqtSignal(list)
    balises_nearodom_sig=pyqtSignal(list)
    transforms_sig=pyqtSignal(list)
    def __init__(self, parent):
        QObject.__init__(self, parent)
        ecal_core.initialize(sys.argv, "RadarQt receiver")
        self.lidar_sub = ProtoSubscriber("lidar_data", pbl.Lidar)
        self.lidar_sub.set_callback(self.handle_lidar_data)
        self.lidar_amalgames_sub = ProtoSubscriber("amalgames", pbl.Amalgames)
        self.lidar_amalgames_sub.set_callback(self.handle_amalgames_data)   
        self.lidar_balises_odom_sub = ProtoSubscriber("balises_odom", pbl.Balises)    
        self.lidar_balises_odom_sub.set_callback(self.handle_balises_odom_data)   
        self.lidar_balises_nearodom_sub = ProtoSubscriber("balises_near_odom", pbl.Balises)    
        self.lidar_balises_nearodom_sub.set_callback(self.handle_balises_nearodom_data)      
        # self.lidar_transforms = ProtoSubscriber("transforms",pbl.Transforms)
        # self.lidar_transforms.set_callback(self.handle_transforms)

    def handle_lidar_data(self, topic_name, msg, time):
        data = list(zip(msg.angles, msg.distances, msg.quality))
        self.lidar_data_sig.emit(data)
    
    def handle_amalgames_data(self,topic, msg, time):
        data = list(zip(msg.x,msg.y,msg.size))    
        self.amalgame_sig.emit(data)
    def handle_balises_odom_data(self,topic, msg, time):
        data = list(zip(msg.index,msg.x,msg.y))    
        self.balises_odom_sig.emit(data)
    def handle_balises_nearodom_data(self,topic, msg, time):
        data = list(zip(msg.index,msg.x,msg.y))    
        self.balises_nearodom_sig.emit(data)
    # def handle_transforms(self,topic,msg,time):
    #     data= list(zip(msg.theta, msg.tx, msg.ty))
    #     self.transforms_sig.emit(data)
