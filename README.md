# CiscoDeviceVersions v1.0
<h2>Cisco Network Device Version fetch.</h2>
 

This is a simple script designed to go and fetch the current IOS versions on Cisco devices.

The script is synchronous, and as such the amount of time it takes will be parallel with the amount of devices added. 
It may be possible to rework the script for async tasks to speed up the process time. Please be aware of memory and other resource considerations. 

Modify the script at your own risk. 

<h2>SETUP</h2>
<b>The script needs 8 libaries to work:</b>
<ul>
 <li><a href="http://www.paramiko.org/">paramiko</a></li>
  <li>os.path</li>
  <li>getpass</li>
  <li>time</li>
  <li>sys</li>
  <li>argparse</li>
 <li><a href="https://pypi.org/project/python-dotenv/">dotenv</a></li>
  <li>socket</li>
</ul>
    
<b>The script requires a .env file placed in the same directory.</b>

<b>The script needs 3 items modified in the .env file before use:</b>
<ol>
<li>Populate the 'IP_LIST' with all ip's that are cisco devices and ssh capable. Seperate IP's using a comma "," and no spaces.</li>
<li>Specify the SAVE_PATH to be where you would like to store the output. Use '/' slashes not '\' slashes</li>
<li>Specify the FILE_NAME to be the name of the output file.</li>
</ol>

<b>The script at run time will need credentials that are able to perform the 'show version' command on the devices specified in th IP array'</b>

<h2>Verified Devices</h2>
<b>This script has been verified to work with the below devices. However, this script in theory should work with most cisco IOS devices.</b>
<ul>
  <li>1921 Router</li>
  <li>4331 ISR routers</li>
  <li>2960X switches</li>
  <li>5516-x ASA</li>
</ul>

<b>To debug issues, you can run the script with the '--debug' flag, or alternatively you can modify the 'DEBUG' setting in the .env file.</b>

<b>I do not own any rights to cisco products or software. This script was made to help manage the devices only.</b>
