"""
Jiaqi Huang (Imperial College London)
02-03-2011
"""
import ctypes
import numpy as np

# load DLL
nidaq = ctypes.windll.nicaiu # load the DLL
##############################
# Setup some typedefs and constants
# to correspond with values in
# C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
# the typedefs

uint8 = ctypes.c_uint8
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float64 = ctypes.c_double
TaskHandle = uInt32
# the constants
DAQmx_Val_ChanForAllLines = 1
DAQmx_Val_GroupByChannel = 0

class Ports( object ):
    """
    This class performs the necessary initialization of the DAQ hardware and
    initializes the digital lines to low (digital 0)
    """
    def __init__( self ):
        #self.port0 = [0,0,0,0]
        self.port1 = [0,0,0,0]
        #self.port0data = np.zeros((4,), np.uint8 )
        self.port1data = np.zeros((4,), np.uint8 )

        #self.taskHandle0 = TaskHandle( 0 )
        self.taskHandle1 = TaskHandle( 1 )
        
        # setup the DAQ hardware for port0 and port1
        #self.CHK(nidaq.DAQmxCreateTask("",
        #                  ctypes.byref( self.taskHandle0 )))
        self.CHK(nidaq.DAQmxCreateTask("",
                          ctypes.byref( self.taskHandle1 )))
        
        #self.CHK(nidaq.DAQmxCreateDOChan( self.taskHandle0,
        #                           "Dev4/port0/line0:3",
        #                           "",
        #                           DAQmx_Val_ChanForAllLines))
        self.CHK(nidaq.DAQmxCreateDOChan( self.taskHandle1,
                                   "Dev4/port1/line0:3",
                                   "",
                                   DAQmx_Val_ChanForAllLines))
        
        #self.run(self.taskHandle0)
        self.run(self.taskHandle1)
        
        # Initialize digital ports
        self.update( port1 = self.port1) #, port1 = self.port1)
        
    def CHK( self, err ):
        """a simple error checking routine"""
        if err < 0:
            buf_size = 100
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))
        if err > 0:
            buf_size = 100
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
            raise RuntimeError('nidaq generated warning %d: %s'%(err,repr(buf.value)))
        
    def run( self, taskHandle ):
        self.CHK(nidaq.DAQmxStartTask( taskHandle ))
        
    def stop( self ):
        nidaq.DAQmxStopTask( self.taskHandle1 )
        nidaq.DAQmxClearTask( self.taskHandle1 )
        
    def update(self, port1 = [0,0,0,0]):#, port1 = [0,0,0,0]
        #if len(port0) != 4:
        #    raise ValueError('port0 argument must have 4 values')
        if len(port1) != 4:
            raise ValueError('port1 argument must have 4 values')

        #for i in range(len(port0)):
        #    self.port0data[i] = port0[i]
        for i in range(len(port1)):
            self.port1data[i] = port1[i]
        #self.CHK(nidaq.DAQmxWriteDigitalLines( self.taskHandle0,
        #                      1, 1, float64(10.0),
        #                      DAQmx_Val_GroupByChannel,
        #                      self.port0data.ctypes.data,
        #                      None,
        #                      None))
        self.CHK(nidaq.DAQmxWriteDigitalLines( self.taskHandle1,
                              1, 1, float64(10.0),
                              DAQmx_Val_GroupByChannel,
                              self.port1data.ctypes.data,
                              None,
                              None))



if __name__ == '__main__':
    import time
    import numpy



    D_out = Ports() 
    
    D_out.update(port1=[1,0,0,0])
    time.sleep( 0.1 )
    D_out.update(port1=[0,0,0,0])
    
    time.sleep( 2 )
    
    D_out.update(port1=[1,0,0,0])
    time.sleep( 0.1 )
    D_out.update(port1=[0,0,0,0])




    D_out.stop()
