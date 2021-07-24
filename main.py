


#The Purpose of this code it to create a quick fix to allow HamLib to control 2 the RT-21 Az/El
#which uses 2 USB devices to control the Az and El rotator
#This assumes that HamLib communicates using TCP socket as stated in the communication section of:
#http://manpages.ubuntu.com/manpages/trusty/man8/rotctld.8.html
#it may be worth while to try and capture the messages on the socket to see what type of things are
#being sent back and forth and alter as needed
#Also I opened an Issue on github which seems like there is intention to resolve by Sept
#https://github.com/Hamlib/Hamlib/issues/747


#Usage:
#Set The Host Address of the machine
#Set the ROTCTLRS_PORT to be the port that you tell ROTCTLRS about
#Set the Az_PORT to the Azmithul Rotator Port
#Set the El_PORT to the Elevation Rotator Port

#Warning this code is trash

import SocketDuplicator
import argparse
import socket
# BC I'm lazy make these globals to this program
global LAST_REQUESTED_POSREQUESTED, HOST, Az_PORT, El_PORT, ROTCTLD_PORT


#TODO Should this open the port or should HamLib open the port
def Recieve_Command():

        #Create a Socket at client side
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, ROTCTLD_PORT))
        while True:
            print("Waiting for incoming command")
            s.listen(1)
            conn, addr = s.accept()
            data = conn.recv(1024)
            print(data)
            Parse_Command(data.decode())
            conn.close()
#            print('Received:' + command.decode())
 #           command = s.recv(1024)
  #      Parse_Command(command)

        return


#This will need to be able to parse out The commands that could be sent to the RotCtld
#TODO I dont know how SatNog or HamLib communicates with rotctld I would assume they send the 'short' command\
#ToDO But they could send the longer commands through the socket (eg: "\\dump_caps \n" rather than "1 \n"
def Parse_Command(command):
    print(f"Here {command[0]}")
    if command[0] == 'P': Parse_Set_Pos(command)
    if command[0] == 'p': Fake_Current_Pos()
    if command[0] == 'M': Parse_Move(command)
    if command[0] == 'S': Split_Command(command)
    if command[0] == 'K': Split_Command(command)
    if command[0] == 'R': Split_Command(command)
    if command[0] == '_': Fake_Get_info(command)
    if command[0] == '1': Fake_Dump_Caps(command)

    #     K, \park            Set the rotor to the park position
    #     R, \reset           Reset the rotor
    #     _, \get_info        Get the rotor Model Name
    #     1, \dump_caps       Get the rot capabilities and display select values

    return

#send a command out to the specified port 
def Send_Command(Rotor_Port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, Rotor_Port))
    sock.send(command)
    return

#Incase we need to send stuff back
def Talk_Back():
    return


#Brief: Split the Set pos Command into 2 separate commands
#Command should Come in like "P 100 090 \n"
#Will need to be split:
#"P 100 000 \n"
#"P 090 000 \n"
def Parse_Set_Pos(command):
    print("Parsing Set Pos")
    command_components = command.split( )
    Send_Command(Az_PORT, f"{command_components[0]} {command_components[1]} 000 \n".encode())
    Send_Command(El_PORT, f"{command_components[0]} {command_components[2]} 000 \n".encode())
    print("Commands Sent")
    return

#Hopefuly They dont request this data back bc I dont want to code it
def Fake_Current_Pos():
    return

#if commands like "park" are sent we want them to be split and sent out
def Split_Command(command):
    Send_Command(Az_PORT, command.encode())
    Send_Command(El_PORT, command.encode())
    print("Commands Sent")
    return



#### THIS is Where the Magic Begins!!!!
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #Add valid arguments to take in
    parser.add_argument('--host', help='host ip')
    parser.add_argument('--rotctld_port', help='Port to tell Hamlib that you are using')

    parser.add_argument('--az_port', help='Port for azimuth Rotator')

    parser.add_argument('--el_port', help="Port For elevation Rotator")

    args = parser.parse_args()


    #Assign The args
    HOST = args.host
    ROTCTLD_PORT = int(args.rotctld_port)
    Az_PORT=int(args.az_port)
    El_PORT=int(args.el_port)

    #This variable should contain a list in the for mat of:
    #float [Az, Ez] to fool the requester
    LAST_REQUESTED_POSREQUESTED = [0.0,0.0]

    #Jump into it
    Recieve_Command()




#Known Commands
# # Get the rot capabilities from Hamlib and store in the %rot_caps hash.
# Commands are the same as described in the rotctld(1) man page.  This is only
# a brief summary.
#     P, \set_pos         Set the rotor's Azimuth and Elevation
#     p, \get_pos         Get the rotor's Azimuth and Elevation
#     M. \move            Move Up, Down, Left, Right at Speed
#     S, \stop            Stop rotation
#     K, \park            Set the rotor to the park position
#     R, \reset           Reset the rotor
#     _, \get_info        Get the rotor Model Name
#     1, \dump_caps       Get the rot capabilities and display select values


