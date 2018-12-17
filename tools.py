import os
import pipes
import sublime

RUBY_SYNTAX_FILES = [
  'Ruby.sublime-syntax',
  'Ruby on Rails.sublime-syntax',
  'RSpec.sublime-syntax',
]

class FileTools(object):
  @staticmethod
  def quote(path):
    # TODO: Use shlex.quote as soon as a newer python version is available.
    return pipes.quote(path)

  @staticmethod
  def is_ruby_file(view):
    if not view:
      return False
    syntax_file = view.settings().get('syntax')

    if syntax_file == None:
      return False

    for syntax in RUBY_SYNTAX_FILES:
      if syntax_file.endswith(syntax):
        return True
    return False

class Settings():
  @staticmethod
  def get(view, key, default=""):
    file_settings = sublime.load_settings('RubocopDaemon.sublime-settings')
    try:
      value = view.settings().get('rubocop_daemon').get(key)
    except AttributeError:
      value = ""
    return value or file_settings.get(key, view.settings().get("rubocop_daemon_" + key, default))
