from doc_instance import DocInstance


def insert_test_record(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '测试记录',
                               '测试记录', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestRecordImpl',
                                     'getFrontPages',
                                     ['projectId', 'turnId'],
                                     '【测试记录】测试记录首页',
                                     '测试记录首页')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestRecordImpl',
                                     'getTestRecords',
                                     ['projectId', 'turnId'],
                                     '【测试记录】软件测试记录表格',
                                     '软件测试记录表格')
    doc_instance.insert_break_page()
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestRecordImpl',
                                     'getTestCenterTestRecords',
                                     ['projectId', 'turnId'],
                                     '【测试记录】软件测试中心测试记录',
                                     '软件测试中心测试记录')
    return doc_instance.instance_id
