from doc_instance import DocInstance


def insert_regression_record(is_template, instance_id=None):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '回归测试记录',
                               '回归测试记录', is_template, instance_id)
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionRecord',
                                     'getFrontPages',
                                     ['projectId', 'turnId'],
                                     '【测试记录】回归测试记录首页',
                                     '回归测试记录首页')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestRecordImpl',
                                     'getTestRecords',
                                     ['projectId', 'turnId'],
                                     '【回归测试记录】软件测试记录表格',
                                     '软件测试记录表格')
    # 插入分页符
    doc_instance.insert_break_page()
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestRecordImpl',
                                     'getTestCenterTestRecords',
                                     ['projectId', 'turnId'],
                                     '【测试记录】回归测试记录表单',
                                     '回归测试记录表单')
    #doc_instance.insert_break_page()
    doc_instance.insert_header(1, '附录1 文档审查单')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getDocCheckData',
                                     ['projectId', 'turnId'],
                                     '【测试记录】附件1 文档审查单',
                                     '文档审查单')
    doc_instance.insert_break_page()
    doc_instance.insert_header(1, '附录2 代码审查单')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getCodeCheckData',
                                     ['projectId', 'turnId'],
                                     '【测试记录】附录2 代码审查单',
                                     '代码审查单')
    print(doc_instance.instance_id)
