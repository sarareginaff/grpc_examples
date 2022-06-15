package services

import (
	"fmt"
	"context"
	"time"
	"io"
	"log"

	"go_grpc/pb"
)

type UserService struct {
	pb.UnimplementedUserServiceServer	
}

func NewUserService() *UserService {
	return &UserService{}
}

func (*UserService) AddUser(ctx context.Context, req *pb.User) (*pb.User, error) {
	//Exemplo: Chama o repository para inserir no BD
	fmt.Println("Inserted user", req.GetName())

	return &pb.User{
		Id: "123",
		Name: req.GetName(),
		Email: req.GetEmail(),
	}, nil
}

func (*UserService) AddUserVerbose(req *pb.User, stream pb.UserService_AddUserVerboseServer) error {
	stream.Send(&pb.UserResultStream{
		Status: "Init",
		User: &pb.User{},
	})

	//Exemplo: validação, inserir no BD...
	time.Sleep(time.Second * 3)

	stream.Send(&pb.UserResultStream{
		Status: "User has been inserted",
		User: &pb.User{
			Id: "123",
			Name: req.GetName(),
			Email: req.GetEmail(),
		},
	})

	//Sleep aqui pra indicar outras atividades que poderiam acontecer
	time.Sleep(time.Second * 3)

	stream.Send(&pb.UserResultStream{
		Status: "Completed",
		User: &pb.User{
			Id: "123",
			Name: req.GetName(),
			Email: req.GetEmail(),
		},
	})

	time.Sleep(time.Second * 3)

	return nil
}

func (*UserService) AddUsers(stream pb.UserService_AddUsersServer) error {
	users := []*pb.User{}

	for {
		req, err := stream.Recv()
		if err == io.EOF {
			return stream.SendAndClose(&pb.Users{
				User: users,
			})
		}
		if err != nil {
			log.Fatalf("Error receiveing stream: %v", err)
		}

		users = append(users, &pb.User{
			Id: req.GetId(),
			Name: req.GetName(),
			Email: req.GetEmail(),
		})
		fmt.Println("Adding user ", req.GetName())
	}
}

func (*UserService) AddUsersVerbose(stream pb.UserService_AddUsersVerboseServer) error {
	for {
		req, err := stream.Recv()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			log.Fatalf("Error receiveing stream: %v", err)
		}

		err = stream.Send(&pb.UserResultStream{
			Status: "Added",
			User: req,
		})
		if err != nil {
			log.Fatalf("Error sending stream to the client %v", err)
		}
		fmt.Println("Adding user ", req.GetName())
	}
}