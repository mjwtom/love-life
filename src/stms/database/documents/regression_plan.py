from doc_instance import DocInstance


def insert_regression_plan(is_template, instance_id=None):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '回归测试计划',
                               '回归测试计划', is_template, instance_id)
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getFrontPages',
                                     ['projectId', 'turnId'],
                                     '【测试计划】回归测试计划首页',
                                     '回归测试计划首页')
    doc_instance.insert_toc()
    # doc_instance.insert_break_page()
    doc_instance.insert_header(1, "范围")
    doc_instance.insert_header(2, '标识')
    doc_instance.insert_text("a）已批准的文档标识号：${_instance_identifier}")
    doc_instance.insert_text("b）标题：${_product_softwareName}回归测试说明")
    doc_instance.insert_text("c）本文档使用的系统为${_product_systemName}，"
                             "适用的软件配置项为：${_product_softwareName}（${_instance_version}） 。")
    doc_instance.insert_header(2, '系统概述')
    doc_instance.insert_text("${_product_softwareName}（${_instance_version}）与${_instance_version}（V1.0）的所在系统情况一致，"
                             "参见${_instance_version}测评大纲（定型/鉴定测评大纲）。 ")
    doc_instance.insert_header(2, '文档概述')
    doc_instance.insert_text('本回归测试计划的内容包括XXX软件回归测试的范围、测试项目、测试方法、测试进度和人员安排等，同时：')
    doc_instance.insert_text('a）为本回归测试的管理工作提供指南，为回归测试说明设计提供技术依据；')
    doc_instance.insert_text('b）确定回归测试的内容和通过准则；')
    doc_instance.insert_text('c）进行回归测试活动及进度安排与策划，提出对回归测试环境、设备、器材、组织机构以及人员等的需求。 ')

    doc_instance.insert_header(1, '引用文件')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getReferenceDocument',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】引用文件表',
                                     '回归测试计划引用文件表')
    doc_instance.insert_header(1, '术语和缩略语')
    #此处来源于测试大纲的术语和缩略语
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'productTermAndAbbreList',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】术语和缩略语表',
                                     '回归测试计划术语和缩略语表')
    doc_instance.insert_header(1, '软件回归测试环境')
    doc_instance.insert_text("${_product_softwareName}（${_instance_version}）与${_instance_version}（V1.0）的所在系统情况一致，"
                             "参见${_instance_version}测评大纲（定型/鉴定测评大纲）。 ")
    doc_instance.insert_header(2, '软硬件环境')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTestEnvironment',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】测试环境',
                                     '测试环境')
    doc_instance.insert_header(1, '回归测试内容与方法')
    doc_instance.insert_header(2, '测试类型和测试策略')
    doc_instance.insert_text('配置项测试已进行下列测试类型的测试：文档审查、静态测试、功能测试、接口测试、人机交互界面测试、强度测试、安全性测试、恢复性测试、安装性测试。'
                             '由于xx，故在回归测试中不做xx测试，需进行的测试类型为：xx。')
    doc_instance.insert_text('按照上述测试类型选择全部可用的配置项测试用例，对${_product_softwareName}（${_instance_version}）进行回归测试。')
    doc_instance.insert_text('上述测试类型的测试要求和标识与配置项测试的测试要求和标识一致，参见${_product_softwareName}测评大纲（定型/鉴定测评大纲）。')
    doc_instance.insert_text('根据回归测试项目的实际情况，以人工测试为主，辅以相关的测试工具，采用黑盒测试和白盒测试相结合的回归测试策略。 ')
    doc_instance.insert_header(2, '测试项及测试方法')
    doc_instance.insert_text('回归测试的测试项有如下变更，其它未变更的测试项和优先级参见${_product_softwareName}测评大纲（定型/鉴定测评大纲）。 ')
    doc_instance.insert_header(3, '文档审查（XXX_WDS）')
    doc_instance.insert_text('委托方提交的文档有如下变更：')
    doc_instance.insert_text('1.	xx。')
    doc_instance.insert_text('2.	xx。')
    doc_instance.insert_text('变更的文档审查测试项具体见表5 - X。（未变更名称的和删去的测试项不再赘述）')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getDocumentRivision',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】文档审查测试项内容',
                                     '回归测试计划文档审查测试项内容表')
    doc_instance.insert_header(3, '代码审查（XXX_DMS）')
    doc_instance.insert_text('代码审查测试项有如下变更：')
    doc_instance.insert_text('1.	根据${_product_softwareName}（${_instance_version}）需求规格说明，增加主控程序代码审查。')
    doc_instance.insert_text('2.	根据问题影响域分析说明，删去中断服务程序1代码审查测试项。')
    doc_instance.insert_text('变更的代码审查测试项，具体见表5-X。（未变更名称的和删去的测试项不再赘述）')
    doc_instance.insert_text('代码审查单参见${_product_softwareName}测评大纲 （定型/鉴定测评大纲）。')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getCodeRevision',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】文档审查测试项内容',
                                     '回归测试计划文档审查测试项内容表')
    doc_instance.insert_header(3, '静态分析（XXX_JTF）')
    doc_instance.insert_text('静态分析有如下变更：')
    doc_instance.insert_text('1.	根据${_product_softwareName}（${_instance_version}）需求规格说明，增加对主控程序的静态分析。')
    doc_instance.insert_text('2.	根据问题影响域分析说明，对中断服务程序1不进行静态分析。')
    doc_instance.insert_text('测试项仍为控制流分析、数据流分析、接口特性分析、软件质量特性度量，优先级不变，'
                             '参见${_product_softwareName}测评大纲（定型/鉴定测评大纲）。 ')
    doc_instance.insert_header(3, '功能测试（XXX_GNC）')
    doc_instance.insert_text('功能测试有如下变更：')
    doc_instance.insert_text('1.	根据XXX软件（VX.X）需求规格说明，增加功能10测试项。')
    doc_instance.insert_text('2.	根据问题影响域分析说明，删去功能9测试项。')
    doc_instance.insert_text('3.	已有的功能9测试项增加xx内容。')
    doc_instance.insert_text('变更的功能测试项，具体见表5-X。（未变更名称的和删去的测试项不再赘述）')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getFunctionRevision',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】文档审查测试项内容',
                                     '回归测试计划文档审查测试项内容表')
    doc_instance.insert_header(3, 'XX测试（XXX_XXC）')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTestTypeAndMethod',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】测试类型及方法',
                                     '回归测试计划测试类型及方法')
    doc_instance.insert_header(1, '测试人员安排')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getWorkers',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】测试人员安排',
                                     '回归测试计划测试人员安排表')
    doc_instance.insert_header(1, '回归测试进度')
    doc_instance.insert_text('根据以往的回归测试经验、被测试软件规模和复杂程度，估计X个测试人员大约需要XX个工作日才能完成回归测试。'
                             '其中回归测试需求分析和回归测试策划大概需要XX天，回归测试设计和实现大概需要XX天，回归测试执行大概需要XX天，'
                             '回归测试总结大概需要XX天')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getProgressPlan',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】测试进度计划',
                                     '回归测试计划测试进度计划表')
    doc_instance.insert_header(1, '风险分析')
    doc_instance.insert_text('回归测试的测试项有如下变更，其它未变更的测试项和优先级参见${_product_softwareName}测评大纲（定型/鉴定测评大纲）。 ')
    doc_instance.insert_header(1, '测试项与有关文档的追踪关系')
    doc_instance.insert_text('新增测试项与有关文档追踪的对应关系具体见表10-1，其它未变更的对应关系参见${_product_softwareName}测评大纲（定型/鉴定测评大纲）。 ')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                    'getDocumentRelationship',
                                    ['projectId', 'turnId'],
                                    '【回归测试计划】测试项与有关文档追踪的对应关系',
                                    '回归测试计划测试项与有关文档追踪的对应关系表')
    doc_instance.insert_header(1, '回归测试任务结束条件')
    doc_instance.insert_text('以下条件满足任意一条时，可以结束回归测试任务：')
    doc_instance.insert_text('a）测试发现的问题均已整改正确，未发现新引入问题或回归测试发现的新引入问题也已整改正确。')
    doc_instance.insert_text('b）若有问题未整改，分析原因并在测试报告中说明。 ')
    doc_instance.insert_header(1, '回归测试的生成文档')
    doc_instance.insert_header(2, '技术文档和技术记录')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getDocumentRecord',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】技术文档和技术记录',
                                     '回归测试计划技术文档和技术记录一览表')
    doc_instance.insert_header(2, '管理记录')
    doc_instance.insert_mt_structure('com.stms.tps.doc.regression.RegressionPlan',
                                     'getManagement',
                                     ['projectId', 'turnId'],
                                     '【回归测试计划】管理记录一览表',
                                     '回归测试计划管理记录一览表')
    print(doc_instance.instance_id)
