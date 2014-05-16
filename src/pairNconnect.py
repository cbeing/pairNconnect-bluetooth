#! /usr/bin/env python
##
 # This file is under MIT Licence
 # Copyright (C) 2014 Skander Ben Mahmoud <skander.benmahmoud@esprit.tn>
 #   
 # Permission is hereby granted, free of charge, to any person obtaining a copy of
 # this software and associated documentation files (the "Software"),
 # to deal in the Software without restriction, including without limitation
 # the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 # sell copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 #   
 # The above copyright notice and this permission notice shall be included in all copies
 # or substantial portions of the Software.
 #   
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 # INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
 # AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 # DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 # ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



arduino_baddr = '00:12:10:17:09:70'
pin_code = '1234'
adapter_type = 'hci0'
node = None
service = "spp"

import gobject

import sys
import dbus
import dbus.service
import dbus.mainloop.glib
import time



class Rejected(dbus.DBusException):
  _dbus_error_name = "org.bluez.Error.Rejected"

class Agent(dbus.service.Object):
  exit_on_release = True

  def set_exit_on_release(self, exit_on_release):
    self.exit_on_release = exit_on_release

  @dbus.service.method("org.bluez.Agent", in_signature="", out_signature="")
  def Release(self):
    print "Release"
    if self.exit_on_release:
      mainloop.quit()

  @dbus.service.method("org.bluez.Agent", in_signature="o", out_signature="s")
  def RequestPinCode(self, device):
    return pin_code

def create_device_reply(device):
  mainloop.quit()

def create_device_error(error):
  print 'Pair Error: %s' %error
  mainloop.quit()



def pair_device():
  pass

def connectToDevice(bus, adapter):
  path = adapter.FindDevice(arduino_baddr)
  serial = dbus.Interface(bus.get_object("org.bluez", path), "org.bluez.Serial")
  print "Service : %s" %service
  print "Path : %s" %path
  node = serial.Connect(service)
  print "Connected %s to %s " %(node, arduino_baddr)
  f = open('/tmp/blue_dev', 'w+')
  f.write(node)
  f.close()

  while True:
    time.sleep(1)

  serial.Disconnect(node)



if __name__ == '__main__':

  print "Paring ..."

  dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
  bus = dbus.SystemBus()

  manager = dbus.Interface(bus.get_object("org.bluez", "/"),
      "org.bluez.Manager")

  capability = "KeyboardDisplay"
  path = manager.FindAdapter(adapter_type)
  adapter = dbus.Interface(bus.get_object("org.bluez", path), "org.bluez.Adapter")
  path = "/test/agent"
  agent = Agent(bus, path)

  mainloop = gobject.MainLoop()


  agent.set_exit_on_release(False)
  adapter.CreatePairedDevice(arduino_baddr, path, capability,
      reply_handler=create_device_reply,
      error_handler=create_device_error)

  mainloop.run()

  print "Pairing finished."
  print "Connecting ..."
  connectToDevice(bus, adapter)


