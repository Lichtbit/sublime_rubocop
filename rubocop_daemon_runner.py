from os.path import expanduser
from os import path
import socket
import os
import signal
import sublime
import subprocess

BUFFER_SIZE = 4096
STATUS_ID = "rubocop_daemon_runner"

class RubocopDaemonRunner(object):
  def __init__(self, view, args):
    self.view = view
    self.config_file = ''
    self.port = None
    self.token = None
    self.socket = None
    self.workspace = None
    self.auto_correct = False
    self.start_daemon_automaticly = False
    vars(self).update(args)
 
  def run(self, pathlist, options=[]):
    if not self.workspace:
      self.set_short_status(self.view, "Rubocop Daemon: Workspace path not defined")
      return ""

    if not self.daemon_online():
      if self.start_daemon_automaticly:
        self.start_daemon()
        self.set_short_status(self.view, "Rubocop Daemon starting ...")
      else:
        self.set_short_status(self.view, "Rubocop Daemon not running")
      return ""

    self.connect_to_socket()
    self.send_to_socket(pathlist, options)
    return self.recvall_from_socket()

  def set_short_status(self, active_view, text):
    def erase_status():
      active_view.erase_status(STATUS_ID)
    active_view.set_status(STATUS_ID, text)
    sublime.set_timeout_async(erase_status, 2000)

  def start_daemon(self):
    subprocess.Popen(self.start_daemon_automaticly, cwd=self.workspace)

  def send_to_socket(self, pathlist, options):
    options_string = self.options_string(pathlist, options)
    send_body = "%s %s exec %s" % (self.token, self.workspace, options_string)
    self.socket.sendall(send_body.encode())

  def daemon_online(self):
    self.token = self.daemon_file("token")
    self.port = self.daemon_file("port")
    pid = self.daemon_file("pid")
    if self.token == "" or self.port == "" or pid == "": return False
    self.port = int(self.port)
    try:
        os.kill(int(pid), 0)
    except OSError:
        return False
    else:
        return True

  def connect_to_socket(self):
    self.socket = socket.socket()
    self.socket.connect(('localhost', self.port))

  def recvall_from_socket(self):
    self.socket.shutdown(socket.SHUT_WR)
    data = b''
    while True:
      part = self.socket.recv(BUFFER_SIZE)
      data += part
      if len(part) < BUFFER_SIZE:
          # either 0 or end of data
          break
    self.socket.close()
    return data

  def daemon_file(self, name):
    sub_path = self.workspace.strip("/").replace('/', '+')
    file = path.join(expanduser("~"), ".cache/rubocop-daemon/%s/%s" % (sub_path, name))
    return "" if not path.isfile(file) else open(file, "r").read()

  def options_string(self, pathlist, options=[]):
    list = self.options_list(pathlist, options)
    return ' '.join(list)

  def options_list(self, pathlist, options=[]):
    result = []

    if options:
      for option in options:
        result.append(option)
    if self.config_file:
      result.append('-c')
      result.append(self.config_file)
    if self.auto_correct:
      result.append('-a')
    for path in pathlist:
      result.append(path)

    return result
