from __future__ import print_function

#from concurrent import futures

import logging
import sys

from grpc.beta import implementations
from google.protobuf import text_format


import TelemetrySystemStats_pb2


logger = logging.getLogger('SysStats')
class SysStatsClient:
  def init_logger(self):
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)-15s[%(threadName)-15s::%(module)-20s:%(funcName)-20s] %(message)s' )
                        
    self.l = logging.LoggerAdapter(logger, {})
    
  def __init__(self, ip, port):
    self.init_logger()
    self.l.debug('Securing channel %s:%d' % (ip, port))
    #channel = implementations.insecure_channel('localhost', 50051)
    channel = implementations.insecure_channel(ip, port)
    self.l.debug(str(channel))
    self.l.debug('Creating stub')
    self.stub = TelemetrySystemStats_pb2.beta_create_BrocadeTelemetrySystemData_service_stub(channel)

  def getSysStats(self):
    self.l.debug('Calling getSysStats')
    try:
      moRespStream = self.stub.BrocadeTelemetrySystemData(TelemetrySystemStats_pb2.BrocadeTelemetrySystemData_request(profile_name='PythonProfile'),timeout=None)
      for moResp in moRespStream:
        s_resp = text_format.MessageToString(moResp, as_one_line=True) 
        self.l.debug('Received Response: %s' % s_resp)
    except KeyboardInterrupt:
      self.l.exception("KeyboardInterrupt error:") 
      raise
    except:
      self.l.exception("Unexpected error:") #, sys.exc_info()[0]
      raise

def printUsage():
  print ("Usage: %s ipv4 port" % sys.argv[0])
  sys.exit(-1)
    
def checkArgs(arg_count):
  if len(sys.argv) < arg_count:
    printUsage()
    
if __name__ == '__main__':
  checkArgs(3)


  client = SysStatsClient(sys.argv[1], int(sys.argv[2]))
  client.getSysStats()

