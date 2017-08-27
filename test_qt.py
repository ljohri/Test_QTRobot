#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>


import sys, os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
import XYZSlider  

#logger_init(logging.VERBOSE)
#logger_init(logging.INFO)
#logger_init(logging.DEBUG)





#main-------------------------------------------------
print('setup swift ...')

#swift = SwiftAPI(dev_port = '/dev/ttyACM0')
#swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI(dev_port = 'COM4') # default by filters: {'hwid': 'USB VID:PID=2341:0042'}


print('setup QT')
a = QApplication(sys.argv)
ex = Example()
sys.exit(a.exec_())

print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())
print('set Z150 ...')
swift.set_position(x=150,y=0,z = 150, wait = True,speed=2000)
swift.set_gripper (True)
sleep(5)

print('open the gripper')
swift.set_gripper(False)
sleep(2)
print('close the gripper')
swift.set_gripper (True)
sleep(5)

#swift.set_laser(True)
#sleep(5)
#swift.set_laser(False)


exit()
