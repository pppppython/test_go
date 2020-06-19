package main

import (
	"fmt"
	"net"
	"time"
)

func main() {

	serverAddr := "127.0.0.1:8000"
	tcpAddr, err := net.ResolveTCPAddr("tcp", serverAddr)
	if err != nil {
		fmt.Println("Resolve TCPAddr error", err)
	}
	conn, err := net.DialTCP("tcp4", nil, tcpAddr)
	defer conn.Close()
	if err != nil {
		fmt.Println("connect server error", err)
	}

	//conn.Write([]byte("hello , I am client"))
	//go recv(conn)
	//time.Sleep(2 * time.Second)//等两秒钟，不然还没接收数据，程序就结束了。


	buffer := make([]byte, 1024)
	sum := 0
	for i := 0; i <= 100; i++ {
	n, err := conn.Read(buffer)
	if err == nil {
		fmt.Println("read message from server:" + string(buffer[:n]))
		fmt.Println("Message len:", n)
	}
	sum += i
	time.Sleep(1* time.Second)
    }
}


/*

func recv(conn net.Conn) {
	buffer := make([]byte, 1024)
	//sum := 0
	//for i := 0; i <= 100; i++ {
	n, err := conn.Read(buffer)
	if err == nil {
		fmt.Println("read message from server:" + string(buffer[:n]))
		fmt.Println("Message len:", n)
	}
	//sum += i
	time.Sleep(1* time.Second)
    //}
}
*/
