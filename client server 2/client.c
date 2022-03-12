// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <string.h>

#define PORT 44455

/*
xxxxxxxxxxxxxxxxxxxxxxxxStruct Declarationxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/

struct fileData{
	int dd;
	int mm;
	int yyyy;
	char item_name[150];
	float price;
};


int valid_date(int dd, int mm, int yyyy){
	//check years
	if(yyyy>=1900 && yyyy<=9999){		
		
		//check months
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
xxxxxxxxxxxxxxxxxxxxxxxxCheck File Validityxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/

int is_valid(char file_name[100]){
	printf("\n\nStarting file check\n");
	
	char line[1024], item_name[100];
	int dd,mm,yyyy, value, lines  = 0;
	float item_price;

	FILE *fp;
	fp = fopen(file_name, "r");

	if ( fp == NULL){
		perror("Failed to open file : ");
		return 0; 
	}

	while (fgets(line, sizeof(line), fp)){

		value = sscanf(line, "%d.%d.%d %[^\t] %f", &dd, &mm, &yyyy, item_name, &item_price);
		lines = lines + 1;

		if (value != 5 || strlen(item_name) == 0) {

				printf("Error on line : %d of file : %s\n", lines, file_name);
				printf("Please upload valid file\n");
				return 0;
		}

		if (  !(value = valid_date(dd,mm, yyyy))  ){
			printf("Error on line : %d of file : %s\n", lines, file_name);
			printf("Please upload valid file\n");
			return 0;
		}
	}

	printf("File %s is valid\n", file_name);
	return 1;
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
xxxxxxxxxxxxxxxxxxxxxxxxSend File To CLient From Client To Serverxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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

			perror("[-]Error in sending file.");
			return;
        }
        bzero(file_contents, 1024);

    }
	fclose(fp);
	printf("File sent to server\n");
	return;
}


/*
xxxxxxxxxxxxxxxxxxxxxxxxReceive File From Serverxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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


void print_file(char file[10]){
	printf("Printing similar entries\n");
	char file_data[200];
	FILE *fp;
	fp = fopen(file, "r");

	while(fgets(file_data, sizeof(file_data), fp )){
		printf("%s\n", file_data);
	}

	fclose(fp);
	printf("Finished printing similar entries\n");

	return;
}

/*
xxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

xxxxxxxxxxxxxxxxxxxxxxxxStart Of Main Functionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*/

