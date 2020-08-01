package main

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"time"
	"os"
	"io"
	"github.com/gorilla/websocket"
)

var clients = make(map[*websocket.Conn]bool) // 连接的客户端，是一个集合
var broadcast = make(chan string)            // 广播通道
var a string
var rr = make([]byte, 1) //定义切片，保存前端传来的控制信息,长度为1，容量为1

var ch2 = make(chan []byte)

// 配置升级http协议
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}



func saye(w http.ResponseWriter, r *http.Request) {
	f, err := os.Open("mains.html")
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()
	io.Copy(w, f)
}

func sayhelloName(w http.ResponseWriter, r *http.Request) {
	f, err := os.Open("h.html")
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()
	io.Copy(w, f)
}





//主线程
func main() {

	go geet() //开启一个goroutine，连接TCP服务器
	
	// Create a simple file server
	//fs := http.FileServer(http.Dir("../public"))
	//http.Handle("/", fs)

	// 配置websocket路由
	http.HandleFunc("/ws", handleConnections)
	
	// 获取消息，并发送到每一个客户端
	go handleMessages()

	http.HandleFunc("/", saye)               //设置访问的路由
	http.HandleFunc("/xx", sayhelloName)     //设置访问的路由
	err := http.ListenAndServe("192.168.1.5:8000", nil) //设置监听的端口
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
	
}

func handleConnections(w http.ResponseWriter, r *http.Request) {
	println("kkkkkk")
	//升级初始的GET请求到一个websocket
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Fatal(err)
	}
	// 确保在函数返回时关闭连接
	//defer ws.Close()

	// 注册新客户端
	clients[ws] = true

	//循环读取当前客户端传来的控制信息
	for {
		
		//接收每个客户端发回来的消息

		_, rr, err := ws.ReadMessage()
		//ss := string(rr[0])
		//fmt.Println(ss)
		ch2 <- rr //将前端传来的消息传入ch2通道
		//ss[0:0]
		if err != nil {
			log.Printf("error: %v", err)
			delete(clients, ws)
			break
		}

	}
}

func handleMessages() {
	for {
		time.Sleep(time.Duration(100) * time.Millisecond)
		// 从广播频道获取下一条消息
		msg := <-broadcast
		//将其发送到当前连接的每个客户端
		for client := range clients {
			err := client.WriteJSON(msg)
			if err != nil {
				//log.Printf("error: %v", err)
				client.Close()

				delete(clients, client)
			}
		}
	}
}

//TCP连接函数
func geet() {

	serverAddr := "127.0.0.1:8000"
	tcpAddr, err := net.ResolveTCPAddr("tcp", serverAddr)
	if err != nil {
		fmt.Println("Resolve TCPAddr error", err)
	}
	conn, err := net.DialTCP("tcp4", nil, tcpAddr)

	defer conn.Close()
	if err != nil {
		fmt.Println("连接tcp服务器出错", err)
	}

	go func() {
		for {
			time.Sleep(time.Duration(100) * time.Millisecond)
			pp := <-ch2
			//pk := string(pp[:49])
			//fmt.Println(pk)
			conn.Write(pp) //向tcp服务器发送数据
		}
	}()

	buffer := make([]byte, 62)

	for {
		//time.Sleep(1 * time.Second)
		time.Sleep(time.Duration(100) * time.Millisecond)

		conn.Read(buffer) //读取TCP发来的数据

		kk := string(buffer[:62])
		//fmt.Println(len(kk))
		// 将新接收到的消息发送到广播频道
		broadcast <- kk

	}

}