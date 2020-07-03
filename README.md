# Bibliography ordering in LaTeX documents

This package is intendend for ordering the bibliography in LaTeX documents.
If you have your entire document content and all the bibliography items in one file,
you can use this package to sort the bibitems in the order that they appear in the text.
This package also takes care of ordering multiple citations, e.g. commands like `\cite{key1,key2,key3}`.



#### Usage

1. Put your entire document content (including the `thebibliography` part) in the file `input.txt` (in the same folder as this project)
2. Run `sort_bibliography.py`. If there are unused bibitems, the program will ask whether to keep them or not; in that case, type `y` for yes, `n` for no, and then hit `Enter`.
3. Collect your document with sorted bibliography from `output.tex`


In the current version, the file `input.txt` already has some sample content, as well as the corresponding pdf file.
To test the program, simply run `sort_bibliography.py`.
Or simply see the results in `output.tex` (and in the corresponding pdf file).


#### Additional notes

Compared to some other packages of this sort, this one has several advantages:
- It completely ignores the parts commented out by `%`
- Supports the UTF-8 encoding
- If there are duplicate bibitem keys, the program will give a warning
- This package also takes care of ordering multiple citations like `\cite{key1,key2,key3}`

There are also several drawbacks:
- The input filename is fixed
- The whole document contents must be contained in a single file

However, these almost never pose a problem in a regular research article.

#### History and acknowledgements

This project is inspired by
https://github.com/LaTeX-Bibitem-Styler/latex-bibitemstyler .

- 2020.01 Started development in the course of the projects, 
supported by 
the Russian Foundation for Basic Research according to the research projects
No. 18-32-00015 and No. 18-02-00048, 
and by the Foundation for the Advancement of Theoretical Physics and Mathematics "BASIS" according to
the research project No. 19-1-5-106-1 
- 2020.07 A few minor improvements