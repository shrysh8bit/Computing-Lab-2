1.	The positve indexing for read, write and delete is 0-indexed. Exactly as per assignment 1.

2.	For multi-line inputs, strictly use the quoatation marks. To submit the command press enter to reach next line and press enter again on an empty line to submit.

3.	For inviting a client, use V/E when setting permissions. Only E (not e) has been mapped and all other entries default to VIEWER permission. This has been done since user is inviting another user, in case of incorrect input, it defaults to least privilege. The permissions on the server end are stored in int. The server will display them in integer and not alph. Corresponding values are :-
	a. 1 - Owner
	b. 2 - Editor
	c. 3 - Viewer

4.	The invite request has to be replied in yes/no. No other values are permitted.

5.	Issue faced - When a client is entering a command and an invite message is recieved, it creates unexpected behaviour since the execution stage in client is not at select and client is not reading any incoming message on the socket but at STDIN instead.
