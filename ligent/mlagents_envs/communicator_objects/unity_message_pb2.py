# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mlagents_envs/communicator_objects/unity_message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ligent.mlagents_envs.communicator_objects import unity_output_pb2 as mlagents__envs_dot_communicator__objects_dot_unity__output__pb2
from ligent.mlagents_envs.communicator_objects import unity_input_pb2 as mlagents__envs_dot_communicator__objects_dot_unity__input__pb2
from ligent.mlagents_envs.communicator_objects import header_pb2 as mlagents__envs_dot_communicator__objects_dot_header__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mlagents_envs/communicator_objects/unity_message.proto',
  package='communicator_objects',
  syntax='proto3',
  serialized_pb=_b('\n6mlagents_envs/communicator_objects/unity_message.proto\x12\x14\x63ommunicator_objects\x1a\x35mlagents_envs/communicator_objects/unity_output.proto\x1a\x34mlagents_envs/communicator_objects/unity_input.proto\x1a/mlagents_envs/communicator_objects/header.proto\"\xc0\x01\n\x11UnityMessageProto\x12\x31\n\x06header\x18\x01 \x01(\x0b\x32!.communicator_objects.HeaderProto\x12<\n\x0cunity_output\x18\x02 \x01(\x0b\x32&.communicator_objects.UnityOutputProto\x12:\n\x0bunity_input\x18\x03 \x01(\x0b\x32%.communicator_objects.UnityInputProtoB%\xaa\x02\"Unity.MLAgents.CommunicatorObjectsb\x06proto3')
  ,
  dependencies=[mlagents__envs_dot_communicator__objects_dot_unity__output__pb2.DESCRIPTOR,mlagents__envs_dot_communicator__objects_dot_unity__input__pb2.DESCRIPTOR,mlagents__envs_dot_communicator__objects_dot_header__pb2.DESCRIPTOR,])




_UNITYMESSAGEPROTO = _descriptor.Descriptor(
  name='UnityMessageProto',
  full_name='communicator_objects.UnityMessageProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='communicator_objects.UnityMessageProto.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unity_output', full_name='communicator_objects.UnityMessageProto.unity_output', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unity_input', full_name='communicator_objects.UnityMessageProto.unity_input', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=239,
  serialized_end=431,
)

_UNITYMESSAGEPROTO.fields_by_name['header'].message_type = mlagents__envs_dot_communicator__objects_dot_header__pb2._HEADERPROTO
_UNITYMESSAGEPROTO.fields_by_name['unity_output'].message_type = mlagents__envs_dot_communicator__objects_dot_unity__output__pb2._UNITYOUTPUTPROTO
_UNITYMESSAGEPROTO.fields_by_name['unity_input'].message_type = mlagents__envs_dot_communicator__objects_dot_unity__input__pb2._UNITYINPUTPROTO
DESCRIPTOR.message_types_by_name['UnityMessageProto'] = _UNITYMESSAGEPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UnityMessageProto = _reflection.GeneratedProtocolMessageType('UnityMessageProto', (_message.Message,), dict(
  DESCRIPTOR = _UNITYMESSAGEPROTO,
  __module__ = 'ligent.mlagents_envs.communicator_objects.unity_message_pb2'
  # @@protoc_insertion_point(class_scope:communicator_objects.UnityMessageProto)
  ))
_sym_db.RegisterMessage(UnityMessageProto)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002\"Unity.MLAgents.CommunicatorObjects'))
# @@protoc_insertion_point(module_scope)