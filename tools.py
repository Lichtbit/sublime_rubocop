import os
import pipes
import sublime


class FileTools(object):
  @staticmethod
  def quote(path):
    # TODO: Use shlex.quote as soon as a newer python version is available.
    return pipes.quote(path)

  @staticmethod
  def is_ruby_file(view):
    if not view:
      return False
    return view.match_selector(0, 'source.ruby')

class Settings():
  @staticmethod
  def get(view, key, default=""):
    file_settings = sublime.load_settings('RubocopDaemon.sublime-settings')
    try:
      value = view.settings().get('rubocop_daemon').get(key)
    except AttributeError:
      value = ""
    return value or file_settings.get(key, view.settings().get("rubocop_daemon_" + key, default))
