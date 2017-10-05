import Queue
# Date:10-22-2015
# WLST script to collect server and thread level status
# Prints out threads and server status
# Connect with encrypted password or pass credentials via method arguments
# Author: Keynes Paul
# E-mail: keynes.paul@oracle.com
import sys

connect_strings={}
server_status={}
thread_status={}
data_for_all_domains=[]
queue = Queue.Queue()
#thresholds begin
health_state_threshold
server_status_threshold
thread_status_threshold
free_memory_threshold
free_memory_percentage_threshold

#threshold end
class server_report(object):

    def __init__(self):
        pass

    def connect_server_for_status(credentials,report_status):
            formatted_credentials = str(credentials).split(',')
            url=formatted_credentials[0]
            userconf=formatted_credentials[1]
            keyconf=formatted_credentials[2]
            connect(url=url,userConfigFile=userconf,userKeyFile=keyconf)
            domain_name = cmo.getName()
            servers_list = getMBean("Servers")
            servers = servers_list.getServers()
            domainRuntime()
            for server in servers:
                #begin heap status
                free_memory    = int(server.getJVMRuntime().getHeapFreeCurrent())/(1024*1024)
                free_memory_percentage = int(server.getJVMRuntime().getHeapFreePercent())
                current_memory = int(server.getJVMRuntime().getHeapSizeCurrent())/(1024*1024)
                max_heap_size     = int(server.getJVMRuntime().getHeapSizeMax())/(1024*1024)
                print('%20s %7d MB %5d MB %5d MB %3d%%' % (server.getName(),current,free,max,freePct))
                #end heap status
                #begin garbage collection status
                
                #end garbage collection status
                selected_server = server.getName()
                cd('ServerRuntimes/' + selected_server)
                connect_url = cmo.getURL("t3")
                connect_strings[selected_server]=connect_url
                server_state= str(cmo.getState())
                cd('ThreadPoolRuntime/ThreadPoolRuntime/')
                hogging_threads= cmo.getHoggingThreadCount()
                completed_request_count = cmo.getCompletedRequestCount()
                pending_user_request_count=cmo.getPendingUserRequestCount()
                throughput = cmo.getThroughput()
                health_state = str(cmo.getHealthState())
                health_state = health_state[health_state.find(':',health_state.find(':')+1)+1:health_state.find(',',health_state.find(',')+1)]
                execute_threads = cmo.getExecuteThreads()
                stuck_thread_count=0
                idle_thread_count=0
                hogger_thread_count=0
                standby_thread_count=0
                for thread in execute_threads:
                    if thread.isStuck() != 0:
                        stuck_thread_count += 1
                    elif thread.isIdle() != 0:
                        idle_thread_count += 1
                    elif thread.isHogger() != 0:
                        hogger_thread_count += 1
                    else:
                        standby_thread_count += 1
                if stuck_thread_count > 3:
                    threadDump()
                # print domain_name, ",", selected_server, ",", throughput, ",", pending_user_request_count, ",", health_state, ",", hogging_threads, ",", completed_request_count, ",", server_state, ",", idle_thread_count, ",", hogger_thread_count, ",", standby_thread_count, ",", stuck_thread_count
        

if __name__ == '__main':
    server_status = server_report.server_report()
    server_status.connect_server_for_status(str(sys.argv[1]),self.queue)