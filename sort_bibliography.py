####################################################################################
# 2020 Jan 11
# by Free Fall
# Inspired by https://github.com/LaTeX-Bibitem-Styler/latex-bibitemstyler
####################################################################################


BEGIN_DOC_ID = r'\begin{document}'
END_DOC_ID = r'\end{document}'
BIB_BEGIN_ID = r'\begin{thebibliography}'
BIBITEM_BEGIN_ID = r'\bibitem{'
BIB_END_ID = r'\end{thebibliography}'
COMMENT_SEQUENCE = '%'
ENCODING = "utf-8"


def find_substring_skipping_comment(big_string, substring):
    start_of_comment = big_string.find(COMMENT_SEQUENCE)
    if start_of_comment != -1:
        big_string = big_string[:start_of_comment]
    return big_string.find(substring)


def split_main_file_into_parts(main_filename):
    file_lines = []
    preamble_end = None
    bib_start = None
    postamble_start = None
    with open(main_filename, 'r', encoding=ENCODING) as inf:
        line_number = 0
        for line in inf:
            # print(line)
            file_lines.append(line)
            if find_substring_skipping_comment(line, BEGIN_DOC_ID) != -1 and preamble_end is None:
                preamble_end = line_number + 1
            if find_substring_skipping_comment(line, BIBITEM_BEGIN_ID) != -1 and bib_start is None:
                bib_start = line_number
            if find_substring_skipping_comment(line, BIB_END_ID) != -1 and postamble_start is None:
                postamble_start = line_number
            line_number += 1
    preamble = file_lines[:preamble_end]
    tex_body = file_lines[preamble_end:bib_start]
    bib_body = file_lines[bib_start:postamble_start]
    postamble = file_lines[postamble_start:]
    comments = {}
    for i in range(len(tex_body)):
        comment_idx = tex_body[i].find(COMMENT_SEQUENCE)
        if comment_idx != -1:
            comments[i] = tex_body[i][comment_idx:]
            tex_body[i] = tex_body[i][:comment_idx]
    # Return
    return comments, preamble, tex_body, bib_body, postamble


def parse_tex_body(tex_body):
    cite_list = []
    for i in range(len(tex_body)):
        line = tex_body[i]
        new_line = ''
        while line.find('\\cite{') != -1:
            new_cite_idx = line.find('\\cite{') + len('\\cite{')
            new_line += line[:new_cite_idx]
            line = line[new_cite_idx:]
            end_cite_idx = line.find('}')
            temp = line[:end_cite_idx]
            line = line[end_cite_idx + 1:]
            # handle multiple keys inside single citation
            cites = temp.split(',')
            for j in range(len(cites)):
                cite = cites[j].strip()  # clear leading and trailing whitespaces
                cites[j] = cite
                if cite not in cite_list:
                    cite_list.append(cite)
            # Place the citations in the correct order
            cites.sort(key=lambda x: cite_list.index(x))
            new_line += ','.join(cites) + '}'
        new_line += line
        tex_body[i] = new_line
    return cite_list


def parse_bib_body(bib_body):
    bibitems_keys = []
    bibitems_locations = []
    for i in range(len(bib_body)):
        bibitem_begin = find_substring_skipping_comment(bib_body[i], BIBITEM_BEGIN_ID)
        if bibitem_begin != -1:
            key_start = bibitem_begin + len(BIBITEM_BEGIN_ID)
            key_end = bib_body[i].find('}', key_start)
            key = bib_body[i][key_start:key_end]
            if key in bibitems_keys:
                print(f'WARNINIG: found duplicate bibitem key: {key}')
            bibitems_keys.append(key)
            bibitems_locations.append(i)
    bibitems_locations.append(len(bib_body))
    bibitems_idx = {} # for each key it gives two values = indices of start and end
    for i in range(len(bibitems_keys)):
        bibitems_idx[bibitems_keys[i]] = (bibitems_locations[i], bibitems_locations[i+1])
    return bibitems_idx


def reassemble_bibliography_in_correct_order(cite_list, bibitems_idx, old_bib_body):
    bib_body = []
    for cite in cite_list:
        if cite in bibitems_idx.keys():
            bib_body += old_bib_body[bibitems_idx[cite][0]:bibitems_idx[cite][1]]
            del bibitems_idx[cite]
        else:
            print(f'WARNINIG: found missing bibitem key: {cite}')
    if len(bibitems_idx) != 0:
        print(f'{len(bibitems_idx)} bibitems are note cited. Do you want to include them at the end? y/n')
        responce = input().strip()
        if responce == 'y':
            for value in bibitems_idx.values():
                bib_body += old_bib_body[value[0]:value[1]]
    return bib_body


def reassemble_final_file(comments, preamble, new_tex_body, new_bib_body, postamble):
    # Paste back the comments
    for line_number in comments.keys():
        new_tex_body[line_number] += comments[line_number]
    # Assemble the file
    file_lines = preamble + new_tex_body + new_bib_body + postamble
    file_contents = ''.join(file_lines)
    return file_contents


def main():
    # Prepare io names
    data_dir = ''
    main_filename = data_dir + 'input.tex'
    output_filename = data_dir + 'output.tex'
    # Do the work
    comments, preamble, tex_body, bib_body, postamble = split_main_file_into_parts(main_filename)
    cite_list = parse_tex_body(tex_body)
    bibitems_idx = parse_bib_body(bib_body)
    new_bib_body = reassemble_bibliography_in_correct_order(cite_list, bibitems_idx, bib_body)
    new_file_contents = reassemble_final_file(comments, preamble, tex_body, new_bib_body, postamble)
    # Save the results
    with open('output.tex', 'w', encoding=ENCODING) as ouf:
        to_print = new_file_contents
        ouf.write(to_print)
    return


if __name__ == '__main__':
    main()
