package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

var mutex sync.Mutex
var clients = make(map[*websocket.Conn]bool) // 连接的客户端，是一个集合
var broadcast = make(chan string)            // 广播通道
var a string
var rr = make([]byte, 1) //定义切片，保存前端传来的控制信息,长度为1，容量为1

var ch2 = make(chan []byte)

var b int                  //用于存储待接收字节的长度,给x切片赋值
var x = make([]int, 5, 10) //直接定义切片，存储待接收字节的长度
var c int                  //用于存储待接收字节的长度,从x切片获取

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

func cs(w http.ResponseWriter, r *http.Request) {

	if r.Method == "GET" && len(r.FormValue("firstname")) > 0 {

		b, _ := strconv.Atoi(r.FormValue("firstname"))
		x[1] = b

	}
	f, err := os.Open("cs.html")
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()
	io.Copy(w, f)
}

func qx(w http.ResponseWriter, r *http.Request) {
	f, err := os.Open("qx.html")
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()
	io.Copy(w, f)
}

//主线程
func main() {

	go geet() //开启一个goroutine，连接TCP服务器

	// 配置websocket路由
	http.HandleFunc("/ws", handleConnections)

	// 获取消息，并发送到每一个客户端
	go handleMessages()

	http.HandleFunc("/", saye)           //主界面路由
	http.HandleFunc("/cs", cs)           //参数界面路由
	http.HandleFunc("/xx", sayhelloName) //流程界面路由
	http.HandleFunc("/qx", qx)           //曲线界面路由

	//err := http.ListenAndServe("192.168.1.9:8000", nil) //设置监听的端口
	err := http.ListenAndServe("0.0.0.0:8000", nil) //设置监听的端口
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
		time.Sleep(time.Duration(1000) * time.Millisecond)
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

	//serverAddr := "192.168.0.3:5000"
	serverAddr := "0.0.0.0:5000"
	tcpAddr, err := net.ResolveTCPAddr("tcp", serverAddr)
	if err != nil {
		fmt.Println("Resolve TCPAddr error", err)
	}
	conn, err := net.DialTCP("tcp4", nil, tcpAddr)

	//defer conn.Close()
	if err != nil {
		fmt.Println("连接tcp服务器出错", err)
	}

	go func() {
		for {
			time.Sleep(time.Duration(100) * time.Millisecond)
			pp := <-ch2 //pp是前端传过来的消息
			println(pp)
			//conn.Write(pp) //向tcp服务器发送数据
			conn.Write(pp)
		}
	}()
	//c := <-ch3

	buffer := make([]byte, 1000)

	for {

		time.Sleep(time.Duration(1000) * time.Millisecond) //延时100毫秒

		c := x[1]
		conn.Read(buffer) //读取TCP发来的数据
		println(c)

		kk := string(buffer[:c])
		println(kk)

		println("接收的字节长度:" + strconv.Itoa(c))

		// 将新接收到的消息发送到广播频道
		broadcast <- kk

	}

}
