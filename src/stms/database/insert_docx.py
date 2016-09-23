from db_util import MysqlClient
from statements import instance_insert, metadata_insert, structure_insert, \
    clean_instance, clean_structure, clean_metadata, instance_insert

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
    init_map = dict(
        className='com.stms.tps.doc.TestOutlineImpl',
        methodName='initMetadata'
    )
    param_map = dict(
        projectId="13",
        testTurn="1"
    )
    order_num = 0
    # instance_id = instance_insert(param_map, '13', init_map)
    # 插入文档实例
    instance_id = instance_insert(param_map, 13)
    # 插入目录
    metadata_map = dict(
        className='com.stms.tps.doc.TestReportImpl',
        methodName='getSimpleToC'
    )
    metadata_id = metadata_insert(metadata_map)
    structure_insert(instance_id, -1, order_num, '3', 1,
                     '目录', '生成目录', metadata_id);
    order_num += 1

    # 插入分页符
    metadata_map = dict(
        className='com.stms.tps.doc.TestReportImpl',
        methodName='getBreakPage'
    )
    break_page_metadata_id = metadata_insert(metadata_map)
    structure_insert(instance_id, -1, order_num, '3', 1,
                     '分页', '分页', break_page_metadata_id);
    order_num += 1

    # 插入范围
    pid1 = structure_insert(instance_id, -1, order_num, '1', 1,
                     '范围', '范围d');
    order_num += 1

    # 插入文档标识
    pid = structure_insert(instance_id, pid1, order_num, '1', 2,
                     '标识', '文档标识');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '1) 文档标识号：XXXX-RJCP-CPDG-XXXX 。');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '2) 标题： YYYYYYYY软件定型/鉴定测评大纲 。');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '3) 被测件：YYYYYYYY软件 ，各软件配置项信息及标识见表1-1。');
    order_num += 1

    metadata_map = dict(
        className='com.stms.tps.doc.TestReportImpl',
        methodName='getVersionInformation',
        params=['projectId']
    )
    # 插入测试项数据用于处理复杂的节点
    metadata_id = metadata_insert(metadata_map)
    structure_insert(instance_id, pid,order_num, '3', 1,
                     '版本信息表', '测试项', metadata_id)
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '4)术语和缩略语');
    order_num += 1

    metadata_map = dict(
        className='com.stms.tps.doc.TestReportImpl',
        methodName='getTerms',
        params=['projectId']
    )
    # 插入测试项数据用于处理复杂的节点
    metadata_id = metadata_insert(metadata_map)
    structure_insert(instance_id, pid, order_num, '3', 1,
                     '术语和缩略语', '测试项', metadata_id)
    order_num += 1

    pid = structure_insert(instance_id, pid1, order_num, '2', 2,
                     '文档概述', '文档标识');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '本文档内容包括：1.范围；2.引用文档；3.测评概述；4.测试结果；5.评价结论与改进建议；6.其他。');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '文档标识本文档适用于XXXXXXXX系统YYYYYYYY软件定型/鉴定 测评，是XXXXXXXX系统YYYYYYYY软件定型/鉴定 的依据 。');
    order_num += 1

    pid = structure_insert(instance_id, pid1, order_num, '1', 2,
                     '委托方的名称与联系方式 ', '文档标识');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '； ', '委托方的名称：海定委办公室');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '委托方地址：XXXXXXXXXX； ');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     ' ', '委托方联系人：XXX；');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '委托方联系人电话：010-XXXXXX。 ');
    order_num += 1

    pid = structure_insert(instance_id, pid1,order_num, '1', 2,
                     '承研单位的名称与联系方式 ', '文档标识');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     ' ', '承研单位的名称：海定委办公室；');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '承研单位地址：XXXXXXXXXX； ');
    order_num += 1

    structure_insert(instance_id, pid ,order_num, '2', 2,
                     ' ', '承研单位联系人：XXX；');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     ' ', '承研单位联系人电话：010-XXXXXX。');
    order_num += 1

    pid = structure_insert(instance_id, pid1, order_num, '1', 2,
                     '定型/鉴定 测评机构的名称与联系方式 ', '文档标识');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '定型/鉴定 测评机构的名称：海定委办公室； ');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     ' ', '定型/鉴定 测评机构地址：XXXXXXXXXX；');
    order_num += 1

    structure_insert(instance_id, pid,order_num, '2', 2,
                     ' ', '定型/鉴定 测评机构联系人：XXX；');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '2', 2,
                     '', '定型/鉴定 测评机构联系人电话：010-XXXXXX。 ');
    order_num += 1

    pid = structure_insert(instance_id, pid1,order_num, '1', 2,
                     '被测软件概述', '文档标识');
    order_num += 1

    pid = structure_insert(instance_id, pid, order_num, '1', 3,
                     '系统概述', '文档标识');
    order_num += 1

    structure_insert(instance_id, pid, order_num, '1', 3,
                     '系统的使命任务和组成 ', '文档标识');
    order_num += 1

    metadata_map = dict(
        className='com.stms.tps.doc.TestReportImpl',
        methodName='getTpsProductSpec',
        params=['projectId']
    )
    # 插入测试项数据用于处理复杂的节点
    metadata_id = metadata_insert(metadata_map)
    structure_insert(instance_id, pid, order_num, '3', 1,
                     '测试项', '测试项', metadata_id)
    order_num += 1

    pid1 = structure_insert(instance_id, -1, order_num, '1', 1,
                     '引用文件', '文档标识');
    order_num += 1


    print("doc instance id %s" % instance_id)


if __name__ == '__main__':
    clean()
    insert_test_report()
