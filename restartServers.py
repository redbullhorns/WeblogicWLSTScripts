import Queue
# Date:10-22-2015
# WLST script to collect server and thread level status
# Prints out threads and server status
# Connect with encrypted password or pass credentials via method arguments
# Author: Keynes Paul
# E-mail: keynes.paul@oracle.com
import sys,os
server_credentials='t3://148.87.148.133:49901,/smnh9o/local/smnh9o-WebLogicConfig.properties,/smnh9o/local/smnh9o-WebLogicKey.properties'
domain_directory='/smnh9o/local/config/domains/soa_domain'
nm_host = 'vmohsmnhm094.oracleoutsourcing.com'
nm_port = '49946'

def server_restart():
    selected_servers=[]
    formatted_credentials = str(server_credentials).split(',')
    # url=formatted_credentials[0]
    url=''
    userconf=formatted_credentials[1]
    keyconf=formatted_credentials[2]
    redirect('/dev/null', 'false')
    # nmConnect(userConfigFile=userconf,userKeyFile=keyconf, host=nm_host,port=nm_port, nmType='ssl', domainName='soa_domain')
    nmConnect(userConfigFile='/smnh9o/local/smnh9o-WebLogicConfig.properties',userKeyFile='/smnh9o/local/smnh9o-WebLogicKey.properties',host='vmohsmnhm094.oracleoutsourcing.com',port='49946', mType='ssl', domainName='soa_domain',verbose='true')
    readDomain(domain_directory)
    admin_server=cmo.getAdminServerName()
    if not str(nmServerStatus(admin_server)).__contains__('RUNNING'):
        nmStart(admin_server)
        while not str(nmServerStatus(admin_server)).__contains__('RUNNING'):
            print 'Restarting %s ...' % admin_server
            os.system('sleep 5s')
            if str(nmServerStatus(admin_server)).__contains__('ADMIN'):
                resume(admin_server)
        print '%s is %s'%(admin_server, str(nmServerStatus(admin_server)))
    cd('Server/' + admin_server)
    listen_address = cmo.getListenAddress()
    listen_port = cmo.getListenPort()
    url = 't3://'+str(listen_address)+':'+str(listen_port)
    connect(url=url,userConfigFile=userconf,userKeyFile=keyconf)
    servers_list = getMBean("Servers")
    servers = servers_list.getServers()
    user_provided_servers = sys.argv[1:]
    for server in servers:
        selected_servers.append(server.getName())
    for server in user_provided_servers:
        if server not in selected_servers:
            print 'Input servers %s not valid!! Available list of server:' %server
            for server in selected_servers:
                print server
            return
    for server in user_provided_servers:
        domainRuntime()
        cd("/ServerRuntimes/" + server)
        current_machine = cmo.getCurrentMachine()
        domain_home = cmo.getCurrentDirectory()[:-1]
        cd("../../ServerLifeCycleRuntimes/" + server)
        server_state = str(cmo.getState())
        if not (str(server_state).__contains__('SHUTDOWN')):
            shutdown(server, 'Server', force='true')
        print 'Waiting for server %s to shutdown ...' % server
        os.system('sleep 10s')
        while not(str(cmo.getState()).__contains__('SHUTDOWN')):
            print 'Waiting for server %s to shutdown ...' %server
        print 'Clearing tmp and cache folders ...'
        current_time=os.system('date +%F-%r')
        delete_command = str('ssh '+ current_machine+'.oracleoutsourcing.com '+'cd '+ domain_home+'/servers/'+server+'/; mv cache cache-%s;mv tmp tmp-%s')%(current_time,current_time)
        print delete_command
        os.system(delete_command)
        print 'Restarting server %s .' % server
        serverRuntime()
        start(server, 'Server', block='false')
        domainRuntime()
        print 'Waiting for server %s to restart ...' % server
        os.system('sleep 10s')
        while not (str(cmo.getState()).__contains__('RUNNING') or str(cmo.getState()).__contains__('FAILED_NOT_RESTARTABLE')):
            print 'Waiting for server %s to restart ...' %server
            if str(cmo.getState()).__contains__('FAILED_NOT_RESTARTABLE'):
                print '%s needs manual attention, is FAILED_NOT_RESTARTABLE !!' % server
                break
            elif str(cmo.getState()).__contains__('ADMIN'):
                print '%s needs manual attention, resumed to running !!' % server
                resume(server)
            os.system('sleep 10s')
        print 'Server %s is RUNNING.' %server

server_restart()