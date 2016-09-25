from doc_instance import DocInstance


def insert_problem_confirmation():
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.ProblemConfirmReport',
                                     'getXml',
                                     ['projectId'])
    print(doc_instance.instance_id)
