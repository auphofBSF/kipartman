'''
docstring
'''

from wx.lib.pubsub import pub

from helper.debugtools import debugprint

import platform, os, logging, datetime
import threading


from configuration import Configuration
from transitions import Machine, State

if platform.system() == 'Windows':
    from helper import kicadWin32GuiMonitor as kicadGUImonitor
else:
    pass #TODO: implement linux handler

def log(msg):
    if 'logging' in globals(): logging.debug(
        "{:%H:%M:%S.%f}:{}".format(
            datetime.datetime.now(),
            msg
        ))

class KicadEeschema(object):
    def __init__(self): 
        self.set_environment()
        self.set_schematic()
    
    def set_schematic(self, sheet='', file=''):
        self.sheet = sheet
        self.file = file
        log("Kicad:Eeschem: SCHEMATIC: Sheet:{}, File:{}".format(
            self.sheet, self.file
        ))

    def set_environment(self, hwnd=0, component_add_hwnd=0):
        self.hwnd = hwnd
        self.component_add_hwnd = component_add_hwnd

    def enter_EeschemaForeground(self): 
        log("Kicad:Eeschema: STATE: Entered Foreground ")
        pub.sendMessage('kicad.change.status', listen_to = 'Eeschema.Foreground')

    def enter_EeschemaBackground(self): 
        log("Kicad:Eeschema: STATE: Entered Background")
        pub.sendMessage('kicad.change.status', listen_to = 'Eeschema.Background')

    #Component Properties Dialog
    def enter_EeschemaComponentPropertiesForeground(self): 
        pub.sendMessage('kicad.change.status', listen_to = 'Eeschema.ComponentProperties.Entered')
        log("Kicad:componentProperties: STATE: Foreground: Entered")
    def exit_EeschemaComponentPropertiesForeground(self): 
        pub.sendMessage('kicad.change.status', listen_to = 'Eeschema.ComponentProperties.Exited')
        log("Kicad:componentProperties: STATE: Foreground: Exit")
    #Component Add Dialog
    def enter_EeschemaComponentAddForeground(self, hwnd=0, component_add_hwnd=0):
        self.component_add_hwnd = component_add_hwnd
        pub.sendMessage('kicad.change.status', listen_to = 'Eeschema.ComponentAdd.Entered')
        log("Kicad:componentAdd: STATE: Foreground: Entered hwnd:{}".format(component_add_hwnd))

    def exit_EeschemaComponentAddForeground(self, hwnd=0, component_add_hwnd=0): 
#        self.component_add_hwnd = component_add_hwnd
        pub.sendMessage('kicad.change.status', listen_to = 'Eeschema.ComponentAdd.Exited')

        log("Kicad:componentAdd: STATE: Foreground: Exit")


    def exit_EeschemaComponentProperties(self): log("Kicad:componentProperties: STATE: Exited")
    def say_goodbye(self): log("goodbye, old state!")

    pass

 
class ThreadKipartman(threading.Thread):
    stop = False
    debugstatus = 'Initializing-0'

    def __init__(self, *args, **kwargs):
         super(ThreadKipartman, self).__init__( *args, **kwargs)
         self.debugstatus = ThreadKipartman.debugstatus #'Initializing'
         self.stop = False