int main()
{
	int sock = 0;
	struct sockaddr_in serv_addr;

	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		printf("\n Socket creation error \n");
		return -1;
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
	char message[100];

	read(sock, message, sizeof(message));

	if ( !strcmp(message, "Max clients connected, try again later") ){
		printf("\nMessage from server : \n%s\n", message);
		return 0;
	}else{
		printf("\nMessage from server :\n %s\n", message);
	}

	while(1){

		printf("\n\nCommands available to user:\n");
		printf("1. Sort file 			: /sort <filename> <field> (D/N/P)\n");
		printf("2. Merge two files 		: /merge <filename 1> <filename2> <filename3> <field> (D/N/P)\n");
		printf("3. Similarity of two files	: /similarity <filename 1> <filename2>\n");
		printf("4. Exit the client program	: /exit\n\n");
		


		char input_cmd[1024], cmd[15], file1[100], file2[100], file3[100], field[1];
		int input_field_count;

		printf("Cmd at client from user : ");

		bzero(input_cmd, sizeof(input_cmd));
		fgets(input_cmd, sizeof(input_cmd), stdin);
		fflush(stdin);

		char temp[1000];
		input_field_count = sscanf(input_cmd,"%s %[^\n]",cmd, temp );

		/*
		xxxxxxxxxxxxxxxxxxxxxxxxSort Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
		*/	
		if ( !strcmp(cmd, "/sort")){
			printf("In /sort function\n");

			input_field_count = sscanf(temp,"%s %s %s %s",file1, file2, file3, field );


			//Cmd check
			if ( input_field_count != 2){
				printf("Invalid input by user\n");
				continue;
			}

			if (file2[0] != 68 && file2[0] != 78 && file2[0] != 80){
				printf("Invalid input by user\n");
				continue;
			}


			//Send cmd to server
			write(sock, input_cmd, sizeof(input_cmd));
		
			//Send file to server
			send_file(file1, sock);


			//File validity by server
			char check_reply[64];

			read (sock, check_reply, sizeof(check_reply));

			if (!strcmp(check_reply, "error")){
				printf("File validity check : %s\n", check_reply);
				continue;
			}else{
				printf("File validity check : pass\n");
			}

			//Receive sorted file from server
			receive_file(file1, sock);
	
			continue;
		}


		/*
		xxxxxxxxxxxxxxxxxxxxxxxxMerge Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
		*/	

		if ( !strcmp(cmd, "/merge")){
			
			printf("\nIn /merge function\n");	
			input_field_count = sscanf(temp,"%s %s %s %s",file1, file2, file3, field );

			//Cmd check
			if ( input_field_count != 4){
				printf("Invalid input by user\n");
				continue;
			}
			
			//Send cmd to server
			fflush(stdin);

			write(sock, input_cmd, sizeof(input_cmd));
			fflush(stdin);

			//Send file to server
			send_file(file1, sock);
			send_file(file2, sock);

			
			//Valid file check_reply
			char check_reply[64];

			read(sock, check_reply, sizeof(check_reply));
			// printf("Validity reply : %s\n", check_reply);
			
			if (!strcmp(check_reply, "error")){
				printf("\nError in file : %s, pl upload valid file\n", file1);
				continue;
			}else{
				printf("\nFile : %s passed validity check\n", file1);
			}

			read(sock, check_reply, sizeof(check_reply));
			// printf("Validity reply : %s\n", check_reply);
			
			if (!strcmp(check_reply, "error")){
				printf("Error in file : %s, pl upload valid file\n", file2);
				continue;
			}else{
				printf("File : %s passed validity check\n", file2);
			}


			//sort check
			char sort_return[6] = "pass1";

			read(sock, sort_return, sizeof(sort_return));
			// printf("Sort check reply : %s\n", sort_return);

			if (!strcmp(sort_return, "error")){
				printf("\nFile : %s is not sorted, pl upload valid file\n", file1);
				continue;	
			}else{
				printf("\nFile : %s passed sorting ceck\n", file1);
			}
			
			read(sock, sort_return, sizeof(sort_return));
			// printf("Sort check reply : %s\n", sort_return);

			if (!strcmp(sort_return, "error")){
				printf("File : %s is not sorted, pl upload valid file\n", file2);
				continue;	
			}else{
				printf("File : %s passed sorting ceck\n", file2);

			}

			//Receive sorted file from server
			receive_file(file3, sock);
			// print_file(file3);
			continue;
		}


		/*
		xxxxxxxxxxxxxxxxxxxxxxxxSimilarity Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
		*/	

		if ( !strcmp(cmd, "/similarity")){
			printf("\nIn /similarity functionn\n");

			input_field_count = sscanf(temp,"%s %s %s %s",file1, file2, file3, field );

			//Cmd check
			if ( input_field_count != 2){
				printf("Invalid input by user\n");
				continue;
			}

			//Send cmd to server
			fflush(stdin);
			write(sock, input_cmd, sizeof(input_cmd));
			fflush(stdin);

			//Send file to server
			send_file(file1, sock);
			send_file(file2, sock);


			char check_reply[64];

			read(sock, check_reply, sizeof(check_reply));
			if (!strcmp(check_reply, "error")){
				printf("\nError in file : %s, pl upload valid file\n", file1);
				continue;
			}else{
				printf("\n\nFile : %s passed validity check\n", file1);
			}

			read(sock, check_reply, sizeof(check_reply));
			if (!strcmp(check_reply, "error")){
				printf("Error in file : %s, pl upload valid file\n", file2);
				continue;
			}else{
				printf("File : %s passed validity check\n", file2);
			}
			
			strcpy(file3, "sim.txt");
			receive_file(file3, sock);

			print_file(file3);
			continue;

		}

		/*
		xxxxxxxxxxxxxxxxxxxxxxxxExit Commandxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
		*/	

		if ( !strcmp(cmd, "/exit")){
			write(sock, input_cmd, sizeof(input_cmd));
			close(sock);
			break;
		}

		printf("\nInvalid Command, No match found\n");
		continue;
	}
  
  return 0;
}
