from __future__ import print_function
from st2reactor.sensor.base import Sensor

from concurrent import futures
import sys

from grpc.beta import implementations
from google.protobuf import json_format

import TelemetrySystemStats_pb2


class CpuUtilizationSensor(Sensor):

    def __init__(self, sensor_service, config=None):
        super(CpuUtilizationSensor, self).__init__(sensor_service=sensor_service, config=config)
        self._logger = self._sensor_service.get_logger(__name__)
        self._logger.info('init....\n')

        #parse config data

        self.ip = self.config['hostip']
        self.port = self.config['port']
        self.user_name = self._config['user_name']
        self.user_pass = self._config['pass']


    def setup(self):

        ## Initialize the grpc client connection and create a stub
        self.channel = implementations.insecure_channel(self.ip, int(self.port))
        self._logger.info('channel established %s-%d- \n', self.ip, int(self.port))
        self.stub = TelemetrySystemStats_pb2.beta_create_BrocadeTelemetrySystemData_service_stub(self.channel) 
        self._logger.info('stub  %s \n', str(self.stub))


    def run(self):
        self._logger.info('inside run\n')

        try:
            self._logger.info('inside run1\n')
            resp_stream = self.stub.BrocadeTelemetrySystemData(TelemetrySystemStats_pb2.BrocadeTelemetrySystemData_request(profile_name='PythonProfile'),timeout=120)
            for resp in resp_stream:
                j_resp = json_format.MessageToJson(resp)
                print(j_resp)
                j_dict = json.loads(j_resp)
                self._sensor_service.dispatch(trigger='cpu_usage.cpu_utilization', payload=j_dict)
                return
        except Exception as e:
                self._logger.exception('Polling VDX failed: %s' % (str(e)))
                raise
        self._logger.info('inside run4\n')

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
