from doc_instance import DocInstance


def insert_problem(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '软件问题确认报告单',
                               '软件问题确认报告单模板',is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.ProblemConfirmReport',
                                     'getDocxXml',
                                     ['projectId', 'turnId'],
                                     '软件问题确认报告单',
                                     '软件问题确认报告读取的元数据')
    print(doc_instance.instance_id)


def insert_softwareinout(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '被测软件出入登记表',
                               '被测软件出入登记表模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.SoftwareInOut',
                                     'getDocxXml',
                                     ['projectId', 'turnId'],
                                     '软件问题确认报告单',
                                     '软件问题确认报告读取的元数据')
    print(doc_instance.instance_id)
