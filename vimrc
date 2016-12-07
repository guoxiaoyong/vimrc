"=========================
"
" guoxiaoyong's vimrc
"
"========================

set nocompatible

set ai " auto indent
set cmdheight=2
set enc=utf8
set hls " highlight search
set incsearch
set laststatus=2
set mps+=<:>
set number " show line number
set showtabline=2
set sw=2 " shift width
set nowrap

" macos vim set modelines to 0 by default
set modeline
set modelines=10

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
