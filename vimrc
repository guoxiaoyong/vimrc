"=========================
"
" guoxiaoyong's vimrc
"
"========================

set number
set modeline
set modelines=10
set showtabline=2
set laststatus=2
set cmdheight=2
set mps+=<:>
set tabstop=4
set expandtab

colorscheme darkblue

nmap <C-\> ma:%!astyle<Enter>`a
nmap ) ma:%!iconv -f gbk -t utf8<Enter>`a
nmap ( ma:%!dos2unix<CR>`a

" set path+=$HOME/path/**
" set tags+=$HOME/tags/tags

function! Loadtmpl(tmpl_file, pattern)
    let tmpl = readfile(a:tmpl_file)
    let skel = ''
    for n in tmpl
        let skel = skel . n . "<CR>" 
    endfor
    execute "iab " . a:pattern . " " . skel 
endfunction

let s:tmpls = [['skel.cpp', 'cxxx'], ['skel.c', 'cccc']]

for s:n in s:tmpls
    let s:f = $HOME . "/.vim/" . s:n[0]
    call Loadtmpl(s:f, s:n[1])
endfor

