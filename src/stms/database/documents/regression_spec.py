from doc_instance import DocInstance


def insert_regression_spec(is_template):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '回归测试说明',
                               '回归测试说明', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionSpecification',
                                     'getFrontPages',
                                     ['projectId', 'turnId'],
                                     '【测试说明】回归测试说明首页',
                                     '回归测试说明首页')
    doc_instance.insert_toc()
    #doc_instance.insert_break_page()
    doc_instance.insert_header(1, "范围")
    doc_instance.insert_header(2, '标识')
    doc_instance.insert_text("a）已批准的文档标识号：${_instance_identifier}")
    doc_instance.insert_text("b）标题：${_product_softwareName}回归测试说明")
    doc_instance.insert_text("c）本文档使用的系统为${_product_systemName}，"
                             "适用的软件配置项为：${_product_softwareName}（${_instance_version}） 。")
    doc_instance.insert_header(2, '系统概述')
    doc_instance.insert_text("${_product_softwareName}（${_instance_version}）与${_instance_version}（V1.0）的所在系统情况一致，"
                             "参见${_instance_version}测评大纲（定型/鉴定测评大纲）。 ")
    doc_instance.insert_header(2,'文档概述')
    text = '本文档是对${_product_softwareName}行配置项测试的回归测试说明，' \
           '根据该被测软件需求规格说明、操作手册等输入条件拟制。' \
           '本文档根据测评大纲中提出的测试条目安排测试进度、准备测试的软件和硬件环境，' \
           '并在此基础上设计详细的测试用例，包括测试输入设计、测试操作设计、期望测试结果等。'
    doc_instance.insert_text(text)
    doc_instance.insert_header(1, '引用文件')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionSpecification',
                                     'getReferenceDocuments',
                                     ['projectId', 'turnId'],
                                     '【回归测试说明】引用文件表',
                                     '回归测试说明引用文件表')
    doc_instance.insert_header(1, '术语和缩略语')
    # 此处来源于测试大纲的术语和缩略语
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'productTermAndAbbreList',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】术语和缩略语表',
                                     '回归测试计划术语和缩略语表')
    doc_instance.insert_header(1, '正式合格性测试准备')
    doc_instance.insert_header(2, '硬件资源')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestSpecificationImpl',
                                     'getHardwareResources',
                                     ['projectId', 'turnId'],
                                     '【回归测试说明】硬件资源表',
                                     '硬件资源表')
    doc_instance.insert_header(2, '软件资源')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestSpecificationImpl',
                                     'getSoftwareResources',
                                     ['projectId', 'turnId'],
                                     '【回归测试说明】软件资源表',
                                     '软件资源表')
    # 由metadata统一生成，正式合格性测试说明
    # doc_instance.insert_header(1, '正式合格性回归测试说明')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestSpecificationImpl',
                                     'getFuction',
                                     ['projectId', 'turnId'],
                                     '【回归测试说明】正式合格性回归测试说明',
                                     '回归测试说明 正式合格性回归测试说明')
    doc_instance.insert_header(1, '回归测试说明与回归测试计划的追踪关系')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionSpecification',
                                     'getTrackRelationship',
                                     ['projectId', 'turnId'],
                                     '【回归测试说明】回归测试说明与回归测试计划的追踪关系',
                                     '回归测试说明与回归测试计划的追踪关系')
    doc_instance.insert_header(1, '测试用例执行顺序')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestSpecificationImpl',
                                     'getTestCaseOrder',
                                     ['projectId', 'turnId'],
                                     '【回归测试说明】测试用例执行顺序',
                                     '测试用例执行顺序')

    print(doc_instance.instance_id)
