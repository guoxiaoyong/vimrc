"=========================
"
" guoxiaoyong's vimrc
"
"========================

set nocompatible

set ai
set cmdheight=2
set enc=utf8
set hls
set incsearch
set laststatus=2
set modeline
set modelines=10
set mps+=<:>
set number
set showtabline=2
set sw=2
set nowrap

" set listchars
set listchars=trail:.,tab:>-
set list

" convert tab to spaces
set tabstop=2
set expandtab

" for macos, syntax is off by default
syntax enable

colorscheme darkblue

set path+=$HOME/work/navi/**
set tags+=$HOME/tags/tags

pyfile ~/.vim/vim_plugin.py

" Protocol Buffers syntax.
augroup filetype
au! BufRead,BufNewFile *.proto
augroup end

" Automatically removes trailing whitespaces before writing.
function! Action_on_bufwrite()
  py add_presto_copyright()
  py strip_trailing_white_space()
endfunction

autocmd BufWritePre *.sh,*.cxx,*.hpp,*.cpp,*.cc,*.h,*.proto,*.py,*.bakefile :call Action_on_bufwrite()