class KicadGUIEventProcessor(threading.Thread):
    stop = False

    def __init__(self, *args, **kwargs):
        super(KicadGUIEventProcessor, self).__init__(*args, **kwargs)
        pass

    def terminate(self):
        log('KicadGUIEventProcessor TERMINATE')
        KicadGUIEventProcessor.stop = True

    @staticmethod
    def EventProcessor(self, multiprocessQueue):
        #Statemachine Config
        # https://github.com/pytransitions/transitions#states

        kcE = KicadEeschema()
        states = [
            'EeschemaClosed',
            State(name='Eeschema_Foreground', on_enter=['enter_EeschemaForeground']),
            State(name='Eeschema_componentProperties_Foreground'
                , on_enter=['enter_EeschemaComponentPropertiesForeground']
                , on_exit=['exit_EeschemaComponentPropertiesForeground']),
            'Eeschema_ComponentAdd_launching1stHwnd',
            'Eeschema_ComponentAdd_launching2ndHwnd',
            State(name='Eeschema_componentAdd_Foreground'
                , on_enter=['enter_EeschemaComponentAddForeground']
                , on_exit=['exit_EeschemaComponentAddForeground']),
            State(name='Eeschema_Background', on_enter=['enter_EeschemaBackground'])
        ]
        transitions = [
            #Component Properties Edit
            {'trigger': 'ComponentPropEdit', 'source': '*',
            'dest': 'Eeschema_componentProperties_Foreground'},
            {'trigger': 'ComponentPropEdit_close',
            'source': 'Eeschema_componentProperties_Foreground',
            'dest': 'Eeschema_Foreground'},
            #Component Add 
            {'trigger': 'ComponentAdd_launching1stHwnd',
            'source': '*',
            'dest': 'Eeschema_ComponentAdd_launching1stHwnd'},

            {'trigger': 'ComponentAdd_launching2ndHwnd',
            'source': 'Eeschema_ComponentAdd_launching1stHwnd',
            'dest': 'Eeschema_ComponentAdd_launching2ndHwnd'},
            
            {'trigger': 'ComponentAdd_Focus',
            'source': ['Eeschema_ComponentAdd_launching2ndHwnd'
                    , 'Eeschema_Background'
                    , 'Eeschema_Foreground'],
            'dest': 'Eeschema_componentAdd_Foreground'},

            {'trigger': 'ComponentAdd_close',
            'source': 'Eeschema_componentAdd_Foreground',
            'dest': 'Eeschema_Foreground'},

            {'trigger': 'Foreground',
            'source': '*',
            'dest': 'Eeschema_Foreground'},
            {'trigger': 'Background', 'source': 'Eeschema_Foreground',
            'dest': 'Eeschema_Background'},
            {'trigger': 'Background', 'source': ['Eeschema_componentProperties_Foreground'
                                                ,'Eeschema_componentAdd_Foreground'],
            'dest': 'Eeschema_Background'},
        ]
        kcE_stateMachine = Machine(kcE)
        #kcE_stateMachine.  #TODO configure Machine logging (disable)
        logging.getLogger('transitions').setLevel(logging.ERROR)
        kcE_stateMachine.add_states(states)
        kcE_stateMachine.add_transitions(transitions)

        #TODO: Determine state (is kicad open, is component properties open
        kcE_stateMachine.set_state('EeschemaClosed')
        # TODO: are there many instances open (Handle multiple instances)
        '''
        EventHandler queue Dict keys
                'dwmsEventTime':"%s:%04.2f".format(dwmsEventTime
                , float(dwmsEventTime - EventHandler.lastTime)/1000)
                , 'eventTypeText': eventTypes.get(event, hex(event))
                , 'eventTypeHex':  hex(event)
                , 'hwnd': hwnd
                , 'processID': processID or -1
                , 'dwEventThread' :dwEventThread or -1
                , 'shortName':shortName
                , 'titleValue':title.value})
        '''
        log('EventProcessor: about to start receiving events, THREAD INSTANCE:{}: '.format(self))

        while not KicadGUIEventProcessor.stop:
            try:
                #multiprocessQueue.get is blocking, so put a 2s timeout
                obj = multiprocessQueue.get(True,2)
                if not KicadGUIEventProcessor.stop:
                    try:
                        if isinstance(obj, dict):
                            if (obj['eventTypeText'] in ['Foreground']
                                    and obj['shortName'] == u'bin\\kicad.exe'
                                    and obj['titleValue'] == u'Component Properties'):
                                log(u' \t\t--------------------- Kicad Component Properties:{} hwnd:{}'.format(obj['eventTypeText']
                                                            , obj['hwnd'])
                                                            )
                                kcE.ComponentPropEdit()

                            elif (obj['eventTypeText'] in ['Foreground']
                                    and obj['shortName'] == u'bin\\kicad.exe'
                                    and obj['titleValue'] != u'Component Properties'):
                                kcE.Foreground()

                            #Component Add sequence of window launches
                            #slightly more complicated, the signiture is the 'Choose Component (
                            # but we have to find the hwnd for the 3rd show  to detect task switching back to eeschema with the dialog open

                            elif (obj['eventTypeText'] in ['Show']
                                    and obj['shortName'] == u'bin\\kicad.exe'
                                    and u'Choose Component (' in obj['titleValue']
                                    and kcE.is_Eeschema_Foreground()):
                                kcE.ComponentAdd_launching1stHwnd(obj['hwnd'])
                            # now look for 2nd window - Handle 1st one
                            elif (kcE.is_Eeschema_ComponentAdd_launching1stHwnd()):
                                if (obj['eventTypeText'] in ['Show']
                                    and obj['shortName'] == u'bin\\kicad.exe'
                                    and obj['titleValue'] == u''):
                                    kcE.ComponentAdd_launching2ndHwnd(obj['hwnd'])
                            # Looking for 2ns Window - THis should be it
                            elif (kcE.is_Eeschema_ComponentAdd_launching2ndHwnd()):
                                if (obj['eventTypeText'] in ['Show']
                                    and obj['shortName'] == u'bin\\kicad.exe'
                                    and obj['titleValue'] == u''):
                                    kcE.ComponentAdd_Focus(component_add_hwnd=obj['hwnd'])
                            # Component Add Switch back from Background
                            elif (obj['eventTypeText'] in ['Show']
                                    and obj['shortName'] == u'bin\\kicad.exe'
                                    and kcE.component_add_hwnd == obj['hwnd']
                                    #and u'Choose Component (' in obj['titleValue'])
                                    and kcE.is_Eeschema_Foreground()):
                                kcE.ComponentAdd_Focus(component_add_hwnd=obj['hwnd'])

                            # Record the filename and Scheetname in kcE
                            elif (obj['eventTypeText'] in ['Focus','Capture']
                                and obj['shortName'] == u'bin\\kicad.exe'
                                and (False or 'Eeschema' in obj['titleValue'])):

                                #print('DUMP:{}'.format(obj['titleValue'].split(u'\u2014')))
                                # print('DUMP:{}'.format([elem.encode("hex") for elem in obj['titleValeue']]))
                                titleParse = obj['titleValue'].split(u'\u2014')
                                kcE.set_schematic( sheet=titleParse[1].strip(),
                                                    file= titleParse[2].strip())

                            elif (obj['eventTypeText'] in ['Foreground']
                                    and obj['shortName'] != u'bin\\kicad.exe'
                                    and not (kcE.is_EeschemaClosed()
                                                or kcE.is_Eeschema_Background())):
                                kcE.Background()
                            #TODO: Sense Eeschema being closed
                            # What to watch for or test.
                            # May have to test if window is open
                            else:
                                if obj['shortName']==u'bin\\kicad.exe':
                                    log(u'\t\t\t---------------------********'
                                        '----{}\t{}\t{}\t{}\t{}\t{}\tkcE:{}'.format(
                                        obj['dwmsEventTime']
                                        , obj['eventTypeText']
                                        , obj['eventTypeHex']
                                        , obj['shortName']
                                        , obj['titleValue']
                                        , obj['hwnd']
                                        ,kcE.component_add_hwnd))
                                else:
                                    pass
                        elif isinstance(obj, unicode):
                            #print(obj)
                            pass
                        pass
                    except Exception as e:
                        log('\tKicadGUIEventProcessor.EventProcessor ERROR: {}, STATE:{}, OBJ:{}'.format(e,kcE.state, obj))
                        pass
                    finally:
                        pass
                else:
                    log('Thread Stop is active')
            except:
                pass


def EventWatcher(q):
        configuration=Configuration()
        configuration.Load()
        log('Launched EventWatcher PID:{}'.format(os.getpid()))
        log('Launching kGm.EventHandler.main')

        kicadGUImonitor.EventHandler.main(q) 