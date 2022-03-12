#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/shm.h>
#include <time.h>
#include <ctype.h>

#define PORT 57908

int  client_id[10][2] = {0};

struct permissions{
	int id;
	char file_name[100];
	int permission;
	int lines;
};
struct permissions file_permission[100];

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Client Socket to Id xxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int socket_to_id(int socket){

	for (int i = 0; i < 10 ; i++){
		if (client_id[i][1] == socket){
			return client_id[i][0];
		}
	}

	return 0;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Client Id to Socket xxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int id_to_socket(int id){

	for(int i = 0; i < 10; i++){
		if (client_id[i][0] == id){
			return client_id[i][1];
		}
	}
	return 0;

}

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Check If Uploaded File Is Dupl xxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/

int is_dupl(char file_name[100], int socket){
	int dupl = 0;
	printf("Checking file : %s for duplicates\n", file_name);
	for (int i = 0; i < 100; i++){
		
		if( !strcmp(file_permission[i].file_name, file_name)){
			printf("File with same name exists at server\n");
			dupl =  1;
		}
	}
	
	if (dupl){
		char err[10] = "duplicate";
		write(socket, err, sizeof(err));

		char err1[1024] = "Upload failed due to file being duplicate";
		write(socket, err1, sizeof(err1));

		return 1;
	}else{
		char err[10] = "not dupl";
		write(socket, err, sizeof(err));
	}

	printf("File not dupl\n");
	return 0;
}


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
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxReceive File From Clientxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void receive_file(char file_name[100], int socket_fd){   
	
	printf("\nReceiving file %s fm client\n", file_name);
	char cmd_parameter[] = "recv.txt";

	FILE *fp;
	fp = fopen(cmd_parameter, "w");

    int lines;
    char file_contents[1024] = {0};

	read(socket_fd, file_contents, sizeof(file_contents));
	reverse(file_contents, 0, strlen(file_contents) - 1);

	lines = atoi(file_contents);
	printf("Lines incoming : %d\n", lines);

	bzero(file_contents, 1024);
	fflush(stdin);
	fflush(stdout);
	printf("Num of lines received\n");
    for (int i = 0; i < lines; i++) {

		fflush(stdin);
		fflush(stdout);
		read(socket_fd, file_contents, sizeof(file_contents));
		fprintf(fp, "%s", file_contents);
        bzero(file_contents, 1024);
		printf("Num of lines received : %d\n", i);
       
    }
	fclose(fp);
	printf("File received to server fm client\n");

	rename(cmd_parameter, file_name);

	char msg[1024] = "File sucessfully received at server";
	write(socket_fd, msg, sizeof(msg));

	return;
}


/*
xxxxxxxxxxxxxxxxxxxxxxxxSend File To CLient From Server To Clientxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void send_file(char file_name[100], int socket_fd){   

	printf("\nSending file %s to server\n", file_name);
	FILE *fp;
	fp = fopen(file_name, "r");

    int lines_in_file = 0;
    char file_contents[1024];

    while(fgets(file_contents, sizeof(file_contents), fp) != NULL) {
		lines_in_file = lines_in_file + 1;
	}

	int i  = 0;
	bzero(file_contents, 1024);

	while (lines_in_file){
		file_contents[i] = lines_in_file%10 + 48 ;
		lines_in_file = lines_in_file/10;
		i++;
	}

	reverse(file_contents, 0, strlen(file_contents) - 1);

	printf("Lines in outgoing file : %s\n", file_contents);

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

	printf("File sent to server\n");
	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxSend File To CLient From Server To Clientxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void update_line_count(char filename[100]){
	char temp[100];
	int lines = 0;

	FILE *fp;
	fp = fopen(filename, "r");
	while(fgets(temp, sizeof(temp), fp) != NULL){
		lines++;
	}

	for (int i = 0; i < 100; i++){
		if (!strcmp(filename, file_permission[i].file_name)){
			file_permission[i].lines = lines;
		}
	}

	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Generate Random 5 Digit Client Id xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void new_client_id( int socket){
	
	srand(time(NULL));
	int client_rand_id;

	while (1)
	{
		client_rand_id = 10000 + rand () % 90000;

		for (int i = 0; i < 10; i++){
			if (client_id[i][0] == client_rand_id);
			continue;
		}
		break;
	}

	for (int i = 0; i < 10; i++){
		if ( client_id[i][0] == 0){
			client_id[i][0] = client_rand_id;
			client_id[i][1] = socket;
			break;
		}
	}
	printf("Client id : %d at Socket : %d created\n", client_rand_id, socket);

	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Send Connected Clients Ids xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void send_user_list(int socket){

	printf("Sending client info\n");
	int id;
	char send[10];

	for (int i = 0; i < 5; i++){
		id  = client_id[i][0];
		// send_id(id, socket);
		bzero(send, sizeof(send));
		int j = 0;
		while (id){
			send[j] = id%10 + 48 ;
			id = id/10;
			j++;
		}

		reverse(send, 0, strlen(send) - 1);

		printf("sending id : %s\n", send);
		write(socket, send, sizeof(send));
	}
	
	
	printf("Sent\n");

	return ;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Send File List To Client xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void send_file_list(int socket){

	printf("Sending file info\n");
	// int id;
	char send[1024];

	for (int i = 0; i < 100; i++){
		bzero(send, sizeof(send));
		sprintf (send, "%d %s %d %d", file_permission[i].id, file_permission[i].file_name,
			file_permission[i].permission, file_permission[i].lines );
		
		write(socket, send, sizeof(send));
	}
	
	printf("Sent\n");
	return ;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Send Connected Clients Ids xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void update_file_permission(int socket, int permission, char file[100]){
	int id, line;
	char file_contents[1024];

	printf("Updating file permissions\n");

	//socket to client_id search
	for (int i = 0; i < 5; i++){
		if (client_id[i][1] == socket){
			id = client_id[i][0];
			break;
		}
	}
	printf("socket to client id : %d\n", id);

	int num_lines = 0;
	FILE *fp;
	fp = fopen(file, "r");
    while(fgets(file_contents, sizeof(file_contents), fp) != NULL) {
		num_lines++;
	}
	fclose(fp);
	
	for (int i = 0; i < 100; i++){
		if (file_permission[i].id == id && !strcmp(file_permission[i].file_name, file)){
			file_permission[i].permission = permission;
			return;
		}
	}

	//empty line in file_permission
	for (int i = 0; i < 99; i++){
		if (file_permission[i].id == 0){
			file_permission[i].id = id;
			strcpy(file_permission[i].file_name , file);
			file_permission[i].permission = permission;
			file_permission[i].lines = num_lines;
			// line = i;
			return;
		}
	}

	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Client Permission Checker xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int permission_check(int socket, char cmd_parameter[100], int permission){
	int id;
	printf("Checking client permissions\n");
	for (int i = 0; i < 5; i++){
		if (client_id[i][1] == socket){
			id = client_id[i][0];
			break;
		}
	}

	printf("Client with socket : %d has id : %d\n", socket, id);


	for (int i = 0; i < 100; i++){
		// 	file_permission[i].permission);
		if (file_permission[i].id == id && !strcmp(file_permission[i].file_name, cmd_parameter)){
			// 	file_permission[i].permission);
			if (file_permission[i].permission <= permission){
				return 1;
			}
		}
	}

	printf("Not permitted\n");
	return 0;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Read File Content To Client xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void read_file_content_to_client(int socket, char file[100], int start, int stop){

	FILE *fp;
	fp = fopen(file, "r");

	char file_content[1024];
	int lines = 0, temp, i =0;

	while (fgets(file_content, sizeof(file_content), fp)){
		lines++;
	}

	if (start < -lines || start >= lines || stop < -lines || stop >= lines ){
		sprintf(file_content, "Line number out of index" );
		write(socket, file_content, sizeof(file_content));
		return;
	}else{
		sprintf(file_content, "Line number valid" );
		write(socket, file_content, sizeof(file_content));
	}


	printf("Start : %d\t\t Stop : %d\n", start, stop);
	
	start += lines;
	start = start%lines;

	stop += lines;
	stop = stop%lines;

	int initial_skip, to_read;

	initial_skip = start;
	to_read = stop - start + 1;

	printf("To read : %d\n", to_read);


	temp = to_read;
	bzero(file_content, 1024);
	
	while (temp){
		file_content[i] = temp%10 + 48 ;
		temp = temp/10;
		i++;
	}

	reverse(file_content, 0, strlen(file_content) - 1);

	printf("Lines in outgoing read : %s\n", file_content);
	write(socket, file_content, sizeof(file_content));

	rewind(fp);

	for (int i = 0; i < initial_skip; i++){
		fgets(file_content, sizeof(file_content), fp);
	}

	for (int i = 0; i < to_read; i++){
		bzero(file_content, sizeof(file_content));
		fgets(file_content, sizeof(file_content), fp);
		write(socket, file_content, sizeof(file_content));
	}

	fclose(fp);

	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx File Existence and Permission Check xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int file_and_permission_check(int curr_socket, char filename[100], int permission){

	int file_exist = 0;
	for (int i = 0; i < 100; i++){
		if (  !strcmp(file_permission[i].file_name, filename) ){
			file_exist = 1;
			break;
		}
	}

	if (!file_exist){
		char reply[5] = "huh!";
		write(curr_socket, reply, sizeof(reply));
		return 0;
	}


	//permission check
	int permission_reply;
	permission_reply = permission_check(curr_socket, filename, permission);
	printf ("reply fm permission check : %d\n", permission_reply);

	if (permission_reply){
		char reply[5] = "yes";
		write(curr_socket, reply, sizeof(reply));
	}else{
		char reply[5] = "no";
		write(curr_socket, reply, sizeof(reply));
		return 0;;
	}

	return 1;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Insert In File xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void insert_in_file(char filename[100], int index, char contents[1024], int curr_socket){
	printf("In insert in file module\n");
	printf("%s %d -%s-", filename, index, contents);

	int lines_in_file = 0;
	char temp[1024];

	FILE *fp;
	fp = fopen(filename, "r");
	while(fgets(temp, sizeof(temp), fp)){
		lines_in_file++;
	}
	// final_line_num = atoi(line);
	printf("Pre check : %d  , lines : %d\n", index, lines_in_file);

	if (index < -lines_in_file || index >= lines_in_file ){
		sprintf(temp, "Line number out of index" );
		write(curr_socket, temp, sizeof(temp));
		printf("%s\n", temp);
		return;
	}else{
		sprintf(temp, "Line number valid" );
		write(curr_socket, temp, sizeof(temp));
		printf("%s\n", temp);

	}

	printf("Inserting at : %d  , lines : %d\n", index, lines_in_file);
	index += lines_in_file ;
	index = index%lines_in_file;
	printf("Final inserting at : %d\n", index);
	
	rewind(fp);
	FILE *ins;
	ins = fopen("temp.txt", "w+");

	for ( int j = 0 ; j < index + 1; j++){
		fgets(temp, sizeof(temp), fp);
		fprintf(ins, "%s", temp);
	}

	bzero(temp, sizeof(temp));
	for (int i = 0; i < strlen(contents) - 4; i++){
		temp[i] = contents[i + 1];
	}
	fprintf(ins, "%s\n",  temp);

	
	while( fgets(temp, sizeof(temp), fp) ){
		sscanf(temp,"%[^\n]", temp );

		fprintf(ins, "%s\n", temp );
	}
	
	
	fclose(ins);
	fclose(fp);

	rename("temp.txt", filename);
		
	sprintf(temp, "Line(s) inserted to file");
	write(curr_socket, temp, sizeof(temp));

	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx Delete From File xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int delete_from_file(char filename[100], int start, int stop, int curr_socket){
	printf("In delete from file\n");
	printf("%s %d %d %d \n", filename, start, stop, curr_socket);

	int lines_in_file = 0, index_check = 1;
	char temp[1024];

	FILE *fp;
	fp = fopen(filename, "r");
	while(fgets(temp, sizeof(temp), fp)){
		lines_in_file++;
	}

	start += lines_in_file;
	stop += lines_in_file;

	printf("Start : %d , sto p: %d, lines : %d\n", start, stop, lines_in_file);

	if (start < 0 || start > (2*lines_in_file) || stop < 0  || stop > (2*lines_in_file) ){
		index_check = 0;
	}

	printf ("Index check : %d\n", index_check);
	if (start > stop ){
		index_check = 0;
	}

	if (!index_check){
		sprintf(temp, "Line number out of index" );
		write(curr_socket, temp, sizeof(temp));
		return 1;
	}else{
		sprintf(temp, "Line number valid" );
		write(curr_socket, temp, sizeof(temp));
	}

	start = start%lines_in_file;
	stop = stop%lines_in_file;

	printf("Start : %d , stop: %d\n", start, stop);

	
	rewind(fp);
	FILE *ins;
	ins = fopen("temp.txt", "w+");

	for ( int j = 0 ; j < start  ; j++){
		fgets(temp, sizeof(temp), fp);
		fprintf(ins, "%s", temp);
	}

	for (int i = 0; i <= (stop - start); i++){
		fgets(temp, sizeof(temp), fp);
	}
	
	while( fgets(temp, sizeof(temp), fp) ){
		fprintf(ins, "%s", temp );
	}
	
	
	fclose(ins);
	fclose(fp);

	rename("temp.txt", filename);
		
	sprintf(temp, "Line(s) deleted from file");
	write(curr_socket, temp, sizeof(temp));

	return 0;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx User Exit - Data deletion xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void user_exit(int socket){
	int id = socket_to_id(socket);
	char filename[100];

	for (int i = 0; i < 100; i++){
		if (file_permission[i].id == id && file_permission[i].permission == 1){
			strcpy(filename, file_permission[i].file_name);

			for (int i = 0; i < 100; i++){
				if (!strcmp(filename, file_permission[i].file_name)){
					file_permission[i].id = 0;
					file_permission[i].lines = 0;
					file_permission[i].permission = 0;
					strcpy(file_permission[i].file_name , "0");
				}
			}
		}
	}

	for (int i = 0; i < 5; i++){
		if (client_id[i][1] == socket){
			id = client_id[i][0];
			client_id[i][0] = 0;
			client_id[i][1] = 0;
		}
	}

	char msg[1024] = "User data deleted from server, GOODBYE";
	write(socket, msg, sizeof(msg));

	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxx User Invite xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void invite_user(char file[100], int id, int permission, int socket){
	printf("\n\n Invite fn\n");
	printf("%s %d %d\n", file, id, permission);

	int invited_socket, error = 0;
	char msg[1024];

	for (int i = 0; i < 100; i++){
		if (client_id[i][0] == id){
			invited_socket = client_id[i][1];
			error = 0;
			break;
		}
		error = 1;
	}

	if (invited_socket == socket){
		error = 1;
	}

	if(error){
		strcpy(msg, "Invalid client id entered");
		write(socket, msg, sizeof(msg));
	}

	strcpy( msg, "Client invited, will inform when reply received\n");
	write(socket, msg, sizeof(msg));

	int inviting_client;

	for (int i = 0; i < 100; i++){
		if (client_id[i][1] == socket){
			inviting_client = client_id[i][0];
			break;
		}
		error = 1;
	}

	sprintf(msg, "invite_msg %d %s %d",inviting_client, file, permission);
	write(invited_socket, msg, sizeof(msg));

	return;
}


/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

xxxxxxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/


int main(){

	int sockfd, ret_val;
	int new_socket, curr_socket;

	struct sockaddr_in serverAddr;
	struct sockaddr_in newAddr;

	socklen_t addr_size;

	char buffer[1024];

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if(sockfd < 0){
		printf("Error in creating Socket\n");
		exit(1);
	}
	printf("Server Socket has been created\n");

	memset(&serverAddr, '\0', sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

	ret_val = bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
	if(ret_val < 0){
		printf("Error in binding socket\n");
		exit(1);
	}
	printf("Socket successfullly binded to port number : %d\n", PORT);

	if(listen(sockfd, 5) == 0){
		printf("Socket listening for client connection\n");
	}


	//set of socket descriptors
    fd_set readfds;

	int max_sd, max_clients = 7, client_socket[7] = {0}, sd, activity, valread;

    for (int i = 0; i < max_clients; i++) {
        client_socket[i] = 0;
    }


	int connections = 0;

	while(1){
		 
		//clear the socket set
        FD_ZERO(&readfds);

		//add master socket to set
        FD_SET(sockfd, &readfds);
		max_sd = sockfd;

		for ( int i = 0 ; i < max_clients ; i++) {
			//socket descriptor
			sd = client_socket[i];

			//if valid socket descriptor then add to read list
			if(sd > 0){
				FD_SET( sd , &readfds);
			}

			//highest file descriptor number, need it for the select function
            if(sd > max_sd){
				max_sd = sd;
			}
		}

		printf("\nWaiting for activity at select\n");
        //wait for an activity on one of the sockets 
        activity = select( max_sd + 1 , &readfds , NULL , NULL , NULL);


		//ACCEPT NEW CONNECTION
        if (FD_ISSET(sockfd, &readfds)) {
			
			/*
			xxxxxxxxxxxxxxxxxxxxxxxxAccept New Connectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
			*/
			new_socket = accept(sockfd, (struct sockaddr*)&newAddr, &addr_size);
			if(new_socket < 0){
				printf("Error in accepting new connection\n");
				continue;
			}

			//add new socket to array of sockets
			printf("Connection from client est\n");
			printf("New socket %d\n", new_socket);
			connections++;

			if (connections > 5){
				char quit_msg[] = "Max clients connected, try again later\n";
				write(new_socket, quit_msg, sizeof(quit_msg));
				close(new_socket);
				connections--;
				continue;

			}else{
				char welcome[] = "GREETINGS Client, What can I do for you today?\n";
				write(new_socket, welcome, sizeof(welcome));
			}

			//Assign client id and save socket number
			printf("Assigning random client id\n");
			new_client_id(new_socket);
			
            for (int i = 0; i < max_sd; i++) 
            {
                //if position is empty
				if( client_socket[i] == 0 ){
                    client_socket[i] = new_socket;
                    // printf("Adding to list of sockets as %d\n" , i);
					
					break;
                }
            }


			for (int i = 0; i < 5; i++){
				printf("%d		%d\n", client_id[i][0], client_id[i][1]);
			}

		}else{
			
			// Operation on existing socket
			for (int i = 0; i < max_clients; i++){
				curr_socket = client_socket[i];
				
				if (FD_ISSET(curr_socket , &readfds)){
					fflush(stdin);

					char incoming_cmd[1024], extracted_cmd[24], param_1[1024], param_2[1024], param_3[1024], param_4[1024], param_5[1024];
					int input_field_count, start_index, stop_index;


					printf("\n\nStart of new iteration, waiting for command\n");
					printf("\nCommand from client to server : ");

					bzero(incoming_cmd, sizeof(incoming_cmd));
					read(curr_socket, incoming_cmd, sizeof(incoming_cmd));
					printf("%s\n", incoming_cmd);
					fflush(stdin);

					char cmd_parameter[1000];
					input_field_count = sscanf(incoming_cmd,"%s %[^\n]",extracted_cmd, cmd_parameter );


					/*
					xxxxxxxxxxxxxxxxxxxxxxxx /users commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/	
					if ( !strcmp(extracted_cmd, "/users") ){
						printf("In /users function\n");

						send_user_list(curr_socket);
						break;
					}

					/*
					xxxxxxxxxxxxxxxxxxxxxxxx /Files Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/	
					if ( !strcmp(extracted_cmd, "/files") ){
						printf("In /files function\n");

						send_file_list(curr_socket);
						break;
					}


					/*
					xxxxxxxxxxxxxxxxxxxxxxxx /Upload Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/
					if ( !strcmp(extracted_cmd, "/upload") ){
						printf("\nIn /upload function\n");

						//File receive
						printf("start dupl check\n");
						int dupl;
						dupl = is_dupl(cmd_parameter, curr_socket);
						printf("Finish dupl check : %d\n", dupl);

						if(!dupl){
							receive_file(cmd_parameter, curr_socket); 
							update_file_permission(curr_socket, 1, cmd_parameter);

							printf("Updated file permissions\n");
							for ( int i = 0; i < 5; i++){
								printf("%d\t%s\t%d\t%d\n", file_permission[i].id, file_permission[i].file_name, 
									file_permission[i].permission, file_permission[i].lines);
							}
						}

						break;
					}

					// /*
					// xxxxxxxxxxxxxxxxxxxxxxxx /Download Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					// */
					if ( !strcmp(extracted_cmd, "/download") ){
						printf("\nIn /download function\n");

						if (!file_and_permission_check(curr_socket, cmd_parameter, 3)){
							break;
						}

						send_file(cmd_parameter, curr_socket);

						break;
					}

					// /*
					// xxxxxxxxxxxxxxxxxxxxxxxx /Invite Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					// */
					if ( !strcmp(extracted_cmd, "/invite") ){
						printf("\nIn /invite function\n");

						input_field_count = sscanf(cmd_parameter,"%s %s %s",param_1, param_2, param_3);
						if (!file_and_permission_check(curr_socket, param_1, 1)){
							break;
						}
			
						int id = atoi(param_2);
						int perm = atoi(param_3);
						invite_user(param_1, id, perm, curr_socket);

						break;
					}

					/*
					xxxxxxxxxxxxxxxxxxxxxxxx Invite Reply From Client xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/	
					if ( !strcmp(extracted_cmd, "invite_reply") ){
						char temp_param[972];
						sscanf(cmd_parameter,"%s %s %s %s %s",param_1, temp_param, param_3, param_4, param_5);
						
						
						if (!strncmp(param_5, "yes", 3)){
							int id = socket_to_id(curr_socket);
							printf ("UPdating permissions %d %d %s\n",curr_socket, atoi(param_3), temp_param);
							update_file_permission( curr_socket, atoi(param_3), temp_param );
							
							printf("socket : %d  id : %d\n", curr_socket, id);
							sprintf(incoming_cmd, "User %d has accepted your invite for file %s\n", id, temp_param);

							id = id_to_socket(atoi(param_4));
							write(id, incoming_cmd, sizeof(incoming_cmd));
						
						}else{
							int id = socket_to_id(curr_socket);
							sprintf(incoming_cmd, "User %d has NOT accepted your invite for file %s\n", id, temp_param);

							id = id_to_socket(atoi(param_4));
							write(id, incoming_cmd, sizeof(incoming_cmd));
						}
						break;
					}


					/*
					xxxxxxxxxxxxxxxxxxxxxxxx /Read Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/
					if ( !strcmp(extracted_cmd, "/read") ){
						printf("\nIn /read function\n");

						input_field_count = sscanf(cmd_parameter,"%s %s %s",param_1, param_2, param_3 );

						if (!file_and_permission_check(curr_socket, param_1, 3)){
							break;
						}

						start_index = atoi(param_2);
						stop_index = atoi(param_3);

						printf("Input fd count in cmd : %d\n", input_field_count);
						printf("Start : %d\t Stop: %d\n",start_index, stop_index );
						
						//Cmd check
						if ( input_field_count == 1){
							read_file_content_to_client(curr_socket, param_1, 0, -1 );
						}else if(input_field_count == 2){
							read_file_content_to_client(curr_socket,param_1, start_index, start_index);
						}else{
							read_file_content_to_client(curr_socket, param_1, start_index, stop_index);
						}

						break;
					}


					/*
					xxxxxxxxxxxxxxxxxxxxxxxx /Insert Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/
					if ( !strcmp(extracted_cmd, "/insert") ){
						printf("\nIn /insert function\n");

						int index_given = 0;

						input_field_count = sscanf(cmd_parameter,"%s %s %s",param_1, param_2, param_4 );

						printf("Starting file & permission check\n");
						if (!file_and_permission_check(curr_socket, param_1, 2)){
							break;
						}

						if (input_field_count == 3){
							// sscanf(cmd_parameter,"%s %d %s",param_1, start_pt, param_4 );
							index_given = 1;
							// start_index = atoi(pa)
						}

						strcpy(param_3, incoming_cmd);
						
						int i = 0;
						while (param_3[i] != '"'){
							i++;
						}

						for (int j = 0; j < strlen(param_3) - i; j++){
							param_3[j] = param_3[j + i];
						}
						param_3[strlen(param_3) - i] = '\0';

						if (index_given){
							printf("Convert line from str to int\n");
							start_index = atoi(param_2);
							printf("p 2 : %s    start : %d\n", param_2, start_index);
							printf("Calling fn to insert, index given\n");
							
							printf ("Line for inserting : %s %s %s\n",param_1, param_2, param_3);
							insert_in_file(param_1, start_index - 1, param_3, curr_socket);
						}else{
							start_index = 0;

							FILE *fp;
							fp = fopen(param_1, "r");

							while(fgets(param_2, sizeof(param_2), fp)){
								start_index++;
							}
							fclose(fp);

							printf("Calling fn to insert, index not given\n");
							insert_in_file(param_1, start_index - 1, param_3, curr_socket);
						}

						update_line_count(param_1);
						read_file_content_to_client(curr_socket, param_1, 0, -1 );
						break;
					}


					/*
					xxxxxxxxxxxxxxxxxxxxxxxx /Delete Command xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/
					if ( !strcmp(extracted_cmd, "/delete") ){
						printf("\nIn /delete function\n");

						input_field_count = sscanf(cmd_parameter, "%s %d %d", param_1, &start_index, &stop_index );
						
						printf("Starting file & permission check\n");
						if (!file_and_permission_check(curr_socket, param_1, 2)){
							break;
						}

						if (input_field_count == 1){
							start_index = 0;
							FILE *fp;
							char temp[1000];
							fp = fopen(param_1, "r");
							while(fgets(temp, sizeof(temp), fp)){
								stop_index++;
							}
							fclose(fp);
						}else if(input_field_count == 2){
							stop_index = start_index;
						}
						
						int fail;
						fail = delete_from_file(param_1, start_index, stop_index, curr_socket);
						
						if (fail){
							break;
						}

						update_line_count(param_1);
						read_file_content_to_client(curr_socket, param_1, 0, -1 );
						
						break;
					}


					/*
					xxxxxxxxxxxxxxxxxxxxxxxxExit Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/
					if ( !strcmp(extracted_cmd, "/exit")){
						printf("Closing connection to client\n");
						user_exit(curr_socket);

						
						close(curr_socket);
						// FD_CLR(curr_socket, &readfds);
						client_socket[i] = 0;
						// fflush(stdin);
						// bzero(incoming_cmd, sizeof(incoming_cmd));
						connections--;
						break;
					}

					printf("\nInvalid Command, No match found\n");
					break;
					
				}
			}
		}
	}
	close(new_socket);

	return 0;
}

