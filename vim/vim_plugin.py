# Author: Xiaoyong
# Date: 2016-Dec-1
import os
import sys
import stat
import datetime
import getpass
import vim


VIM_HOME = os.path.join(os.path.expanduser('~'), '.vim')
TEMPLATE_HOME = os.path.join(VIM_HOME, 'template')
TEMPLATES = {}


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
 files, _ = listdir(TEMPLATE_HOME)
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
      "cpp": "// {text}",
      "c": "// {text}"}
  filetype = vim.eval("&filetype")
  if filetype in comment_syntax:
    comment = comment_syntax[filetype]
    if isinstance(lines, str):
      return comment.format(text=lines)
    else:
      return [comment.format(text=line) for line in lines]


def add_presto_copyright():
  copyright = TEMPLATES['presto_copyright']
  year = datetime.datetime.now().year
  author = getpass.getuser()
  first_line = vim.current.buffer[0].lower().strip()
  if "@presto" in first_line:
    del vim.current.buffer[0]
    for lineno, line in enumerate(copyright):
      line = line.format(year=year, author=author)
      line = make_comment(line)
      vim.current.buffer.append(line, lineno)


if __name__ == "__main__":
  load_templates()
