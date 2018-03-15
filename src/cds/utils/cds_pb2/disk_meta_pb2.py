# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: disk_meta.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='disk_meta.proto',
  package='bce.cds',
  syntax='proto2',
  serialized_pb=_b('\n\x0f\x64isk_meta.proto\x12\x07\x62\x63\x65.cds\x1a\x0c\x63ommon.proto\"\x1f\n\nDiskPathPb\x12\x11\n\tfull_path\x18\x01 \x02(\t\"x\n\x0e\x44iskPropertyPb\x12\x0f\n\x07\x64isk_id\x18\x01 \x02(\x05\x12\x10\n\x08quota_gb\x18\x02 \x02(\x05\x12\x11\n\tdisk_type\x18\x03 \x02(\x05\x12\x16\n\x0eprivate_device\x18\x04 \x02(\x08\x12\x18\n\x10\x63reate_timestamp\x18\x05 \x02(\x03\"\x1c\n\x0bMaxDiskIdPb\x12\r\n\x05value\x18\x01 \x02(\x05')
  ,
  dependencies=[common__pb2.DESCRIPTOR,])




_DISKPATHPB = _descriptor.Descriptor(
  name='DiskPathPb',
  full_name='bce.cds.DiskPathPb',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='full_path', full_name='bce.cds.DiskPathPb.full_path', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=73,
)


_DISKPROPERTYPB = _descriptor.Descriptor(
  name='DiskPropertyPb',
  full_name='bce.cds.DiskPropertyPb',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='disk_id', full_name='bce.cds.DiskPropertyPb.disk_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='quota_gb', full_name='bce.cds.DiskPropertyPb.quota_gb', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_type', full_name='bce.cds.DiskPropertyPb.disk_type', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='private_device', full_name='bce.cds.DiskPropertyPb.private_device', index=3,
      number=4, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create_timestamp', full_name='bce.cds.DiskPropertyPb.create_timestamp', index=4,
      number=5, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=195,
)


_MAXDISKIDPB = _descriptor.Descriptor(
  name='MaxDiskIdPb',
  full_name='bce.cds.MaxDiskIdPb',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='bce.cds.MaxDiskIdPb.value', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=197,
  serialized_end=225,
)

DESCRIPTOR.message_types_by_name['DiskPathPb'] = _DISKPATHPB
DESCRIPTOR.message_types_by_name['DiskPropertyPb'] = _DISKPROPERTYPB
DESCRIPTOR.message_types_by_name['MaxDiskIdPb'] = _MAXDISKIDPB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DiskPathPb = _reflection.GeneratedProtocolMessageType('DiskPathPb', (_message.Message,), dict(
  DESCRIPTOR = _DISKPATHPB,
  __module__ = 'disk_meta_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.DiskPathPb)
  ))
_sym_db.RegisterMessage(DiskPathPb)

DiskPropertyPb = _reflection.GeneratedProtocolMessageType('DiskPropertyPb', (_message.Message,), dict(
  DESCRIPTOR = _DISKPROPERTYPB,
  __module__ = 'disk_meta_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.DiskPropertyPb)
  ))
_sym_db.RegisterMessage(DiskPropertyPb)

MaxDiskIdPb = _reflection.GeneratedProtocolMessageType('MaxDiskIdPb', (_message.Message,), dict(
  DESCRIPTOR = _MAXDISKIDPB,
  __module__ = 'disk_meta_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.MaxDiskIdPb)
  ))
_sym_db.RegisterMessage(MaxDiskIdPb)


# @@protoc_insertion_point(module_scope)
