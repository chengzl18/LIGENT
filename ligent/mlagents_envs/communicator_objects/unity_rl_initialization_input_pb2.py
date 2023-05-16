# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mlagents_envs/communicator_objects/unity_rl_initialization_input.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ligent.mlagents_envs.communicator_objects import capabilities_pb2 as mlagents__envs_dot_communicator__objects_dot_capabilities__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mlagents_envs/communicator_objects/unity_rl_initialization_input.proto',
  package='communicator_objects',
  syntax='proto3',
  serialized_pb=_b('\nFmlagents_envs/communicator_objects/unity_rl_initialization_input.proto\x12\x14\x63ommunicator_objects\x1a\x35mlagents_envs/communicator_objects/capabilities.proto\"\xc0\x01\n\x1fUnityRLInitializationInputProto\x12\x0c\n\x04seed\x18\x01 \x01(\x05\x12\x1d\n\x15\x63ommunication_version\x18\x02 \x01(\t\x12\x17\n\x0fpackage_version\x18\x03 \x01(\t\x12\x44\n\x0c\x63\x61pabilities\x18\x04 \x01(\x0b\x32..communicator_objects.UnityRLCapabilitiesProto\x12\x11\n\tnum_areas\x18\x05 \x01(\x05\x42%\xaa\x02\"Unity.MLAgents.CommunicatorObjectsb\x06proto3')
  ,
  dependencies=[mlagents__envs_dot_communicator__objects_dot_capabilities__pb2.DESCRIPTOR,])




_UNITYRLINITIALIZATIONINPUTPROTO = _descriptor.Descriptor(
  name='UnityRLInitializationInputProto',
  full_name='communicator_objects.UnityRLInitializationInputProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='seed', full_name='communicator_objects.UnityRLInitializationInputProto.seed', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='communication_version', full_name='communicator_objects.UnityRLInitializationInputProto.communication_version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='package_version', full_name='communicator_objects.UnityRLInitializationInputProto.package_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='capabilities', full_name='communicator_objects.UnityRLInitializationInputProto.capabilities', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_areas', full_name='communicator_objects.UnityRLInitializationInputProto.num_areas', index=4,
      number=5, type=5, cpp_type=1, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=152,
  serialized_end=344,
)

_UNITYRLINITIALIZATIONINPUTPROTO.fields_by_name['capabilities'].message_type = mlagents__envs_dot_communicator__objects_dot_capabilities__pb2._UNITYRLCAPABILITIESPROTO
DESCRIPTOR.message_types_by_name['UnityRLInitializationInputProto'] = _UNITYRLINITIALIZATIONINPUTPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UnityRLInitializationInputProto = _reflection.GeneratedProtocolMessageType('UnityRLInitializationInputProto', (_message.Message,), dict(
  DESCRIPTOR = _UNITYRLINITIALIZATIONINPUTPROTO,
  __module__ = 'ligent.mlagents_envs.communicator_objects.unity_rl_initialization_input_pb2'
  # @@protoc_insertion_point(class_scope:communicator_objects.UnityRLInitializationInputProto)
  ))
_sym_db.RegisterMessage(UnityRLInitializationInputProto)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002\"Unity.MLAgents.CommunicatorObjects'))
# @@protoc_insertion_point(module_scope)
