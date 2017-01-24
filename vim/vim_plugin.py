# Author: Xiaoyong
# Date: 2016-Dec-1
import os
import sys
import stat
import datetime
import getpass
import string
import vim


VIM_HOME = os.path.join(os.path.expanduser('~'), '.vim')
TEMPLATE_HOME = os.path.join(VIM_HOME, 'template')
TEMPLATES = {}
TEMP_FILE = '/tmp/vim_py_temp'


# list all files and directories on path `pathname`
def listdir(pathname):
  files_and_dirs = [os.path.join(pathname, entry) \
                    for entry in os.listdir(pathname)]
  files = [one_file for one_file in files_and_dirs \
           if stat.S_ISREG(os.stat(one_file).st_mode)]
  dirs = [one_dir for one_dir in files_and_dirs \
          if stat.S_ISDIR(os.stat(one_dir).st_mode)]
  if len(dirs) == 0:
    return files, dirs
  else:
    sub_files, sub_dirs = zip(*[listdir(dir) for dir in dirs])
    return sum(sub_files, files), sum(sub_dirs, dirs)


def load_templates():
 files = listdir(TEMPLATE_HOME)[0]
 global TEMPLATES
 for one_file in files:
   with open(one_file) as thefile:
     lines = thefile.readlines()
   TEMPLATES[os.path.basename(one_file)] = lines


# remove trailing white space of each line
# remove empty lines at the end of the file
def strip_trailing_white_space():
  for lineno, line in enumerate(vim.current.buffer):
    vim.current.buffer[lineno] = line.rstrip()

  while len(vim.current.buffer[-1]) == 0:
    del vim.current.buffer[-1]


def insert_template(tmplname):
  vim.current.buffer.append(TEMPLATES[tmplname], 0)


def make_comment(lines):
  comment_syntax = {
      "python": "# {text}",
      "sh": "# {text}",
      "cpp": "// {text}",
      "cxx": "// {text}",
      "c": "// {text}",
      "h": "// {text}",
      "hpp": "// {text}",
      "proto": "// {text}"
      }
  filetype = vim.eval("&filetype")
  if filetype in comment_syntax:
    comment = comment_syntax[filetype]
    if isinstance(lines, str):
      return comment.format(text=lines)
    else:
      return [comment.format(text=line) for line in lines]


# check first 5 lines, if @presto is seen,
# replace this line with copyright info
def add_presto_copyright():
  copyright = TEMPLATES['presto_copyright']
  year = datetime.datetime.now().year
  author = getpass.getuser()
  length = len(vim.current.buffer)
  if length == 0:
    return
  length = 5 if length > 5 else length
  first_line = None
  for lineno, line in enumerate(vim.current.buffer[:length]):
    if "@presto" in line.lower().strip():
      first_line = lineno
      break

  if first_line is not None:
    del vim.current.buffer[first_line]
    copyright = [line.format(year=year, author=author) \
                 for line in copyright]
    copyright = make_comment(copyright)
    vim.current.buffer.append(copyright, first_line)


def get_selected_lines():
  start_line = vim.eval('getpos("\'<")')[1]
  end_line = vim.eval('getpos("\'>")')[1]
  return int(start_line), int(end_line)-1


def get_cursor_pos():
  return int(vim.eval('getpos(".")')[1])


def save_selected():
  lineno = get_selected_lines()
  with open(TEMP_FILE, "wt") as temp_file:
    for line in vim.current.buffer[lineno[0]:lineno[1]+1]:
      temp_file.write(line+'\n')



def insert_temp_file():
  cursor_line = get_cursor_pos()
  with open(TEMP_FILE) as temp_file:
    lines = temp_file.readlines()
  vim.current.buffer.append(lines, get_cursor_pos())


# get the absolution path of the file
# associated with current buffer
def get_this_file():
  return vim.eval("expand('%:p')")


def gen_presto_guard_macro():
  this_file = get_this_file()
  topdir = get_top_git_dir()
  rpath = os.path.relpath(this_file, topdir)
  chset = string.letters + string.digits
  res = []
  for ch in rpath:
    if ch in chset:
      res.append(ch)
    else:
      res.append('_')
  macro = ''.join(res)
  return macro.upper() + '_'


def add_cpp_header_guard():
  guard_lines = ['#ifndef {}', '#define {}', '#endif  // {}']
  macro = gen_presto_guard_macro()
  guard_lines = [line.format(macro) for line in guard_lines]
  length = len(vim.current.buffer)
  if length == 0:
    return
  length = 5 if length > 5 else length
  first_line = None
  for lineno, line in enumerate(vim.current.buffer[:length]):
    if "@guard" in line.lower().strip():
      first_line = lineno
      break

  if first_line is not None:
    del vim.current.buffer[first_line]
    vim.current.buffer.append(guard_lines[:2], first_line)
    vim.current.buffer.append(guard_lines[2])


def get_top_git_dir():
  this_file = get_this_file()
  assert os.path.isabs(this_file), \
      'File name error!' % this_file
  path = this_file
  for _ in range(100):  # or use While True??
    path = os.path.split(path)[0]
    if os.path.exists(os.path.join(path, '.git')):
      return path
    elif path == '/':
      assert False, 'Current file is not in a git repository!'


def add_comment():
  start_line, end_line = get_selected_lines()
  print start_line, end_line
  comments = make_comment(vim.current.buffer[start_line-1:end_line])
  del vim.current.buffer[start_line-1:end_line]
  vim.current.buffer.append(comments, start_line-1)


def remove_comment():
  start_line, end_line = get_selected_lines()
  print start_line, end_line
  for lineno in range(start_line-1, end_line):
    line = vim.current.buffer[lineno]
    for col, char in enumerate(line):
      if char not in " #/":
          break
    vim.current.buffer[lineno] = line[col:]


if __name__ == "__main__":
  load_templates()
