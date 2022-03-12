// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <pthread.h>
#include <fcntl.h>

#define PORT 57908


/*
xxxxxxxxxxxxxxxxxxxxxxxxReverse String (Sub Function to Send & Receive File)xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void reverse(char *x, int begin, int end){
   char c;

   if (begin >= end){
      return;
   }

   c = *(x+begin);
   *(x+begin) = *(x+end);
   *(x+end) = c;

   reverse(x, ++begin, --end);
}


/*
xxxxxxxxxxxxxxxxxxxxxxxxSend File From Client To Serverxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void send_file(char file_name[100], int socket_fd){   
	char dupl[10] = {0};
	read (socket_fd, dupl, sizeof(dupl));
	printf("File duplicacy check reply from server : %s\n", dupl);
	
	if ( !strcmp(dupl, "duplicate") ){
		printf("File with same name already exists at server\n");
		printf("Please upload another file\n");
		return;
	}

	printf("\nSending file %s to server\n", file_name);

	FILE *fp;
	fp = fopen(file_name, "r");

    int lines_in_file = 0;
    char file_contents[1024];

    while(fgets(file_contents, sizeof(file_contents), fp) != NULL) {
		lines_in_file = lines_in_file + 1;
	}

	printf("Lines(int) outgoing in file_content : %d\n", lines_in_file);

	int i  = 0;
	bzero(file_contents, 1024);

	while (lines_in_file){
		printf("Line :%d %d\n",i, lines_in_file);

		file_contents[i] = lines_in_file%10 + 48 ;
		lines_in_file = lines_in_file/10;
		// printf("int to char : %d ", file_contents[i]);
		i++;
	}
	printf("Lines(char) outgoing in file_content : %s\n", file_contents);

	// reverse(file_contents, 0, sizeof(file_contents) - 1);
	printf("Lines(char) outgoing in file_content : %s\n", file_contents);

	write(socket_fd, file_contents, sizeof(file_contents));
	bzero(file_contents, 1024);

	rewind(fp);
    while(fgets(file_contents, sizeof(file_contents), fp) != NULL) {
		fflush(stdin);
		fflush(stdout);

        if (write(socket_fd, file_contents, sizeof(file_contents)) == -1) {

			perror("Error in sending file.");
			return;
        }
        bzero(file_contents, 1024);

    }
	fclose(fp);
	printf("Client says : File sent to server\n");
	return;
}


/*
xxxxxxxxxxxxxxxxxxxxxxxxReceive File From Serverxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void receive_file(char file_name[100], int socket_fd){   
	
    char file_contents[1024] = {0};
	
	char cmd_parameter[] = "recv.txt";

	FILE *fp;
	fp = fopen(cmd_parameter, "w");

    int lines;

	//verify this line below
	read(socket_fd, file_contents, sizeof(file_contents));

	lines = atoi(file_contents);

	bzero(file_contents, 1024);
	fflush(stdin);
	fflush(stdout);


    for (int i = 0; i < lines; i++) {

		fflush(stdin);
		fflush(stdout);
		read(socket_fd, file_contents, sizeof(file_contents));
		fprintf(fp, "%s", file_contents);
        bzero(file_contents, 1024);
       
    }

	fclose(fp);
	printf("File received to client fm server\n");
	rename(cmd_parameter, file_name);
	return;
}


int receive_id(int socket){
	int id;
	char data[10] = {0};
	bzero(data, sizeof(data));
	read(socket, data, sizeof(data));
	id = atoi(data);

	return id;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxReceive User List From Serverxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void receive_user_list(int socket){
	
	printf("Clients connected to server are :\n");
	int id;
	char receive[10];

	for (int i = 0; i < 5; i++){
		
        bzero(receive, sizeof(receive));
		read(socket, receive, sizeof(receive));

		// id = receive_id(socket);
		if (strlen(receive) != 0){
			printf("%s\n", receive);
		}
	}
	printf("Received\n");

	return ;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxReceive File List From Serverxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void receive_file_list(int socket){
	
	// printf("Permissions :\n\tO -> Owner\n\tE -> Editor\n\tV -> View\n\n");
	printf("Files held with the server are :\n\n");
	printf("Client id\tFile Name\tPermission\tLines in file\n");

	// int id;
	char receive[1024];

	for (int i = 0; i < 100; i++){
		
        bzero(receive, sizeof(receive));
		read(socket, receive, sizeof(receive));

		// id = receive_id(socket);
		if (receive[0] != '0'){
			char p1[100], p2[100], p3[100], p4[100];
			int id, perm_int, lines;
			// printf("Receive : %s\n", receive);

			sscanf(receive, "%s %s %s %s", p1, p2, p3, p4);
			// input_field_count = sscanf(input_cmd,"%s %[^\n]",extracted_cmd, cmd_parameter );

			// printf("sscanf");
			if(!strcmp(p3, "1")){
				strcpy(p3, "Owner");
			}else if(!strcmp(p3, "2")){
				strcpy(p3, "Editor");
			}else{
				strcpy(p3, "Viewer");
			}
			// printf("permissions");

			sprintf(receive, "%s\t\t%s\t\t%s\t\t%s\n", p1, p2, p3, p4);
			// printf("sprintf");

			printf("%s\n", receive);
		}
	}
	printf("File list received\n");

	return ;
}


int file_and_permission_check_reply(int socket){
	
	//Permission and existence check reply
	char reply[5];
	read (socket, reply, sizeof(reply));
	printf("perm check reply : %s\n", reply);
	if(!strcmp(reply, "huh!")){
		printf("  -  File does not exist at server\n");
		return 0;
	}

	if (!strncmp(reply, "yes", 3)){
		printf("  -  Client permitted to perform requested operation on file\n");
	}else{
		printf("  -  Client NOT permitted to perform requested operation on file\n");
		return 0;
	}

	return 1;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Read File Content From Server xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void read_file_content_from_server(int socket){
	int lines;
	char file_content[1024] = {0};


	//index check
	read (socket, file_content, sizeof(file_content));
	printf("Index check : %s\n", file_content);
	
	if (!strcmp(file_content, "Line number out of index")){
		return;
	}

	read (socket, file_content, sizeof(file_content));
	lines = atoi(file_content);

	printf("Reading %d line(s) from server\n", lines);

	for (int i = 0; i < lines; i++){
		bzero(file_content, sizeof(file_content));
		read(socket, file_content, sizeof(file_content));
		printf("Line %d. %s", i + 1, file_content);
	}

	return;
}




/*
xxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

xxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/

int main()
{
	int sock = 0, rc;
	pthread_t thread_id;
	struct sockaddr_in serv_addr;

	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		printf("\n Socket creation error \n");
		exit(-1);
	}

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	memset (&(serv_addr.sin_zero) , 0 ,8);


	/*
	xxxxxxxxxxxxxxxxxxxxxxxx Make New Connection xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/
	if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
	{
		printf("\nConnection Failed \n");
		return -1;
	}



	// Connection to server est,
	// client will send and receive on socket
	char message[100] = "No msg received from server\n";
	read (sock, message, sizeof(message));

	if ( !strcmp(message, "Max clients connected, try again later\n") ){
		printf("\nMessage from server : %s\n", message);
		return 0;
	}else{
		printf("\nMessage from server :\n %s\n", message);
	}

	int max_fd;
	fd_set readfds;
	char buffer[1024];

	printf("\nCommands available to user:\n");
	printf("1. View all active clients	: /users\n");
	printf("2. View all files and details	: /files\n");
	printf("3. Upload a file		: /upload <filename>\n");
	printf("4. Download a file		: /download <filename>\n");
	printf("5. Invite a collborator		: /invite <filename> <client_id> <permission>\n");
	printf("6. Read from a file		: /read <filename> <start_idx> <end_idx>\n");
	printf("7. Insert into a file		: /insert <filename> <idx> “<message>”\n");
	printf("8. Delete from a file		: /delete <filename> <start_idx> <end_idx>”\n");
	printf("9. Exit the client program	: /exit\n\n");

	while(1){

		char input_cmd[1024], temp[1024];
		bzero(input_cmd, sizeof(input_cmd));

		
		printf("\nCmd at client from user : \n");

		fflush(stdin);
		fflush(stdout);

		max_fd = sock;
        FD_ZERO(&readfds);
        char reply[100];
        FD_SET(sock, &readfds);
        FD_SET(STDIN_FILENO, &readfds);
        fcntl(STDIN_FILENO, F_SETFL, O_NONBLOCK);
        bzero(buffer, sizeof(buffer));
        select(max_fd + 1, &readfds, NULL, NULL, NULL);

        if (FD_ISSET(sock, &readfds))
        {
			printf("\nIncoming message from server\n");
            if (read(sock, buffer, sizeof(buffer)) > 0)
            {
                // master_cmd(sock, buffer);

            }
        }
        else if(FD_ISSET(STDIN_FILENO, &readfds))
        {
			// printf("msg outgoing\n");

			bzero(buffer, sizeof(buffer));
            read(0, buffer, sizeof(buffer));

            // if (read(0, buffer, sizeof(buffer)) > 0){
			// fgets (buffer, sizeof(buffer), stdin);
                // master_cmd(sock, buffer);
                // fseek(stdin, 0, SEEK_END);
                // bzero(buffer, sizeof(buffer));
                // write(listen_fd,buffer,sizeof(buffer));
            
        }



// printf("in master cmd fn\n");
	// printf("incoming cmd: --|%s|--\n", v1);

	char input[1024], extracted_cmd[24], param_1[100], param_2[100], param_3[100];
	int input_field_count, start_index, stop_index;
	
	fflush(stdin);
	bzero(input, sizeof(input));
	strcpy(input, buffer);

	char cmd_parameter[1000];
	input_field_count = sscanf(input,"%s %[^\n]",extracted_cmd, cmd_parameter );
	// printf("incoming cmd: %s\n", input);
	// printf("incoming : %s\n", extracted_cmd);

	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Users Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/users")){
		printf("In /users function\n");

		//Send extracted_cmd to server
		write(sock, input, sizeof(input));
		receive_user_list(sock);
		
		continue;;
	}

	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Files Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/files")){
		printf("In /files function\n");

		//Send extracted_cmd to server
		write(sock, input, sizeof(input));
		receive_file_list(sock);
		
		continue;;
	}


	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Upload Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/upload")){
		printf("\nIn /upload function\n");	
		input_field_count = sscanf(cmd_parameter,"%s %s",param_1, param_2 );

		printf("File name : %s\n", param_1);
		// printf("File name : %s\n", param_2);

		//Cmd check
		if ( input_field_count != 1){
			printf("Invalid input by user\n");
			continue;
		}

		FILE *fp;
		// fp = param_1;

		printf("starting file exists check\n");
		if (fopen(param_1, "r") == NULL){
			printf("File does not exist\n");
			continue;
		}
		// fclose(fp);

		
		printf("Send cmd to server\n");
		//Send cmd to server
		fflush(stdin);
		write(sock, input, sizeof(input));
		fflush(stdin);


		printf("Send file to server\n");
		//Send file to server
		send_file(param_1, sock);

		bzero(input, sizeof(input));
		read (sock, input, sizeof(input));
		printf("Server says : %s\n", input);
		
		continue;;
	}

	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Download Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/download")){
		printf("In /download function\n");
		
		input_field_count = sscanf(cmd_parameter,"%s %s",param_1, param_2 );

		//Cmd check
		if ( input_field_count != 1){
			printf("Invalid input by user\n");
			continue;;
		}
		//Send extracted_cmd to server
		write(sock, input, sizeof(input));

		int check;
		if ( !file_and_permission_check_reply(sock) ){
			continue;;
		}

		receive_file(param_1, sock);
		
		continue;;
	}

	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Invite Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/invite")){
		printf("In /invite function\n");
		
		input_field_count = sscanf(cmd_parameter,"%s %s %s",param_1, param_2, param_3 );

		//Cmd check
		if ( input_field_count != 3){
			printf("Invalid input by user\n");
			continue;;
		}

		if(!strncmp(param_3, "E", 1)){
			strcpy(param_3, "2");
		}else{
			strcpy(param_3, "3");
		}

		sprintf(input, "/invite %s %s %s", param_1, param_2, param_3);
		//Send extracted_cmd to server
		write(sock, input, sizeof(input));

		int check;
		if ( !file_and_permission_check_reply(sock) ){
			continue;
		}

		read(sock, input, sizeof(input));
		printf("Server says : %s\n", input);
		
		continue;
	}


	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Read Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/read")){
		printf("\nIn /read functionn\n");

		input_field_count = sscanf(cmd_parameter,"%s %s %s",param_1, param_2, param_3 );

		//Cmd check
		if ( input_field_count < 1){
			printf("Invalid input by user\n");
			continue;;
		}

		//Send extracted_cmd to server
		fflush(stdin);
		write(sock, input, sizeof(input));
		fflush(stdin);


		if ( !file_and_permission_check_reply(sock) ){
			continue;
		}
		
		read_file_content_from_server(sock);


		continue;

	}

	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Insert Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/insert")){

		input_field_count = sscanf(cmd_parameter,"%s %s %s",param_1, param_2, param_3 );

		//Cmd check
		if ( input_field_count < 2){
			printf("Invalid input by user\n");
			continue;
		}

		int bits;
		fflush(stdin);

		while (select(max_fd + 1, &readfds, NULL, NULL, NULL)){
			fflush(stdin);
			bzero(buffer, sizeof(buffer));
			bits = read(0, buffer, sizeof(buffer));
			strcat (input, buffer);
			if ( bits == 1){
				break;
			}
		}

		printf("\nIn /insert function\n");
		printf("command : %s\n", input);

		int count = 0;
		for (int i = 0; i < sizeof(input); i++){
			if (input[i] == '"'){
				count++;
			}
		}

		if ( count < 2){
			printf("Invalid input format by user\n");
			continue;;
		}
		
		//Send cmd to server
		fflush(stdin);
		write(sock, input, sizeof(input));
		fflush(stdin);

		printf("Starting file & permission check\n");
		if ( !file_and_permission_check_reply(sock) ){
			continue;;
		}


		printf("Starting line number check\n");
		read(sock, input, sizeof(input));

		if (!strcmp(input, "Line number out of index")){
			printf("%s\n", input);
			continue;;
		}
		
		read(sock, input, sizeof(input));

		if (!strcmp(input, "Line(s) inserted to file")){
			printf("The updated file is :\n");
			read_file_content_from_server(sock);
		}

		continue;

	}


	/*
	xxxxxxxxxxxxxxxxxxxxxxxx /Delete Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "/delete")){
		printf("In /delete function\n");
		
		input_field_count = sscanf(cmd_parameter,"%s %s",param_1, param_2 );

		//Cmd check
		if ( input_field_count < 1){
			printf("Invalid input by user\n");
			continue;;
		}

		//Send extracted_cmd to server
		write(sock, input, sizeof(input));

		printf("Starting file & permission check\n");
		if ( !file_and_permission_check_reply(sock) ){
			continue;;
		}

		printf("Starting line number check\n");
		read(sock, input, sizeof(input));

		if (!strncmp(input, "Line number out of index", 24)){
			printf("Index check : %s\n", input);
			bzero(input, sizeof(input));
			continue;
		}

		read(sock, input, sizeof(input));
		if (!strcmp(input, "Line(s) deleted from file")){
			printf("The updated file is :\n");
			read_file_content_from_server(sock);
		}
		
		continue;
	}

	/*
	xxxxxxxxxxxxxxxxxxxxxxxx Invite Request Incoming xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "invite_msg")){
		printf("In invitatin request\n");
		char temp[100];

		printf("Extracted invite : %s\n", extracted_cmd);

		char p0[100], p1[100], p2[100], p3[100];
		sscanf(cmd_parameter,"%s %s %s", param_1, param_2, param_3 );
		
		char perm[10], reply[5] = "123";

		if (!strcmp(param_3, "2") ){
			strcpy(perm, "EDITOR");
		}else{
			strcpy(perm, "VIEWER");
		}
		
		// int bytes;

		printf("User %s has invited you to be %s on file %s\n", param_1, perm, param_2);

		printf("Enter reply yes/no : \n");
		
		bzero(reply,sizeof(reply));
		
		while (  !( strncmp(reply, "yes", 3) == 0 || strncmp(reply, "no",2) == 0 )   )
		{	
			bzero(reply,sizeof(reply));
			fflush(stdin);
			fgets(reply, sizeof(reply), stdin);
		}
		// printf("Final user reply : /%s/\n", reply);

		sprintf(input, "invite_reply %d %s %s %s %s\n", sock, param_2, param_3, param_1, reply);
		write(sock, input, sizeof(input));
		printf("Reply sent to server\n");

		continue;
	}

	/*
	xxxxxxxxxxxxxxxxxxxxxxxx Invite Reply Incoming xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	
	if ( !strcmp(extracted_cmd, "User")){
		printf("%s\n", input);
		continue;
	}


	/*
	xxxxxxxxxxxxxxxxxxxxxxxxExit Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	*/	

	if ( !strcmp(extracted_cmd, "/exit")){
		write(sock, input, sizeof(input));
		read(sock, input, sizeof(input));
		printf("%s\n", input);

		// sleep(1);
		// strcpy(input, "last msg from client\n");


		close(sock);
		write(sock, input, sizeof(input));
		// fflush(stdin);
		// fflush(stdout);
		// bzero(input, sizeof(input));
		return 0;
	}

	printf("\nInvalid Command, No match found\n");
	continue;

	}
  
  return 0;
}