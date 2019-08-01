

metadata = "{u'ephemeral_raw': u'true', u'source': u'console', u'root_on_cds': u'True', u'key': u'bcc1', u'volume_id': u'422104756398715259', u'mount_oncds': u'True', u'payment': u'prepay'}"

print(metadata)
if "u'root_on_cds': u'True'" not in metadata:
    print('not found')
else:
    print('found')
volume_id_key = "u'volume_id': u'"
pos = metadata.find(volume_id_key)
if pos <= 0:
    print('not found')
after_str = metadata[pos + len(volume_id_key):]
pos = after_str.find("',")
evm_id = after_str[:pos]
print(evm_id)
print('done')