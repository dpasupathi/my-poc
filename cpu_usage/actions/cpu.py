from st2actions.runners.pythonrunner import Action

import logging
import sys
import json

from grpc.beta import implementations
from google.protobuf import json_format

import TelemetrySystemStats_pb2


class CpuUtilization(Action):

    def __init__(self, config=None):
       super(CpuUtilization, self).__init__(config=config)
       self.ip = self.config['hostip']
       self.port = self.config['port']

       self.logger.info('Initializing....\n')
       self.channel = implementations.insecure_channel(self.ip, self.port)
       self.logger.info('channel established %s-%d- \n', self.ip, self.port)
       self.stub = TelemetrySystemStats_pb2.beta_create_BrocadeTelemetrySystemData_service_stub(self.channel)
       self.logger.info('stub created\n')

    def run(self, host_ip, port, total_memory=0, free_memory=0, user_name='root', password='fibranne'):
       self.logger.info('Entering run method...\n')
       used  = self.get_cpu_info()
       print('Used Memory: %d\n' % used)
       return True

    def get_cpu_info(self):

       try:
          resp_stream = self.stub.BrocadeTelemetrySystemData(TelemetrySystemStats_pb2.BrocadeTelemetrySystemData_request(profile_name='PythonProfile'),timeout=120)
          for resp in resp_stream:
              j_resp = json_format.MessageToJson(resp)
              print(j_resp)
              j_dict = json.loads(j_resp)
              freem = int(j_dict['totalFreeMemory'])
              totalm = int(j_dict['totalSystemMemory'])
              used = totalm - freem
              return used 
       except Exception as e:
              self.logger.info('Exception: %s\n', str(e));
              return -1 

       return 0 

