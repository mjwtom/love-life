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


def insert_contract_accreditation_report (is_template=False):
        param_map = dict(
            projectId="13",
            testTurn="1"
        )
        doc_instance = DocInstance(param_map, 13, '软件测试合同评审报告',
                                   '软件测试合同评审报告模板', is_template)
        doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.ContractAccreditationReport',
                                         'getDocxXml',
                                         ['projectId', 'turnId', 'meetingId'],
                                         '软件测试合同评审报告',
                                         '软件测试合同评审报告统一生文档 ')
        print(doc_instance.instance_id)


def insert_demand_evaluation(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '项目需求评审报告',
                               '项目需求评审报告模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.DemandEvaluation',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '项目需求评审报告',
                                     '项目需求评审报告统一生文档 ')
    print(doc_instance.instance_id)


def insert_meeting_sign_confirmation(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '测试就绪会签确认表',
                               '测试就绪会签确认表模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.MeetingSignImpl',
                                     'getReadyContentXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '测试就绪会签确认表',
                                     '测试就绪会签确认表统一生文档 ')
    print(doc_instance.instance_id)


def insert_meeting_sign_plan(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '回归测试计划会签确认表',
                               '回归测试计划会签确认表', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.MeetingSignImpl',
                                     'getReadyContentXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '回归测试计划会签确认表',
                                     '回归测试计划会签确认表统一生文档 ')
    print(doc_instance.instance_id)


def insert_inner_revision_comments(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '软件测评大纲内部审查意见',
                               '软件测评大纲内部审查意见', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.OutlineInnerRevisionImpl',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '软件测评大纲内部审查意见',
                                     '软件测评大纲内部审查意见统一生文档 ')
    print(doc_instance.instance_id)


def insert_software_outline_comments(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '软件定型鉴定测评大纲审查意见',
                               '软件定型鉴定测评大纲审查意见模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.OutlineRevisionImpl',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '软件定型鉴定测评大纲审查意见',
                                     '软件定型鉴定测评大纲审查意见统一生文档 ')
    print(doc_instance.instance_id)


def insert_report_revision(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '软件定型鉴定测评大纲审查意见',
                               '软件定型鉴定测评大纲审查意见模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.ReportRivision',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '软件定型鉴定测评大纲审查意见',
                                     '软件定型鉴定测评大纲审查意见统一生文档 ')
    print(doc_instance.instance_id)


def insert_trilateral_comments(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '软件三方测评大纲审查意见',
                               '软件三方测评大纲审查意见模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.TrilateralOutlineRevisionImpl',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '软件三方测评大纲审查意见',
                                     '软件三方测评大纲审查意见模板统一生文档 ')
    print(doc_instance.instance_id)


def insert_configuration_modification_application(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '测试项目配置项变更申请表模板',
                               '测试项目配置项变更申请表模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.meeting.TrilateralOutlineRevisionImpl',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '测试项目配置项变更申请表模板',
                                     '测试项目配置项变更申请表模板统一生文档')
    print(doc_instance.instance_id)


def insert_equipment_environment_check(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '测试设备与测试环境检查单模板',
                               '测试设备与测试环境检查单模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.EquipmentEnvironmentCheck',
                                     'form',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '测试设备与测试环境检查单模板',
                                     '测试设备与测试环境检查单模板统一生文档')
    print(doc_instance.instance_id)


def insert_inout_warehouse(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '测试项目配置项入库出库表模板',
                               '测试项目配置项入库出库表模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.InOutWareHouse',
                                     'inOutWareHouse',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '测试项目配置项入库出库表模板',
                                     '测试项目配置项入库出库表模板统一生文档')
    print(doc_instance.instance_id)


def insert_problem_report(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '软件问题确认报告单模板',
                               '软件问题确认报告单模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.ProblemConfirmReport',
                                     'inOutWareHouse',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '软件问题确认报告单模板',
                                     '软件问题确认报告单模板统一生文档')
    print(doc_instance.instance_id)


def insert_proxy(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '项目测试委托书模板',
                               '项目测试委托书模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.ProxyDocument',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '项目测试委托书模板',
                                     '项目测试委托书模板统一生文档')
    print(doc_instance.instance_id)


def insert_quality_check(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '质量保证检查单模板',
                               '质量保证检查单模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.QualityGuaranteeCheck',
                                     'getFormXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '质量保证检查单模板',
                                     '质量保证检查单模板统一生文档')
    print(doc_instance.instance_id)


def insert_quality_problem_tracker(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '质量保证问题跟踪表模板',
                               '质量保证问题跟踪表模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.QualityProblemTracker',
                                     'form',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '质量保证问题跟踪表模板',
                                     '质量保证问题跟踪表模板统一生文档')
    print(doc_instance.instance_id)


def insert_software_inout(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '被测软件出入登记表模板',
                               '被测软件出入登记表模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.SoftwareInOut',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '被测软件出入登记表模板',
                                     '被测软件出入登记表模板统一生文档')
    print(doc_instance.instance_id)


def insert_test_log(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '测试日志模板',
                               '测试日志模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.TestLog',
                                     'form',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '测试日志模板',
                                     '测试日志模板统一生文档')
    print(doc_instance.instance_id)


def insert_work_arrangement(is_template=False):
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    doc_instance = DocInstance(param_map, 13, '测试项目工作安排模板',
                               '测试项目工作安排模板', is_template)
    doc_instance.insert_mt_structure('com.stms.tps.doc.form.WorkArrangement',
                                     'getDocxXml',
                                     ['projectId', 'turnId', 'meetingId'],
                                     '测试项目工作安排模板',
                                     '测试项目工作安排模板统一生文档')
    print(doc_instance.instance_id)

