# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: snapshot.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='snapshot.proto',
  package='bce.cds',
  syntax='proto2',
  serialized_pb=_b('\n\x0esnapshot.proto\x12\x07\x62\x63\x65.cds\"\x8c\x01\n\x0e\x42\x61\x63kupPbHeader\x12\x0c\n\x04type\x18\x01 \x02(\r\x12\x15\n\rcompress_type\x18\x02 \x02(\r\x12\x0e\n\x06\x62itmap\x18\x03 \x01(\x0c\x12\x14\n\x0cobject_names\x18\x04 \x03(\t\x12\x0e\n\x06offset\x18\x05 \x01(\r\x12\x11\n\tdata_size\x18\x06 \x01(\r\x12\x0c\n\x04lrsn\x18\x07 \x01(\x04\"\xbb\x01\n\x10SnapshotPbHeader\x12\x0f\n\x07snap_id\x18\x01 \x02(\t\x12\x13\n\x0bsnap_parent\x18\x02 \x02(\t\x12\x14\n\x0csnap_size_gb\x18\x03 \x02(\x04\x12\x16\n\x0e\x65xtent_size_mb\x18\x04 \x02(\x04\x12$\n\textent_pb\x18\x05 \x03(\x0b\x32\x11.bce.cds.ExtentPb\x12\x17\n\x0fstripe_width_kb\x18\x06 \x01(\x04\x12\x14\n\x0cstripe_count\x18\x07 \x01(\x04\"=\n\x08\x45xtentPb\x12\x15\n\rextent_offset\x18\x01 \x02(\x04\x12\x1a\n\x12\x65xtent_object_name\x18\x02 \x02(\t\"s\n\x0e\x45xtentPbHeader\x12\x0f\n\x07snap_id\x18\x01 \x02(\t\x12\x15\n\rextent_offset\x18\x02 \x02(\x04\x12\x15\n\rslice_size_mb\x18\x03 \x02(\x04\x12\"\n\x08slice_pb\x18\x04 \x03(\x0b\x32\x10.bce.cds.SlicePb\":\n\x07SlicePb\x12\x14\n\x0cslice_offset\x18\x01 \x02(\x04\x12\x19\n\x11slice_object_name\x18\x02 \x02(\tB\x03\x80\x01\x01')
)




_BACKUPPBHEADER = _descriptor.Descriptor(
  name='BackupPbHeader',
  full_name='bce.cds.BackupPbHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='bce.cds.BackupPbHeader.type', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='compress_type', full_name='bce.cds.BackupPbHeader.compress_type', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bitmap', full_name='bce.cds.BackupPbHeader.bitmap', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object_names', full_name='bce.cds.BackupPbHeader.object_names', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='offset', full_name='bce.cds.BackupPbHeader.offset', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data_size', full_name='bce.cds.BackupPbHeader.data_size', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lrsn', full_name='bce.cds.BackupPbHeader.lrsn', index=6,
      number=7, type=4, cpp_type=4, label=1,
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
  serialized_start=28,
  serialized_end=168,
)


_SNAPSHOTPBHEADER = _descriptor.Descriptor(
  name='SnapshotPbHeader',
  full_name='bce.cds.SnapshotPbHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='snap_id', full_name='bce.cds.SnapshotPbHeader.snap_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='snap_parent', full_name='bce.cds.SnapshotPbHeader.snap_parent', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='snap_size_gb', full_name='bce.cds.SnapshotPbHeader.snap_size_gb', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extent_size_mb', full_name='bce.cds.SnapshotPbHeader.extent_size_mb', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extent_pb', full_name='bce.cds.SnapshotPbHeader.extent_pb', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stripe_width_kb', full_name='bce.cds.SnapshotPbHeader.stripe_width_kb', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stripe_count', full_name='bce.cds.SnapshotPbHeader.stripe_count', index=6,
      number=7, type=4, cpp_type=4, label=1,
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
  serialized_start=171,
  serialized_end=358,
)


_EXTENTPB = _descriptor.Descriptor(
  name='ExtentPb',
  full_name='bce.cds.ExtentPb',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='extent_offset', full_name='bce.cds.ExtentPb.extent_offset', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extent_object_name', full_name='bce.cds.ExtentPb.extent_object_name', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=360,
  serialized_end=421,
)


_EXTENTPBHEADER = _descriptor.Descriptor(
  name='ExtentPbHeader',
  full_name='bce.cds.ExtentPbHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='snap_id', full_name='bce.cds.ExtentPbHeader.snap_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extent_offset', full_name='bce.cds.ExtentPbHeader.extent_offset', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slice_size_mb', full_name='bce.cds.ExtentPbHeader.slice_size_mb', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slice_pb', full_name='bce.cds.ExtentPbHeader.slice_pb', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=423,
  serialized_end=538,
)


_SLICEPB = _descriptor.Descriptor(
  name='SlicePb',
  full_name='bce.cds.SlicePb',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='slice_offset', full_name='bce.cds.SlicePb.slice_offset', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slice_object_name', full_name='bce.cds.SlicePb.slice_object_name', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=540,
  serialized_end=598,
)

_SNAPSHOTPBHEADER.fields_by_name['extent_pb'].message_type = _EXTENTPB
_EXTENTPBHEADER.fields_by_name['slice_pb'].message_type = _SLICEPB
DESCRIPTOR.message_types_by_name['BackupPbHeader'] = _BACKUPPBHEADER
DESCRIPTOR.message_types_by_name['SnapshotPbHeader'] = _SNAPSHOTPBHEADER
DESCRIPTOR.message_types_by_name['ExtentPb'] = _EXTENTPB
DESCRIPTOR.message_types_by_name['ExtentPbHeader'] = _EXTENTPBHEADER
DESCRIPTOR.message_types_by_name['SlicePb'] = _SLICEPB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BackupPbHeader = _reflection.GeneratedProtocolMessageType('BackupPbHeader', (_message.Message,), dict(
  DESCRIPTOR = _BACKUPPBHEADER,
  __module__ = 'snapshot_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.BackupPbHeader)
  ))
_sym_db.RegisterMessage(BackupPbHeader)

SnapshotPbHeader = _reflection.GeneratedProtocolMessageType('SnapshotPbHeader', (_message.Message,), dict(
  DESCRIPTOR = _SNAPSHOTPBHEADER,
  __module__ = 'snapshot_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.SnapshotPbHeader)
  ))
_sym_db.RegisterMessage(SnapshotPbHeader)

ExtentPb = _reflection.GeneratedProtocolMessageType('ExtentPb', (_message.Message,), dict(
  DESCRIPTOR = _EXTENTPB,
  __module__ = 'snapshot_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.ExtentPb)
  ))
_sym_db.RegisterMessage(ExtentPb)

ExtentPbHeader = _reflection.GeneratedProtocolMessageType('ExtentPbHeader', (_message.Message,), dict(
  DESCRIPTOR = _EXTENTPBHEADER,
  __module__ = 'snapshot_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.ExtentPbHeader)
  ))
_sym_db.RegisterMessage(ExtentPbHeader)

SlicePb = _reflection.GeneratedProtocolMessageType('SlicePb', (_message.Message,), dict(
  DESCRIPTOR = _SLICEPB,
  __module__ = 'snapshot_pb2'
  # @@protoc_insertion_point(class_scope:bce.cds.SlicePb)
  ))
_sym_db.RegisterMessage(SlicePb)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\200\001\001'))
# @@protoc_insertion_point(module_scope)
