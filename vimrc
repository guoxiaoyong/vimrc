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
set ruler

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

colorscheme yjsimple

"colorscheme darkblue

set path+=$HOME/work/navi/**
set tags+=$HOME/tags/tags

pyfile ~/.vim/vim_plugin.py

" Protocol Buffers syntax.
augroup filetype
au! BufRead,BufNewFile *.proto
augroup end

" Bakefile syntax
augroup filetype
au! BufRead,BufNewFile *.bakefile :setlocal filetype=bakefile
au! BufRead,BufNewFile bakefile :setlocal filetype=bakefile
augroup end

vmap sy :py save_selected() <Enter>
nmap sp :py insert_temp_file() <Enter>

" Automatically removes trailing whitespaces before writing.
function! Action_on_bufwrite()
  py add_presto_copyright()
  py add_cpp_header_guard()
  py strip_trailing_white_space()
endfunction

autocmd BufWritePre *.sh,*.cxx,*.hpp,*.cpp,*.c,*.cc,*.h,*.proto,*.py,*.bakefile :call Action_on_bufwrite()
