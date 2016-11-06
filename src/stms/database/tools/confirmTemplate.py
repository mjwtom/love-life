from db_util import MysqlClient
from statements import conf


client = MysqlClient(conf)
sql = 'UPDATE `docmetadata` SET `addedBy`=\'3\', `editedby`=\'1013\' WHERE `addedby`=\'1013\''
client.execute(sql)
sql = 'UPDATE `doctemplatestru` SET addedby=\'3\', `editedby`=\'1013\' WHERE addedby=\'1013\''
client.execute(sql)
sql = 'UPDATE `doctemplate` SET addedby=\'3\', `editedby`=\'1013\' WHERE addedby=\'1013\''
client.execute(sql)
print('success')
client.close()
