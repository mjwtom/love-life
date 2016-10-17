from db_util import MysqlClient
from statements_template import clean_template, clean_template_structure, clean_metadata
from statements import clean_instance, clean_structure
from statements import conf
from documents.test_spec import insert_spec
from documents.test_record import insert_test_record
from documents.test_report import insert_test_report


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


def insert_doc(is_template=False):
    #doc_id = insert_test_report(is_template)
    doc_id = insert_test_record(is_template)
    #doc_id = insert_spec(is_template)
    if is_template:
        print('document template id is: %d' % doc_id)
    else:
        print('document instance id is: %d' % doc_id)


if __name__ == '__main__':
    clean()
    insert_doc(True)
