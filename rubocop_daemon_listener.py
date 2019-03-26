import sublime
import sublime_plugin
import locale
import re
import os

from .tools import FileTools
from .tools import Settings
from .rubocop_daemon_runner import RubocopDaemonRunner

REGIONS_ID = 'rubocop_daemon_remark_regions'
STATUS_ID = 'rubocop_daemon'
REGIONS_OPTIONS_BITS = (sublime.DRAW_EMPTY |
                        sublime.DRAW_NO_FILL |
                        sublime.DRAW_NO_OUTLINE |
                        sublime.DRAW_SQUIGGLY_UNDERLINE |
                        sublime.HIDE_ON_MINIMAP)

# Event listener to provide on the fly checks when saving a ruby file.
class RubocopDaemonEventListener(sublime_plugin.EventListener):
  def __init__(self):
    super(RubocopDaemonEventListener, self).__init__()
    self.file_remark_dict = {}
    sublime.set_timeout_async(self.update_marks, 2)

  def get_current_file_dict(self, view):
    if not (view.file_name() in self.file_remark_dict.keys()):
      return None

    return self.file_remark_dict[view.file_name()]

  def clear_marks(self, view):
    dct = self.get_current_file_dict(view)
    if dct:
      dct.clear()
    view.erase_regions(REGIONS_ID)

  def update_marks(self):
    for wnd in sublime.windows():
      for vw in wnd.views():
        self.do_in_file_check(vw)

  def line_no_of_cop_result(self, file_name, result):
    res = result.decode(locale.getpreferredencoding())
    reg_result = re.search(r"^.*:(\d*):\d*: .: (.*)$", res)
    if reg_result:
      return reg_result.group(1), reg_result.group(2).strip()
    return None, None

  def set_marks_by_results(self, view, cop_results):
    lines = []
    path = view.file_name()
    base_file = os.path.basename(path)
    view_dict = self.get_current_file_dict(view)
    if not view_dict:
      view_dict = {}
      self.file_remark_dict[path] = view_dict
    for result in cop_results:
      line_no, message = self.line_no_of_cop_result(base_file, result)
      if line_no is not None:
        ln = int(line_no) - 1
        view_dict[ln] = message
        print(message)
        line = view.line(view.text_point(ln, 0))
        lines.append(sublime.Region(line.begin(), line.end()))
    self.mark_lines(view, lines)

  def mark_lines(self, view, lines):
    icon = Settings.get(view, 'mark_icon', 'arrow_right')
    view.add_regions(REGIONS_ID, lines, 'keyword', icon, REGIONS_OPTIONS_BITS)

  def run_rubocop(self, view):
    if Settings.get(view, 'disable', False):
      return []

    cfg_file = Settings.get(view, 'config_file')
    if cfg_file:
      cfg_file = FileTools.quote(cfg_file)

    runner = RubocopDaemonRunner(view, {
      'config_file': cfg_file,
      'workspace': Settings.get(view, 'workspace'),
      'auto_correct': Settings.get(view, 'auto_correct', False),
      'start_daemon_automaticly': Settings.get(view, 'start_daemon_automaticly', False),
    })
    output = runner.run([view.file_name()], ['--format', 'emacs', '--force-exclusion']).splitlines()

    return output

  def mark_issues(self, view, mark):
    self.clear_marks(view)
    if mark:
      results = self.run_rubocop(view)
      self.set_marks_by_results(view, results)

  def do_in_file_check(self, view):
    if not FileTools.is_ruby_file(view):
      return
    mark = Settings.get(view, 'mark_issues_in_view')
    self.mark_issues(view, mark)

  def on_post_save_async(self, view):
    self.do_in_file_check(view)

  def on_selection_modified(self, view):
    curr_sel = view.sel()
    if curr_sel:
      view_dict = self.get_current_file_dict(view)
      if not view_dict:
        return
      first_sel = curr_sel[0]
      row, col = view.rowcol(first_sel.begin())
      if row in view_dict.keys():
        view.set_status(STATUS_ID, 'RuboCop: {0}'.format(view_dict[row]))
      else:
        view.set_status(STATUS_ID, '')
