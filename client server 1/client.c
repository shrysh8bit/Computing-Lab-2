// Client side C/C++ program to demonstrate Socket programming

#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

#define PORT 1481

int main()
{
	int client_socket_id;
	client_socket_id = socket (AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in server;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_family = AF_INET;
	server.sin_port = htons(PORT);
	memset (&(server.sin_zero) , 0 ,8);

	int server_id;
	char send[256] = {0};
	char receive[256];
	server_id = connect(client_socket_id, (struct sockaddr*)&server, sizeof(struct sockaddr)  );

// while(!strcmp(send, "exit")){
	printf("To close connection to server enter \"exit\" as command");
while(1){
		printf("\n\nStart of new iteration\n");

		printf("Cmd to server : ");

		fgets(send, sizeof(send), stdin);
		fflush(stdin);
		write(client_socket_id, send, sizeof(send));
		fflush(stdin);

		read(client_socket_id, receive, sizeof(receive));
		printf("Fm server : %s\n", receive);
		
		if (!strcmp(receive, "exit")){
			printf("Closing connection to server\n");
			break;
		}
		
	}

	close(client_socket_id);
	return 0;
}
