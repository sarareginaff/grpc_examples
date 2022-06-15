package main

import (
	"log"
	"fmt"
	"io"
	"time"
	"context"
	
	"google.golang.org/grpc"
	"go_grpc/pb"
)

func main() {
	connection, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Could not connnect to grpc server %v", err)
	}
	defer connection.Close()

	client := pb.NewUserServiceClient(connection)
	// AddUser(client)
	// AddUserVerbose(client)
	// AddUsers(client)
	AddUsersVerbose(client)
}

func AddUser(client pb.UserServiceClient) {
	req := &pb.User{
		Id: "0",
		Name: "Saa",
		Email: "sara@gmail.com",
	}

	res, err := client.AddUser(context.Background(), req)
	if err != nil {
		log.Fatalf("Could not make request: %v", err)
	}

	fmt.Println(res)
}

func AddUserVerbose(client pb.UserServiceClient) {
	req := &pb.User{
		Id: "0",
		Name: "Sara",
		Email: "sara@gmail.com",
	}
	
	res, err := client.AddUserVerbose(context.Background(), req)
	if err != nil {
		log.Fatalf("Could not make request: %v", err)
	}

	for {
		stream, err := res.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("Could not receive stream: %v", err)
		}
		fmt.Println("Status: ", stream.Status, "- User: ", stream.GetUser())	
	}
}

func AddUsers(client pb.UserServiceClient) {
	reqs := CreateUsersList()

	stream, err := client.AddUsers(context.Background())
	if err != nil {
		log.Fatalf("Error creating request: %v", err)
	}

	for _, req := range reqs {
		fmt.Println("Sending user", req.GetName())
		stream.Send(req)
		time.Sleep(time.Second * 3)
	}

	res, err := stream.CloseAndRecv()
	if err != nil {
		log.Fatalf("Error receiving response: %v", err)
	}

	fmt.Println(res)
}

func AddUsersVerbose(client pb.UserServiceClient) {
	reqs := CreateUsersList()

	stream, err := client.AddUsersVerbose(context.Background())
	if err != nil {
		log.Fatalf("Error creating request: %v", err)
	}

	go func(){
		for _, req := range reqs {
			fmt.Println("Sending User: ", req.GetName())
			stream.Send(req)
			time.Sleep(time.Second * 2)
		}
		stream.CloseSend()
	}()

	wait := make(chan int)

	go func(){
		for {
			res, err := stream.Recv()
			if err == io.EOF {
				break
			}
			if err != nil {
				log.Fatalf("Error receiving data: %v", err)
				break
			}
			fmt.Printf("Receiving user %v with status %v \n", res.GetUser().GetName(), res.GetStatus())
		}
		close(wait)
	}()

	<-wait
}

func CreateUsersList() []*pb.User {
	return []*pb.User{
		&pb.User{
			Id: "0",
			Name: "Sara",
			Email: "sara@gmail.com",
		},
		&pb.User{
			Id: "1",
			Name: "Renan",
			Email: "renan@gmail.com",
		},
		&pb.User{
			Id: "2",
			Name: "Pedro",
			Email: "pedro@gmail.com",
		},
		&pb.User{
			Id: "3",
			Name: "Erik",
			Email: "erik@gmail.com",
		},
	}
}