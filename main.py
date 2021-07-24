# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import argparse
import os
import shlex

def run_rotctld(m=None, r=None, s=None, T=None, t=None, L=None, C=None, l=None, u=None, e=None, v=None):
    bashCommand = f"rotctld"
    print(r)
    if m is not None: bashCommand=f"{bashCommand} -m {m}"
    if r is not None: bashCommand=f"{bashCommand} -r {r}"
    if s is not None: bashCommand=f"{bashCommand} -s {s}"
    if T is not None: bashCommand=f"{bashCommand} -T {T}"
    if t is not None: bashCommand=f"{bashCommand} -t {t}"
    if L is not None: bashCommand=f"{bashCommand} -L {L}"
    if C is not None: bashCommand=f"{bashCommand} -C {C}"
    if l is not None: bashCommand=f"{bashCommand} -t {l}"
    if u is not None: bashCommand=f"{bashCommand} -L {u}"
    if e is not None: bashCommand=f"{bashCommand} -C {e}"
    import subprocess

    print(bashCommand)

    os.environ["PATH"] = '/usr/bin' + os.pathsep + os.environ["PATH"]
    command_line_args = shlex.split(bashCommand)
    my_env = os.environ.copy()

    process = subprocess.Popen(
        command_line_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=my_env
    )
    print(process.communicate())
    process.wait()
     # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Add valid arguments to take in
    parser.add_argument('--model', '-m',
                        help='Select rotator model number. See -l, "list" option below.')
    parser.add_argument('--rot_file','-r', metavar='--rot-file',
                        help=' Use device as the file name of the port the rotator is connected.  Often  a  serial port,  but  could  be  a  USB  to  serial  adapter  or  USB port device.  Typically /dev/ttyS0, /dev/ttyS1, /dev/ttyUSB0, etc. on Linux or COM1, COM2, etc. on Win32.')

    parser.add_argument('--serial_speed','-s',metavar='--serial-speed',
                        help='Set serial speed to baud  rate.  Uses  maximum  serial  speed  from  rotor  backend capabilities (set by -m above) as the default')

    parser.add_argument('--listen_addr','-T', metavar='--listen-addr')
    parser.add_argument('-t', '--port')
    parser.add_argument('--show_conf','-L', metavar='--show-conf' )

    args = parser.parse_args()
    run_rotctld(m=args.model, r=args.rot_file, s=args.serial_speed, T=args.listen_addr, t=args.port, L=args.listen_addr,
                C=None, l=None, u=None, e=None, v=None)

    parser
    #     -C, --set-conf=parm=val[,parm=val]*
  #             Set config parameter.  e.g. --set-conf=stop_bits=2
  #
  #             Use -L option for a list.
  #
  #      -l, --list
  #             List all model numbers defined in Hamlib and exit.  As  of  1.2.15.1  the  list  is
  #             sorted by model number.
  #
  #             N.B.  In Linux the list can be scrolled back using Shift-PageUp/ Shift-PageDown, or
  #             using the scrollbars of a virtual terminal in X or the cmd window in Windows.   The
  #             output can be piped to 'more' or 'less', e.g. 'rotctld -l | more'.
  #
  #      -u, --dump-caps
  #             Dump capabilities for the radio defined with -m above and exit.
  #
  #      -e, --end-marker
  #             Use END marker in rotctld protocol.
  #
  #             N.B.:  This  option  should  be  considered  obsolete.   Please  consider using the
  #             Extended Response protocol instead (see  PROTOCOL  below).   This  option  will  be
  #             removed in a future Hamlib release.
  #
  #      -v, --verbose
  #             Set verbose mode, cumulative (see DIAGNOSTICS below).
  #
  #      -h, --help
  #             Show a summary of these options and exit.
  #
  #      -V, --version
  #             Show the version of rotctld and exit

