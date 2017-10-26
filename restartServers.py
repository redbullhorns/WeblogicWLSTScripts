import Queue
# Date:10-22-2015
# WLST script to collect server and thread level status
# Prints out threads and server status
# Connect with encrypted password or pass credentials via method arguments
# Author: Keynes Paul
# E-mail: keynes.paul@oracle.com
import sys, os

server_credentials = 't3://148.87.148.133:49901,/smnh9o/local/smnh9o-WebLogicConfig.properties,/smnh9o/local/smnh9o-WebLogicKey.properties'
FMT = '%H:%M:%S'
domain_home='/smnh9o/local/config/domains/soa_domain'
host = 'vmohsmnhm094.oracleoutsourcing.com'

def server_restart():
    selected_servers = []
    formatted_credentials = str(server_credentials).split(',')
    url = formatted_credentials[0]
    userconf = formatted_credentials[1]
    keyconf = formatted_credentials[2]
    redirect('/dev/null', 'false')
    connect(url=url, userConfigFile=userconf, userKeyFile=keyconf)
    servers_list = getMBean("Servers")
    servers = servers_list.getServers()
    user_provided_servers = sys.argv[1:]
    for server in servers:
        selected_servers.append(server.getName())
    for server in user_provided_servers:
        if server not in selected_servers:
            print 'Input servers %s not valid!! Available list of server:' % server
            for server in selected_servers:
                print server
            return
    domainRuntime()
    servers_list = domainRuntimeService.getServerRuntimes()
    for server in user_provided_servers:
        domainRuntime()
        current_machine=''
        for each_server in servers_list:
            if server in each_server.getName():
                current_machine = each_server.getCurrentMachine()
        cd("/ServerLifeCycleRuntimes/" + server)
        server_state = str(cmo.getState())
        if not (str(server_state).__contains__('SHUTDOWN')):
            shutdown(server, 'Server', force='true')
            print 'Waiting for server %s to shutdown ...' % server
            print 'Clearing tmp and cache folders ...'
            delete_command = str('ssh '+ current_machine+'.oracleoutsourcing.com '+'"cd '+ domain_home+'/servers/'+server+'; rm -rf cache-0;mv cache cache-0;rm -rf tmp-0;mv tmp tmp-0"')
            os.system(delete_command)
        os.system('sleep 10s')
        while not (str(cmo.getState()).__contains__('SHUTDOWN')):
            print 'Waiting for server %s to shutdown ...' % server
        print 'Restarting server %s .' % server
        serverRuntime()
        start(server, 'Server', block='false')
        domainRuntime()
        print 'Waiting for server %s to restart ...' % server
        os.system('sleep 10s')
        while not (str(cmo.getState()).__contains__('RUNNING')):
            print 'Waiting for server %s to restart ...' % server
            os.system('sleep 10s')
        print 'Server %s is RUNNING.' % server
server_restart()