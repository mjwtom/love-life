#!/usr/bin/env python

'''
Used to test the performance of document generation
'''

from doc_instance import DocInstance


def insert_test_report(is_template=False):
    param_map = dict(
        projectId="performance_test",
        testTurn="1"
    )

    doc_instance = DocInstance(param_map, 13, '文档生成性能测试',
                               '软件测评报告', is_template)
    for _ in range(0, 10):
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getFrontPages',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】测试大纲首页', '测试大纲首页')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getRevisionHistory',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】修订历史记录', '修订历史记录')
        doc_instance.insert_break_page()
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getDeclaration',
                                     None,
                                     '【测试大纲】有效性声明', '有效性声明')
        doc_instance.insert_toc()
        #doc_instance.insert_break_page()
        doc_instance.insert_header(1, '范围')
        doc_instance.insert_header(2, '标识')
        doc_instance.insert_text('1) 文档标识号：${_instance_identifier}。')
        doc_instance.insert_text('2) 标题： ${_product_softwareName}定型/鉴定测评报告。')
        doc_instance.insert_text('3) 适用的软件及版本：${_product_systemName}${_product_softwareName}。')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getVersionInformation',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】版本信息', '测试大纲版本信息')
        doc_instance.insert_text('4)术语和缩略语')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getTerms',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】术语和缩略语', '术语和缩略语')
        doc_instance.insert_header(2, '文档概述')
        doc_instance.insert_text('本文档内容包括：1.范围；2.引用文档；3.测评概述；4.测试结果；5.评价结论与改进建议；6.其他。')
        doc_instance.insert_text('文档标识本文档适用于XXXXXXXX系统YYYYYYYY软件定型/鉴定 测评，是XXXXXXXX系统YYYYYYYY软件定型/鉴定 的依据 。')
        doc_instance.insert_header(2,'委托方的名称与联系方式')
        doc_instance.insert_text('委托方的名称：${xxxx}；')
        doc_instance.insert_text('委托方地址：XXXXXXXXXX；')
        doc_instance.insert_text('委托方联系人：XXX；')
        doc_instance.insert_text('委托方联系人电话：010-XXXXXX。')
        #
        doc_instance.insert_header(2, '承研单位的名称与联系方式 ')
        doc_instance.insert_text('承研单位名称：${_project_partAOrgName}；')
        doc_instance.insert_text('承研单位地址：${_project_partAOrgAddress}；')
        doc_instance.insert_text('承研单位联系人：${_project_partAOrgManager}；')
        doc_instance.insert_text('承研单位联系人电话：${_project_partAOrgManagerPN}。')
        doc_instance.insert_header(2, '定型/鉴定 测评机构的名称与联系方式')
        doc_instance.insert_text('定型测评机构名称：中国船舶工业软件测试中心；')
        doc_instance.insert_text('定型测评机构地址：江苏省连云港市圣湖路18号；')
        doc_instance.insert_text('定型测评机构联系人：孙志安；')
        doc_instance.insert_text('定型测评机构联系人电话：18036671781。')
        #
        #doc_instance.insert_header(2, '被测软件概述')
        #以下自动迭代生成被测软件概述
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getTpsProductSpec',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】被测软件概述', '【测试大纲】被测软件概述')
        #以下是引用文件
        doc_instance.insert_header(1, '引用文件')
        doc_instance.insert_header(2, '管理类文件')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getManagementDocuments',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】管理类文件表格', '管理类文件表格')
        doc_instance.insert_header(2,'顶层文件')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getTopTechnologyDocuments',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】顶层技术文件', '顶层技术文件表格')
        doc_instance.insert_header(2, '被测软件文档')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getSoftwareDocuments',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】被测软件文档', '被测软件文档')
        doc_instance.insert_header(2, '其他文档')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getOtherDocuments',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】其他文档', '其他文档')
        #测评概述
        doc_instance.insert_header(1, '测评概述')
        doc_instance.insert_header(2, '测评过程概述')
        doc_instance.insert_text('软件定型 / 鉴定'
                        '测评工作分为测试需求分析、测试策划、测试设计和实现、测试执行、测试总结五个测试阶段进行，测试的主要时间节点及工作内容见表3 - 1。此次定型 / 鉴定'
                        '测评分包单位为XXXX，承担${_product_softwareName}测评工作。')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getNodeAndWorkContent',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】测试主要节点及工作内容', '测试主要节点及工作内容')

        #测评环境说明
        doc_instance.insert_header(2, '测评环境说明')
        #以下调用函数，自动生成测试环境
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getTestEnvironment',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】测试环境',
                                     '测试环境说明')

        #测评方法说明
        doc_instance.insert_header(2, '测评方法说明')
        doc_instance.insert_header(3, '测试方法')
        doc_instance.insert_text('测试组选取的测试类型和测试方法要求详见表3-12。')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getTestTypeAndMethod',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】测试类型及测试方法',
                                     '测试类型及测试方法表格')

        #测试工具
        doc_instance.insert_header(3, '测试工具')
        doc_instance.insert_text('测试工具详见表3-13。')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getTestTools',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】测试工具说明表格',
                                     '测试工具说明表格')

        #测试结果
        doc_instance.insert_header(1, '测试结果')
        doc_instance.insert_header(2, '测试执行情况')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getExecuteResult',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】测试结果执行情况总汇',
                                     '测试结果执行情况总汇')

        #以下是测试问题
        doc_instance.insert_header(2, '软件问题')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getSoftwareProblem',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】软件项测试问题统总汇',
                                     '软件项测试问题统计总汇：包括文字和表格')
        doc_instance.insert_header(3, '回归测试问题')
        doc_instance.insert_text('回归测试新增软件问题见表4-20。')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getRegressionProblem',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】软件回归测试问题表格',
                                     '软件回归测试问题表格')
        doc_instance.insert_header(3, '遗留问题')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getLeftProblem',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】遗留问题统计表格',
                                     '遗留问题统计表格')
        doc_instance.insert_header(2, '测试的有效性、充分性说明')
        doc_instance.insert_text('（1）此次测试符合《军用软件产品定型/鉴定管理办法》和《海军装备软件质量管理办法》的要求，测试过程严格受控，符合《军用软件测评实验室测评过程和技术能力要求》的规定；')
        doc_instance.insert_text('（2）完成了《XXXXX测评大纲 》规定的测试内容，测试环境满足测试要求，测试方法和测试用例合理并通过了审查；')
        doc_instance.insert_text('（3）测试过程中，严格按照有关的保密要求开展工作，确保被测件、测试产品的安全；')
        doc_instance.insert_text('（4）测试过程中，测试工具及测试设备完好；')
        text = '（5）根据《XX研制总要求 》和软件承制方提供的被测软件需求规格说明和设计文档，整理出XX个软件需求，XX个隐含需求。由软件需求分析出XX个测试需求，其中文档审查需求XX个，静态测试需求XX个，功能测试需求XX个，性能测试需求XX个，接口测试需求XX个，余量测试需求XX个，边界测试需求XX个，'\
            '人机界面测试XX个，强度测试XX个，安全性测试XX个，…… 。' \
            '测试需求覆盖了《XX研制总要求 》中关于软件的要求和软件需求规格说明及其他等效文档中关于软件功能、性能等全部的书面需求和隐含需求。编写测试用例表单XX组，覆盖全部软件测试需求。' \
            '用例执行情况见附录C。'
        doc_instance.insert_text(text)
        doc_instance.insert_header(1, '评价结论与改进建议')
        doc_instance.insert_header(2, '评价结论')
        doc_instance.insert_header(3, '软件功能性能达标情况')
        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getPass',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】软件主要功能性能达标情况表',
                                     '软件主要功能性能达标情况表')
        doc_instance.insert_header(3, '测评结论')
        doc_instance.insert_text('XXXX系统XXX软件实现了研制要求（来源于项目管理）')
        doc_instance.insert_text('软件功能实现比F=100%')
        doc_instance.insert_text('软件的余量满足指标要求，如存储空间余量、处理时间余量等')
        doc_instance.insert_text('千行程序注视率为x%，满足注视率>=20%的要求')

        doc_instance.insert_mt_structure('com.stms.tps.doc.TestOutlineImpl',
                                     'getSystemSoftware',
                                     ['projectId', 'turnId'],
                                     '【测试大纲】总结中的系统和软件列表',
                                     '测试大纲总结中的系统和软件列表')
        doc_instance.insert_header(2, "改进建议")
        #插入附录
        doc_instance.insert_header(1, "")

    return doc_instance.instance_id