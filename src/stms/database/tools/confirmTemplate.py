from db_util import MysqlClient
from statements import conf


client = MysqlClient(conf)
sql = 'UPDATE `trhz`.`docmetadata` SET `addedBy`=\'3\', `editedby`=\'1013\' WHERE `addedby`=\'1013\''
client.execute(sql)
sql = 'UPDATE `trhz`.`doctemplatestru` SET addedby=\'3\', `editedby`=\'1013\' WHERE addedby=\'1013\''
client.execute(sql)
sql = 'UPDATE `trhz`.`doctemplate` SET addedby=\'3\', `editedby`=\'1013\' WHERE addedby=\'1013\''
client.execute(sql)
print('success')
client.close()
