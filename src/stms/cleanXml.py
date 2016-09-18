import os

file_path = 'D:\\IdeaProjects\\stms\\stms-doc-metainf\\src\\main\\resources\\docTemplate' \
            '\\accreditationReport\\DemandEvaluation\\frontPage.vm'


def cleanP(line, fin):
    pos = line.find('w14')
    next_line = line[pos:]
    line = line[:pos]
    while '>' not in next_line:
        next_line = fin.readline()
    pos = next_line.find('>')
    next_line = next_line[pos:]
    line = line + next_line
    return line


def cleanRsid(line ,fin):
    pos = line.find('w:rsid')
    next_line = line[pos:]
    line = line[:pos]
    while '>' not in next_line:
        next_line = fin.readline()
    pos = next_line.find('>')
    next_line = next_line[pos:]
    line = line + next_line
    return line


def cleanTblPrEx(line, fin):
    next_line = line
    while '/w:tblPrEx' not in next_line:
        next_line = fin.readline()


def do_clean(file_path):
    out_path = file_path + '.out'
    with open(file_path, 'r', encoding='utf-8') as fin, open(out_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            if '<w:p w14:paraId' in line:
                line = cleanP(line, fin)
            elif 'commentRange' in line:
                continue
            elif 'commentReference' in line:
                continue
            elif 'w:rsid' in line:
                line = cleanRsid(line, fin)
            elif 'tblPrEx' in line:
                cleanTblPrEx(line, fin)
                continue
            fout.write(line)
    if os.path.exists(file_path+'.old'):
        os.remove(file_path+'.old')
    os.rename(file_path, file_path + '.old')
    os.rename(out_path, file_path)

if __name__ == '__main__':
    do_clean(file_path)
