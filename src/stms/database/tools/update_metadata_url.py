from db_util import MysqlClient
from statements import conf
import json


client = MysqlClient(conf)
sql = 'select id, url from trhz.docmetadata'
data = client.select(sql)
for id, url in data:
    if not url:
        continue
    try:
        url_data = json.loads(url)
    except Exception as e:
        print(e)
    params = url_data.get('params')
    if params:
        print('url:%s' % params)
        if 'turnId' not in params:
            params.append('turnId')
            url = json.dumps(url_data)
            sql = 'update trhz.docmetadata set url=%s where id = %s'
            client.insert(sql, (url, id))
    else:
        print('empty url:%s' % params)
    print(url_data)
client.close()
