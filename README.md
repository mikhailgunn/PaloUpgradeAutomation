LDAPS communication occurs over port TCP 636. LDAPS communication to a global catalog server occurs over TCP 3269. When connecting to ports 636 or 3269, SSL/TLS is negotiated before any LDAP traffic is exchanged.

ldp.exe on domain controller can test connections
check if there are any cname record for  CNAME records for domain controllers 


Check certificates:
	check Multiple SSL certificates:
	check Local Machine's Personal store.
	NTDS Service's Personal certificate store
	ADDS Active directory  domain services  Personal certificate store

- client and ldaps domain controller must have Root Cert
- domain controller must have issued cert and private key
- root ca must have the key and cert
- issued CA must have the new LDAP DCs hostnames in the certificate
-  certificate must have:
	1. The enhanced key usage extension 
	2. Server Authentication object identifier (1.3.6.1.5.5.7.3.1).


further SSL tshoot enable logging:
https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/health-diagnostic-performance/enable-schannel-event-logging
