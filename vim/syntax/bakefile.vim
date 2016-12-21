" Copyright 2008 prestolabs.
" Author: xguo
" Usage:
" 1. cp proto.vim ~/.vim/syntax/
" 2. Add the following to ~/.vimrc:
"
" augroup filetype
"   au! BufRead,BufNewFile *.bakefile bakefile setfiletype bakefile
" augroup end
"

if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syn keyword bkRule cc_library cc_binary cc_test gen_proto
syn keyword bkVariables name srcs deps data
syn region  bkComment start="#" skip="\\$" end="$" 
syn region  bkString  start=/"/ skip=/\\"/ end=/"/
syn region  bkString  start=/'/ skip=/\\'/ end=/'/

if version >= 508 || !exists("did_proto_syn_inits")
  if version < 508
    let did_proto_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif

  HiLink bkRule         Function 
  HiLink bkVariables    Keyword
  HiLink bkComment      Comment
  HiLink bkString       String

  delcommand HiLink
  endif

  let b:current_syntax = "bakefile"
