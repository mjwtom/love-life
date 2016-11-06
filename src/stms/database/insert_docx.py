from db_util import MysqlClient
from statements_template import clean_template, clean_template_structure, clean_metadata
from statements import clean_instance, clean_structure
from statements import conf
from documents.test_spec import insert_spec
from documents.test_record import insert_test_record
from documents.test_report import insert_test_report
from documents.regression_record import insert_regression_record
from documents.regression_plan import insert_regression_plan
from documents.regression_spec import insert_regression_spec


def clean():
    client = MysqlClient(conf)
    sql = clean_template()
    client.execute(sql)
    sql = clean_template_structure()
    client.execute(sql)
    sql = clean_metadata()
    client.execute(sql)
    sql = clean_instance()
    client.execute(sql)
    sql = clean_structure()
    client.execute(sql)
    client.close()

if __name__ == '__main__':
    # clean()
    # 插入回归测试记录
    # insert_regression_record(True, '4c5dd1d2dba1428fb4af7c30e5077664')
    # 插入回归测试计划
    # insert_regression_plan(True, '55102128b8c44d2b8dd10cdc9a030cb9')
    # 插入回归测试说明
    # insert_regression_spec(True, '104e3635e8c84f288dd6763a8a6a80c9')
    insert_test_report(True, 'e491fbeba1ad47d392615d733b12feaa')
