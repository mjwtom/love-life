from statements_template import instance_insert, metadata_insert, structure_insert, \
    clean_instance, clean_structure, clean_metadata, instance_insert


class DocInstance(object):
    def __init__(self, params, project_id):
        self.order_num = 0
        self.headers_id = []
        self.instance_id = instance_insert(params, project_id)
        self._insert_root()

    def _insert_root(self):
        structure_id = structure_insert(self.instance_id,
                                        -1,
                                        self.order_num,
                                        0, '1', 2,
                                        'root', 'document root');
        self.headers_id.append(structure_id)

    def _insert_structure(self, level, sign, name, digest, metadata_id):
        structure_id = structure_insert(self.instance_id,
                         self.headers_id[level - 1],
                         self.order_num, sign, level,
                         name, digest, metadata_id);
        if sign == '1':
            if len(self.headers_id) <= level:
                self.headers_id.append(structure_id)
            else:
                self.headers_id[level] = structure_id
        self.order_num += 1

    def insert_header(self, level, text):
        self._insert_structure(level, '1', text,
                               '文档%d的第%d级标题'
                               % (self.instance_id, level),
                               None)

    def insert_text(self, text):
        self._insert_structure(len(self.headers_id),
                               '2',
                               '文档%d的文本' % self.instance_id,
                               text, None)

    def insert_mt_structure(self, class_name, method_name, params):
        metadata_map = dict(
            className=class_name,
            methodName=method_name,
            params=params
        )
        metadata_id = metadata_insert(metadata_map)
        self._insert_structure(len(self.headers_id),
                               '2',
                               '带有metadata的项目',
                               '带有metadata的项目digest', metadata_id)

    def insert_toc(self):
        self.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                 'getSimpleToC',
                                 None);

    def insert_break_page(self):
        self.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                 'getBreakPage',
                                 None);
