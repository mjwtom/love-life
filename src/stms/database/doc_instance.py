from statements_template import template_insert, metadata_insert, template_structure_insert, \
    get_break_page_metada_id, get_table_of_content_metada_id
from statements import instance_insert, structure_insert


class DocInstance(object):
    def __init__(self, params, project_id, name='test',
                 digest='test', is_template=False):
        self.order_num = 0
        self.headers_id = []
        self.name = name
        self.last_level = -1
        if is_template:
            self.instance_id = template_insert(name, digest)
        else:
            self.instance_id = instance_insert(params, project_id, name, digest)
        self.is_template = is_template
        self._insert_root(name+'的root节点', digest+'的root节点')

    def _insert_root(self, name='root', digest='document root'):
        if self.is_template:
            structure_id = template_structure_insert(self.instance_id,
                                                     -1,
                                                     -1,
                                                     '1', 0,
                                                     name, digest)
        else:
            structure_id = structure_insert(self.instance_id,
                                        -1,
                                        -1,
                                        '1', 0,
                                        name, digest)
        self.headers_id.append(structure_id)
        self.last_level += 1

    def _insert_structure(self, level, sign, name, digest, metadata_id):
        if self.is_template:
            structure_id = template_structure_insert(self.instance_id,
                                                     self.headers_id[level-1],
                                                     self.order_num, sign,
                                                     level, name, digest,
                                                     metadata_id)
        else:
            structure_id = structure_insert(self.instance_id,
                         self.headers_id[level - 1],
                         self.order_num, sign, level,
                         name, digest, metadata_id)
        if sign == '1':
            if len(self.headers_id) <= level:
                self.headers_id.append(structure_id)
            else:
                self.headers_id[level] = structure_id
            self.last_level = level
        print('structure order %d' % self.order_num)
        self.order_num += 1

    def insert_header(self, level, text):
        self._insert_structure(level, '1', text,
                               '文档%s的第%d级标题'
                               % (self.name, level),
                               None)

    def insert_text(self, text):
        self._insert_structure(self.last_level+1,
                               '2',
                               '文档%s的文本' % self.name,
                               text, None)

    def insert_mt_structure(self, class_name, method_name, params, name, digest):
        metadata_map = dict(
            className=class_name,
            methodName=method_name,
            params=params
        )
        metadata_id = metadata_insert(metadata_map, name, digest)
        self._insert_structure(self.last_level+1,
                               '2',
                               name,
                               digest, metadata_id)

    def insert_toc(self):
        id = get_table_of_content_metada_id()
        self._insert_structure(len(self.headers_id),
                               '2',
                               '文档%s的目录' % self.name,
                               '文档%s的目录' % self.name, id)

    def insert_break_page(self):
        id = get_break_page_metada_id()
        self._insert_structure(len(self.headers_id),
                               '2',
                               '文档%s的分页符' % self.name,
                               '文档%s的分页符' % self.name, id)
