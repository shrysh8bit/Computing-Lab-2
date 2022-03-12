#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 44455

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxStruct Declarationxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
struct fileData{
	int dd;
	int mm;
	int yyyy;
	char item_name[150];
	float price;
};

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxReceive File From Clientxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void receive_file(char file_name[100], int socket_fd){   
	
	printf("\nReceiving file %s fm client\n", file_name);
	char temp[] = "recv.txt";

	FILE *fp;
	fp = fopen(temp, "w");

    int lines;
    char file_contents[1024] = {0};

	read(socket_fd, file_contents, sizeof(file_contents));
	lines = atoi(file_contents);
	printf("Lines incoming : %d\n", lines);

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
	printf("File received to server fm client\n");
	rename(temp, file_name);
	return;
}


/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxCheck Date Validityxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int valid_date(int dd, int mm, int yyyy){

	if(yyyy>=1900 && yyyy<=9999){
        //check month
        if(mm>=1 && mm<=12){
            //check days
            if((dd>=1 && dd<=31) && (mm==1 || mm==3 || mm==5 || mm==7 || mm==8 || mm==10 || mm==12)){

			} else if((dd>=1 && dd<=30) && (mm==4 || mm==6 || mm==9 || mm==11)){

			} else if((dd>=1 && dd<=28) && (mm==2)){

			} else if(dd==29 && mm==2 && (yyyy%400==0 ||(yyyy%4==0 && yyyy%100!=0))){

			} else{
				return 0;
			}
        }
        else{
			return 0;
        }
    } else{
		return 0;
    }
 
    return 1;    
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxCheck File Validityxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int is_valid(char file_name[100], int new_socket){
	printf("\nStarting file check on : %s\n", file_name);
	
	char line[1024], item_name[100], err_msg[64] = "error";
	int dd,mm,yyyy, value, lines  = 0;
	float item_price;

	FILE *fp;
	fp = fopen(file_name, "r");

	if ( fp == NULL){
		perror("Failed to open file : ");
		// exit(0);
		return 0; 
	}

	while (fgets(line, sizeof(line), fp)){

		value = sscanf(line, "%d.%d.%d %[^\t] %f", &dd, &mm, &yyyy, item_name, &item_price);
		lines = lines + 1;

		if (value != 5 || strlen(item_name) == 0) {

				write(new_socket, err_msg, sizeof(err_msg));
				return 0;
		}

		if (  !(value = valid_date(dd,mm, yyyy))  ){
			
			write(new_socket, err_msg, sizeof(err_msg));
			return 0;
		}
	}
	sprintf(err_msg, "pass");
	write(new_socket, err_msg, sizeof(err_msg));

	printf("File is valid\n");
	return 1;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxSwap Structure Contentsxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void swap(struct fileData *a, struct fileData *b){

	struct fileData temp;

	temp = *a;
	*a = *b;
	*b = temp;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxSort File Sent By Clientxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void sort_file(char file_name[], int field){
	
	FILE *fp;
	fp = fopen(file_name, "r");

	char data[1024];
	struct fileData file_content[2000];
	int lines = 0;

	while (fgets(data, sizeof(data), fp)) {
		
		sscanf(data, "%d.%d.%d %[^\t] %f", &file_content[lines].dd ,&file_content[lines].mm,
			&file_content[lines].yyyy, file_content[lines].item_name, &file_content[lines].price );
		
		lines++;
	}


	for (int i = 0; i < lines - 1; i++){
		for ( int j = 0; j < lines - (i + 1); j++){
			if (field == 68){

				if (file_content[j].dd > file_content[j + 1].dd){
					swap (&file_content[j], &file_content[j + 1]);
				}

				if (file_content[j].mm > file_content[j + 1].mm){					
					swap (&file_content[j], &file_content[j + 1]);
				}

				if (file_content[j].yyyy > file_content[j + 1].yyyy){
					swap (&file_content[j], &file_content[j + 1]);
				}
			
			}else if (field == 78){
			
				if (  strcmp(file_content[j].item_name , file_content[j + 1].item_name) > 0    ){
					swap (&file_content[j], &file_content[j + 1]);
				}

			}else if (field == 80){
				
				if (file_content[j].price > file_content[j + 1].price){
					swap (&file_content[j], &file_content[j + 1]);
				}
			}	
		}
	}

	FILE *wr;

	wr = fopen("temp.txt", "w+");

	for ( int i = 0; i < lines; i++){

		sprintf(data, "%2d.%2d.%2d\t%50s\t%f\n", file_content[i].dd ,file_content[i].mm,
				file_content[i].yyyy, file_content[i].item_name, file_content[i].price );
		fprintf (wr, "%s", data);
	}

	fclose(wr);
	fclose (fp);
	rename("temp.txt", file_name);

}

/*
xxxxxxxxxxxxxxxxxxxxxxxxReverse String (Sub Function to Send & Receive File)xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void reverse(char *x, int begin, int end)
{
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
xxxxxxxxxxxxxxxxxxxxxxxxSend File From Server To Clientxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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
	printf("Lines outgoing in file_content : %s\n", file_contents);

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
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxMerge Two Filesxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void merge(char file1[], char file2[], char file3[]){

	printf("\nMerging files\n");
	char data[1024];
	FILE *f1, *f2, *f3;
	f1 = fopen(file1, "r");
	f2 = fopen(file2, "r");
	f3 = fopen(file3, "w+");

	while (fgets(data, sizeof(data), f1)) {

		fprintf (f3, "%s", data);
	}

	while (fgets(data, sizeof(data), f2)) {
		
		fprintf (f3, "%s", data);
	}

	fclose (f1);
	fclose (f2);
	fclose (f3);

	printf("Files Mergerd\n");
	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxSimilarity Of Two Filesxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
void similarity(char file1[], char file2[], char file3[]){
	char data[1024];
	int lines1 = 0, lines2  = 0;
	struct fileData contents1[2000], contents2[2000];
	FILE *fp1, *fp2, *fp3;

	fp1 = fopen(file1, "r");
	while (fgets(data, sizeof(data), fp1)){
		
		sscanf(data, "%d.%d.%d %[^\t] %f", &contents1[lines1].dd ,&contents1[lines1].mm,
			&contents1[lines1].yyyy, contents1[lines1].item_name, &contents1[lines1].price );
		
		lines1++;
	}
	fclose(fp1);

	fp2 = fopen(file2, "r");
	while (fgets(data, sizeof(data), fp2)){
		
		sscanf(data, "%d.%d.%d %[^\t] %f", &contents2[lines2].dd ,&contents2[lines2].mm,
			&contents2[lines2].yyyy, contents2[lines2].item_name, &contents2[lines2].price );
		
		lines2++;
	}
	fclose(fp2);


	fp3 = fopen(file3, "w");
	printf("The similar entries in %s and %s are :\n", file1, file2);
	for (int i = 0; i < lines1; i++){
		for ( int j = 0; j < lines2; j++){
			if (   (contents1[i].dd == contents2[j].dd  && contents1[i].mm == contents2[j].mm && contents1[i].yyyy == contents2[j].yyyy )
					|| contents1[i].item_name == contents2[j].item_name || contents1[i].price == contents2[j].price )
			{
				sprintf(data, "%d.%d.%d\t%50s\t%0.2f\t|\t%d.%d.%d\t%50s\t%0.2f\n", contents1[i].dd, contents1[i].mm, contents1[i].yyyy,
						contents1[i].item_name, contents1[i].price, contents2[j].dd, contents2[j].mm, contents2[j].yyyy,
						contents2[j].item_name, contents2[j].price );
				fprintf(fp3, "%s", data);
				// printf("%s",data);
			}
		}
	}

	fclose(fp3);
}


/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxCheck If File Is Sortedxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/
int is_sorted(char file_name[100], int field, int new_socket){

	printf("\nChecking if file : %s is sorted on : %d\n", file_name, field);
	FILE *fp;
	fp = fopen(file_name, "r");

	int lines = 0, return_val = 1;
	char data[1024];
	struct fileData file_contents[2000];
	
	while ( fgets(data, sizeof(data), fp)){
		sscanf(data, "%d.%d.%d %[^\t] %f", &file_contents[lines].dd ,&file_contents[lines].mm,
			&file_contents[lines].yyyy, file_contents[lines].item_name, &file_contents[lines].price );
		
		lines++;
	}
	fclose(fp);

	for (int i = 0; i < lines -1 ; i++){
		if (field == 68){
			
			if (file_contents[i].yyyy < file_contents[i + 1].yyyy){
				continue;
			}else if (file_contents[i].yyyy > file_contents[i + 1].yyyy){
				return_val = 0;
				break;
			}else{
				if(file_contents[i].mm < file_contents[i+ 1].mm){
					continue;
				}else if (file_contents[i].mm > file_contents[i+1].mm){
					return_val = 0;
					break;
				}else{
					if (file_contents[i].dd <= file_contents[i+1].dd){
						continue;
					}else{
						return_val = 0;
						break;
					}
				}
			}
		}

		if (field == 78){
			if (strcmp(file_contents[i].item_name , file_contents[i + 1].item_name) > 0){
				return_val =  0;
				break;

			}
		}

		if (field == 80){
			if (file_contents[i].price > file_contents[i + 1].price){
				return_val =  0;
				break;

			}
		}
	}

	char sort_return[6] = "pass1";

	if (return_val){
		printf("File is sorted\n");
		write(new_socket, sort_return, sizeof(sort_return));
	}else{
		printf("File is NOT sorted\n");
		sprintf(sort_return, "error");
		write(new_socket, sort_return, sizeof(sort_return));
	}

	return return_val;
}



/*
xxxxxxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

xxxxxxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/

int main(){

	int sock_fd, ret_val;
	int new_socket;

	struct sockaddr_in server_addr;
	struct sockaddr_in new_addr;

	socklen_t addr_size;


	sock_fd = socket(AF_INET, SOCK_STREAM, 0);
	if(sock_fd < 0){
		printf("Error in creating Socket\n");
		exit(1);
	}
	printf("Server Socket has been created\n");

	memset(&server_addr, '\0', sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(PORT);
	server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

	ret_val = bind(sock_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
	if(ret_val < 0){
		printf("Error in binding socket\n");
		exit(1);
	}
	printf("Socket successfullly binded to port number : %d\n", PORT);

	if(listen(sock_fd, 15) == 0){
		printf("Socket listening for client connection\n");
	}


	//set of socket descriptors
    fd_set read_fd;

	int max_sd, max_clients = 20, client_socket[20] = {0}, socket_descriptor;

    for (int i = 0; i < max_clients; i++) {
        client_socket[i] = 0;
    }

	int connections = 1;

	while(1){
		 
        FD_ZERO(&read_fd);
        FD_SET(sock_fd, &read_fd);
		max_sd = sock_fd;

		for ( int i = 0 ; i < max_clients ; i++) {
			socket_descriptor = client_socket[i];

			if(socket_descriptor > 0){
				FD_SET( socket_descriptor , &read_fd);
			}

            if(socket_descriptor > max_sd){
				max_sd = socket_descriptor;
			}
		}

		printf("Waiting at select for file descriptors\n");
        select( max_sd + 1 , &read_fd , NULL , NULL , NULL);


		//ACCEPT NEW CONNECTION
        if (FD_ISSET(sock_fd, &read_fd)) {
			/*
			xxxxxxxxxxxxxxxxxxxxxxxxAccept New Connectionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
			*/
			new_socket = accept(sock_fd, (struct sockaddr*)&new_addr, &addr_size);
			if(new_socket < 0){
				exit(1);
			}

			//add new socket to array of sockets
			printf("New socket %d\n", new_socket);
			printf("Connection from client est\n");
			connections++;
			if (connections > 5){
				char quit_msg[] = "Max clients connected, try again later";
				write(new_socket, quit_msg, sizeof(quit_msg));
				connections--;
				close(new_socket);
				continue;

			}else{
				char welcome[] = "GREETINGS Client, What can I do for you today?\n";
				write(new_socket, welcome, sizeof(welcome));
			}

            for (int i = 0; i < max_sd; i++) 
            {
				if( client_socket[i] == 0 ){
                    client_socket[i] = new_socket;
                    printf("Adding to list of sockets as %d\n" , i);
					
					continue;
                }
            }

		}else{
			
			//else its some IO operation on some other socket :)
			for (int i = 0; i < max_clients; i++){
				socket_descriptor = client_socket[i];
				
				if (FD_ISSET( socket_descriptor , &read_fd)){

					char input_cmd[1024], cmd[15], file1[100], file2[100], file3[100], field[1];
					int input_field_count;


					printf("\n\nStart of new iteration, waiting for command\n");
					printf("\nCommand fm client to server : ");

					bzero(input_cmd, sizeof(input_cmd));
					fflush(stdin);
					
					read(new_socket, input_cmd, sizeof(input_cmd));
					printf("%s\n", input_cmd);
					fflush(stdin);
					fflush(stdout);

					char temp[1000];
					input_field_count = sscanf(input_cmd,"%s %[^\n]",cmd, temp );


					/*
					xxxxxxxxxxxxxxxxxxxxxxxxSort Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/	
					if ( !strcmp(cmd, "/sort") ){
						printf("In /sort function\n");

						input_field_count = sscanf(temp,"%s %s %s %s",file1, file2, file3, field );


						//Cmd check
						if ( input_field_count != 2){
							printf("Invalid input by user\n");
							break;
						}
				
						//File receive
						receive_file(file1, new_socket); 
						
						//File check
						if(!is_valid(file1, new_socket)) break;

						//Sort file
						int field = file2[0] - '\0';
						sort_file(file1, field);

						send_file(file1, new_socket);

						break;
					}

					/*
					xxxxxxxxxxxxxxxxxxxxxxxxMerge Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/
					if ( !strcmp(cmd, "/merge") ){
						printf("\nIn /merge function\n");

						input_field_count = sscanf(temp,"%s %s %s %s",file1, file2, file3, field );

						if ( input_field_count != 4){
							printf("Invalid input by user\n");
							break;
						}
						

						//File receive
						receive_file(file1, new_socket); 
						receive_file(file2, new_socket); 

						//File check
						if(!is_valid(file1, new_socket)) break;
						if(!is_valid(file2, new_socket)) break;

						//SORT Check
						int sort_on = field[0] - '\0';

						if (!is_sorted(file1, sort_on, new_socket)) break;
						if (!is_sorted(file2, sort_on, new_socket)) break;


						//Merge Files
						merge(file1, file2, file3);

						//Sort merged file
						int sort_field = field[0] - '\0';
						sort_file(file3, sort_field);


						printf("\nSending merged files\n");
						send_file(file3, new_socket);

						break;
					}


					/*
					xxxxxxxxxxxxxxxxxxxxxxxxSimilarity Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/	
					if ( !strcmp(cmd, "/similarity")){
						printf("\nIn /similarity function\n");
						
						input_field_count = sscanf(temp,"%s %s %s %s",file1, file2, file3, field );

						if ( input_field_count != 2){
							printf("Invalid input by user\n");
							continue;
						}

						//File receive
						receive_file(file1, new_socket); 
						receive_file(file2, new_socket); 

						//File check
						if(!is_valid(file1, new_socket)) continue;
						if(!is_valid(file2, new_socket)) continue;

						strcpy(file3, "sim.txt");
						similarity(file1, file2, file3);

						send_file(file3, new_socket);
						break;
					}
					/*
					xxxxxxxxxxxxxxxxxxxxxxxxExit Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
					*/
					if ( !strcmp(cmd, "/exit")){
						printf("\nConnection to client closed\n");
						close(new_socket);
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