# HOST = '127.0.0.1'
# ROTCTLRS_PORT = 5789
# Az_PORT=4533
# El_PORT=4532
#
# #This variable should contain a list in the for mat of:
# #float [Az, Ez] to fool the requester
# LAST_REQUESTED_POSREQUESTED = [0.0,0.0]
#
# Recieve_Command()




####ALL THIS IS TRASH!! PROBABLY NOT USEFUL BUT WHO KNOWS
# import argparse
# import os
# import shlex
# import socket
#
#
#
#
# def run_rotctld(m=None, r=None, s=None, T=None, t=None, L=None, C=None, l=None, u=None, e=None, v=None):
#     bashCommand = f"rotctld"
#     print(r)
#     if m is not None: bashCommand=f"{bashCommand} -m {m}"
#     if r is not None: bashCommand=f"{bashCommand} -r {r}"
#     if s is not None: bashCommand=f"{bashCommand} -s {s}"
#     if T is not None: bashCommand=f"{bashCommand} -T {T}"
#     if t is not None: bashCommand=f"{bashCommand} -t {t}"
#     if L is not None: bashCommand=f"{bashCommand} -L {L}"
#     if C is not None: bashCommand=f"{bashCommand} -C {C}"
#     if l is not None: bashCommand=f"{bashCommand} -t {l}"
#     if u is not None: bashCommand=f"{bashCommand} -L {u}"
#     if e is not None: bashCommand=f"{bashCommand} -C {e}"
#     import subprocess
#
#     print(bashCommand)
#
#     os.environ["PATH"] = '/usr/bin' + os.pathsep + os.environ["PATH"]
#     command_line_args = shlex.split(bashCommand)
#     my_env = os.environ.copy()
#
#     process = subprocess.Popen(
#         command_line_args,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         env=my_env
#     )
#     print(process.communicate())
#     process.wait()
#      # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#
#     # Add valid arguments to take in
#     parser.add_argument('--model', '-m',
#                         help='Select rotator model number. See -l, "list" option below.')
#     parser.add_argument('--rot_file','-r', metavar='--rot-file',
#                         help=' Use device as the file name of the port the rotator is connected.  Often  a  serial port,  but  could  be  a  USB  to  serial  adapter  or  USB port device.  Typically /dev/ttyS0, /dev/ttyS1, /dev/ttyUSB0, etc. on Linux or COM1, COM2, etc. on Win32.')
#
#     parser.add_argument('--serial_speed','-s',metavar='--serial-speed',
#                         help='Set serial speed to baud  rate.  Uses  maximum  serial  speed  from  rotor  backend capabilities (set by -m above) as the default')
#
#     parser.add_argument('--listen_addr','-T', metavar='--listen-addr')
#     parser.add_argument('-t', '--port')
#     parser.add_argument('--show_conf','-L', metavar='--show-conf' )
#
#     args = parser.parse_args()
#     run_rotctld(m=args.model, r=args.rot_file, s=args.serial_speed, T=args.listen_addr, t=args.port, L=args.listen_addr,
#                 C=None, l=None, u=None, e=None, v=None)
#
#     parser
#     #     -C, --set-conf=parm=val[,parm=val]*
#   #             Set config parameter.  e.g. --set-conf=stop_bits=2
#   #
#   #             Use -L option for a list.
#   #
#   #      -l, --list
#   #             List all model numbers defined in Hamlib and exit.  As  of  1.2.15.1  the  list  is
#   #             sorted by model number.
#   #
#   #             N.B.  In Linux the list can be scrolled back using Shift-PageUp/ Shift-PageDown, or
#   #             using the scrollbars of a virtual terminal in X or the cmd window in Windows.   The
#   #             output can be piped to 'more' or 'less', e.g. 'rotctld -l | more'.
#   #
#   #      -u, --dump-caps
#   #             Dump capabilities for the radio defined with -m above and exit.
#   #
#   #      -e, --end-marker
#   #             Use END marker in rotctld protocol.
#   #
#   #             N.B.:  This  option  should  be  considered  obsolete.   Please  consider using the
#   #             Extended Response protocol instead (see  PROTOCOL  below).   This  option  will  be
#   #             removed in a future Hamlib release.
#   #
#   #      -v, --verbose
#   #             Set verbose mode, cumulative (see DIAGNOSTICS below).
#   #
#   #      -h, --help
#   #             Show a summary of these options and exit.
#   #
#   #      -V, --version
#   #             Show the version of rotctld and exit

