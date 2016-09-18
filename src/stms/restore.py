import os

file_path = 'D:\\IdeaProjects\\stms\\stms-doc-metainf\\src' \
            '\\main\\resources\\docTemplate\\accreditationReport\\contractAccreditationReport\\frontPage.vm'

if os.path.exists(file_path+'.old'):
    os.remove(file_path)
os.rename(file_path+'.old', file_path)
