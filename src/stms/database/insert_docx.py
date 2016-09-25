from db_util import MysqlClient
from doc_instance import DocInstance
from statements_template import clean_instance, clean_structure, clean_metadata
from form import insert_problem_confirmation

conf = dict(
    host='115.28.239.239',
    user='trhz',
    password='zhimakaimen',
    port=3306,
    database='trhz',
    charset='utf8'
)


def clean():
    client = MysqlClient(conf)
    sql = clean_instance()
    client.execute(sql)
    sql = clean_structure()
    client.execute(sql)
    sql = clean_metadata()
    client.execute(sql)
    client.close()


def insert_test_report():
    param_map = dict(
        projectId="13",
        testTurn="1"
    )

    doc_instance = DocInstance(param_map, 13)
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getFrontPages',
                                     ['projectId'])
    doc_instance.insert_break_page()
    doc_instance.insert_toc()
    doc_instance.insert_break_page()
    doc_instance.insert_header(1, '范围')
    doc_instance.insert_header(2, '标识')
    doc_instance.insert_text('1) 文档标识号：XXXX-RJCP-CPDG-XXXX 。')
    doc_instance.insert_text('2) 标题： YYYYYYYY软件定型/鉴定测评大纲 。')
    doc_instance.insert_text('3) 被测件：YYYYYYYY软件 ，各软件配置项信息及标识见表1-1。')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getVersionInformation',
                                     ['projectId'])
    doc_instance.insert_text('4)术语和缩略语')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTerms',
                                     ['projectId'])
    doc_instance.insert_header(2, '文档概述')
    doc_instance.insert_text('本文档内容包括：1.范围；2.引用文档；3.测评概述；4.测试结果；5.评价结论与改进建议；6.其他。')
    doc_instance.insert_text('文档标识本文档适用于XXXXXXXX系统YYYYYYYY软件定型/鉴定 测评，是XXXXXXXX系统YYYYYYYY软件定型/鉴定 的依据 。')
    doc_instance.insert_header(2,'委托方的名称与联系方式')
    doc_instance.insert_text('委托方的名称：海定委办公室；\n'
                            '委托方地址：XXXXXXXXXX；\n'
                            '委托方联系人：XXX；\n'
                            '委托方联系人电话：010-XXXXXX。')
    doc_instance.insert_header(2, '承研单位的名称与联系方式 ')
    doc_instance.insert_text('承研单位名称：XXXXXXXXXX；\n'
                            '承研单位地址：XXXXXXXXXX；\n'
                            '承研单位联系人：XXX；\n'
                            '承研单位联系人电话：XXX-XXXXXX。')
    doc_instance.insert_header(2, '定型/鉴定 测评机构的名称与联系方式')
    doc_instance.insert_text('定型测评机构名称：中国船舶工业软件测试中心；\n'
                            '定型测评机构地址：江苏省连云港市圣湖路18号；\n'
                            '定型测评机构联系人：孙志安；\n'
                            '定型测评机构联系人电话：18036671781。\n')
    doc_instance.insert_header(2, '被测软件概述')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTpsProductSpec',
                                     ['projectId'])
    doc_instance.insert_header(1, '引用文件')
    doc_instance.insert_header(2, '管理类文件')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getManagementDocuments',
                                     ['projectId'])
    doc_instance.insert_header(2,'顶层文件')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTopTechnologyDocuments',
                                     ['projectId'])
    doc_instance.insert_header(2, '被测软件文档')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getSoftwareDocuments',
                                     ['projectId'])
    doc_instance.insert_header(2, '其他文档')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getOtherDocuments',
                                     ['projectId'])
    doc_instance.insert_header(1, '测评概述')
    doc_instance.insert_header(2, '测评过程概述')
    doc_instance.insert_text('软件定型 / 鉴定'
                        '测评工作分为测试需求分析、测试策划、测试设计和实现、测试执行、测试总结五个测试阶段进行，测试的主要时间节点及工作内容见表3 - 1。此次定型 / 鉴定'
                        '测评分包单位为XXXX，承担UUUU软件测评工作。')
    doc_instance.insert_header(2, '测评环境说明')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTestEnvironment',
                                     ['projectId'])
    doc_instance.insert_header(2, '测评方法说明')
    doc_instance.insert_header(3, '测试方法')
    doc_instance.insert_text('测试组选取的测试类型和测试方法要求详见表3-12。')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTestTypeAndMethod',
                                     ['projectId'])
    doc_instance.insert_header(3, '测试工具')
    doc_instance.insert_text('测试工具详见表3-13。')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getTestTools',
                                     ['projectId'])
    doc_instance.insert_header(1, '测试结果')
    doc_instance.insert_header(2, '测试执行情况')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getExecuteResult',
                                     ['projectId'])
    doc_instance.insert_header(2, '软件问题')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getSoftwareProblem',
                                     ['projectId'])
    doc_instance.insert_header(3, '回归测试问题')
    doc_instance.insert_text('回归测试新增软件问题见表4-20。')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getRegressionProblem',
                                     ['projectId'])
    doc_instance.insert_header(3, '遗留问题')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getLeftProblem',
                                     ['projectId'])
    doc_instance.insert_header(2, '测试的有效性、充分性说明')
    text = '''
（1）此次测试符合《军用软件产品定型/鉴定管理办法》和《海军装备软件质量管理办法》的要求，测试过程严格受控，符合《军用软件测评实验室测评过程和技术能力要求》的规定；
（2）完成了《XXXXX测评大纲 》规定的测试内容，测试环境满足测试要求，测试方法和测试用例合理并通过了审查；
（3）测试过程中，严格按照有关的保密要求开展工作，确保被测件、测试产品的安全；
（4）测试过程中，测试工具及测试设备完好；
（5）根据《XX研制总要求 》和软件承制方提供的被测软件需求规格说明和设计文档，整理出XX个软件需求，XX个隐含需求。
由软件需求分析出XX个测试需求，其中文档审查需求XX个，静态测试需求XX个，功能测试需求XX个，性能测试需求XX个，接口测试需求XX个，余量测试需求XX个，边界测试需求XX个，
人机界面测试XX个，强度测试XX个，安全性测试XX个，…… 。
测试需求覆盖了《XX研制总要求 》中关于软件的要求和软件需求规格说明及其他等效文档中关于软件功能、性能等全部的书面需求和隐含需求。编写测试用例表单XX组，覆盖全部软件测试需求。
用例执行情况见附录C。'''
    doc_instance.insert_text(text)
    doc_instance.insert_header(1, '评价结论与改进建议')
    doc_instance.insert_header(2, '评价结论')
    doc_instance.insert_header(3, '软件功能性能达标情况')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getPass',
                                     ['projectId'])
    doc_instance.insert_header(3, '测评结论')
    doc_instance.insert_mt_structure('com.stms.tps.doc.TestReportImpl',
                                     'getSystemSoftware',
                                     ['projectId'])
    print("doc instance id %s" % doc_instance.instance_id)


if __name__ == '__main__':
    clean()
    insert_test_report()
    #insert_problem_confirmation()
