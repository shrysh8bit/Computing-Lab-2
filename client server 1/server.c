#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<string.h>
#include <ctype.h>

#define PORT 1481


int main(){
	//Initialise the socket
	int server_sock_id = socket(AF_INET, SOCK_STREAM, 0);

	//error check for socket open
	if (server_sock_id < 0){
		perror("Server failed to open socket ");
		exit(1);
	}else{
		printf("Socket open success with port id : %d\n", server_sock_id);
	}

	//Iniptialise env for sockaddr structure
	struct sockaddr_in server;
	server.sin_family = AF_INET;
	server.sin_port = htons(PORT);
	server.sin_addr.s_addr =  INADDR_ANY; // inet_addr( "127.0.0.1") ; 
	memset ( &(server.sin_zero), 0, 8 );


	//Bind to local port
	int server_bind_id;
	server_bind_id = bind( server_sock_id , (struct sockaddr*)&server, sizeof(struct sockaddr) );

	if (server_bind_id < 0){
		perror("Server failed to bind ");
		exit(1);
	}else{
		printf("Bind success \n");
	}

	//Listen for request fm client
	int listen_id = listen(server_sock_id, 10);

	if (server_bind_id < 0){
		// printf("failed to listen\n");
		perror("\nServer failed to listen ");
		exit(1);
	}else{
		printf("Started listening \n");
	}

	//wait for new request and proceed
	struct sockaddr_in client;
	socklen_t client_size;
	client_size = sizeof(client);

	char send[256];
	char receive[256];

	int client_id;
	
	client_id = accept(server_sock_id, (struct sockaddr*)&client, &client_size );



	while (1){
		
		printf("\n\nStart of new iteration\n");
		
		char alph[246], incoming_cmd[256];
		char cmd[8] = {}, movie_name[256] = {}, line[8] = {};

		read(client_id, incoming_cmd, sizeof(incoming_cmd));
		printf("Incoming cmd fm client : %s", incoming_cmd);
		fflush(stdin);

		sscanf(incoming_cmd, "%[^' '\n] %[^' '\n] %[^\n]", cmd, line, movie_name);
		printf("Cmd : %s\n", cmd);
		if(strlen(line) != 0) printf("Line num : %s\n", line);
		if(strlen(movie_name) != 0) printf("Movie : %s\n", movie_name);
		
		FILE *fp;
		fp = fopen("server_file.txt", "r+");

		int total_lines = 0;
		while (fgets(alph, sizeof(alph), fp)) { 
			total_lines++;
		}

		if(!strcmp(cmd, "exit")){
			printf("Closing connection to client\n");
			sprintf(send, "exit" );
			write(client_id, send, sizeof(send));
			break;
		}



		if(!strcmp(cmd, "NLINEX")){
			sprintf(send, "The file contains %d lines\n", total_lines);
			write(client_id, send, sizeof(send));
			continue;

		}


		int final_line_num;

		int num_only = 1;
		char low = 0, high = 9;

		for (int i = 0; i < sizeof(line); i++){
			if (isalpha(line[i])){
				num_only = 0; 
				break;
				}
		}




		if (!strcmp(cmd, "READX")){
			
			if(num_only){
				final_line_num = atoi(line);
			}else{
				final_line_num = 0;
			}
						
			rewind (fp);
			
			if (final_line_num < -total_lines || final_line_num >= total_lines ){
				sprintf(send, "Line number out of index" );
				write(client_id, send, sizeof(send));
				continue;
			}

			final_line_num += total_lines;
			final_line_num = final_line_num%total_lines;

			rewind(fp);
			for (int i = 0; i <= final_line_num; i++){
				fgets(alph,sizeof(alph), fp );
			}

			sprintf(send, "Line is %s\n", alph);
			write(client_id, send, sizeof(send));
			continue;
		}





		if (!strcmp(cmd, "INSERTX")){
			char movie_temp[266];

			if(num_only){
				final_line_num = atoi(line);

				if (final_line_num < -total_lines || final_line_num >= total_lines ){
					sprintf(send, "Line number out of index" );
					write(client_id, send, sizeof(send));
					continue;
				}

				final_line_num += total_lines;
				final_line_num = final_line_num%total_lines;
				
				rewind(fp);
				FILE *ins;
				ins = fopen("temp.txt", "w+");

				for ( int j = 0 ; j < final_line_num ; j++){
					fgets(alph, sizeof(alph), fp);
					fprintf(ins, "%s", alph);
				}
			
				fprintf(ins, "%d\t%s\n", ++final_line_num, movie_name);
				
				while( fgets(alph, sizeof(alph), fp) ){
					sscanf(alph,"%s %[^\n]", line, movie_name );
					final_line_num = atoi(line);

					fprintf(ins, "%d\t%s\n",++final_line_num, movie_name );
				}
				
				total_lines = 0;
				while (fgets(alph, sizeof(alph), fp)) { 
					total_lines++;
				}

				fclose(ins);
				char old_name[] = "temp.txt", new_name[] = "server_file.txt";
				rename(old_name, new_name);
				
				sprintf(send, "Line added to file\n");
				write(client_id, send, sizeof(send));
				continue;
				
			}else{

				final_line_num = total_lines + 1;
				strcpy(movie_temp, movie_name);
				sprintf(movie_temp, "%s %s\n", line, movie_name);
				strcpy(movie_name, movie_temp);

				rewind(fp);
				FILE *ins;
				ins = fopen("server_file.txt", "a");

				final_line_num = total_lines + 1;
				fprintf(ins, "%d\t%s", final_line_num, movie_name);

				fclose(ins);

				sprintf(send, "Line added to file\n");
				write(client_id, send, sizeof(send));
				continue;
			}
		}
		sprintf(send, "Incorrect command entered\n");
		write(client_id, send, sizeof(send));
		continue;
		fclose(fp);
	}
	close(client_id);
	return 0;
}



