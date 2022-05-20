// Server side implementation of UDP client-server model
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#include <iostream>
#include <random>
#include <string>

#define PORT 8888
#define BUFFER_SIZE 256

int create_socket() {
    // Create socket file descriptor
    int socket_file_descriptor = socket(AF_INET, SOCK_DGRAM, 0);

    if (socket_file_descriptor < 0) {
        std::cerr << "Create_Socket: creation failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    return socket_file_descriptor;
}

void setup_server_address(sockaddr_in &server_address) {
    memset(&server_address, 0, sizeof(server_address));

    // Fill server information
    server_address.sin_family = AF_INET;  // IPv4
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(PORT);
}

void setup_client_address(sockaddr_in &client_address) {
    memset(&client_address, 0, sizeof(client_address));
}

void bind_socket(int &socket_file_descriptor, struct sockaddr_in &server_address) {
    // Bind the socket with the server address
    int status = bind(socket_file_descriptor, (const struct sockaddr *)&server_address,
                      sizeof(server_address));
    if (status < 0) {
        std::cerr << "Bind: failed" << std::endl;
        exit(EXIT_FAILURE);
    }
}

void send(int &socket_file_descriptor, const std::string &message,
          const sockaddr_in &client_address) {
    socklen_t length = sizeof(client_address);

    int sent = sendto(socket_file_descriptor, message.c_str(), message.size() + 1, MSG_CONFIRM,
                      (const sockaddr *)&client_address, length);

    if (sent < 0) {
        std::cerr << "Send: failed" << std::endl;
        exit(EXIT_FAILURE);
    }
}

void receive(int &socket_file_descriptor, char *buffer, sockaddr_in &client_address) {
    socklen_t length = sizeof(client_address);
    int received = recvfrom(socket_file_descriptor, buffer, BUFFER_SIZE, MSG_WAITALL,
                            (sockaddr *)&client_address, &length);
    if (received < 0) {
        std::cerr << "Receive: failed" << std::endl;
        exit(EXIT_FAILURE);
    }
    buffer[received] = '\0';
}

int main() {
    srand(3141592);

    char buffer[BUFFER_SIZE];

    int socket_file_descriptor = create_socket();

    struct sockaddr_in server_address;
    setup_server_address(server_address);

    struct sockaddr_in client_address;
    setup_client_address(client_address);

    bind_socket(socket_file_descriptor, server_address);

    std::cout << "Hello, Connection!" << std::endl;

    // Start UDP connection
    receive(socket_file_descriptor, buffer, client_address);

    std::cout << "Hello, Client!" << std::endl;

    int i = 0;
    while (true) {
        // FIXME: Poll & dont send on pollhup or timeout
        send(socket_file_descriptor, std::to_string(i) + "," + std::to_string(random() % 10 + 90),
             client_address);

        usleep(250000);  // simulate measuring distance

        i = (i + 5) % 360;
    }

    return 0;
}