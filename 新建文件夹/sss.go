package main

import (
	"bytes"
	"fmt"
	"log"
	"net"
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

var b bytes.Buffer //创建一个公共缓存区域

var (
	upgrader = websocket.Upgrader{
		// 读取存储空间大小
		ReadBufferSize: 1024,
		// 写入存储空间大小
		WriteBufferSize: 1024,
		// 允许跨域
		CheckOrigin: func(r *http.Request) bool {
			return true
		},
	}
)

type PreparedMessage struct {
}

func wsHandler(w http.ResponseWriter, r *http.Request) {
	var (
		wbsCon *websocket.Conn
		err    error
		//data   []byte
	)
	// 完成http应答，在httpheader中放下如下参数
	if wbsCon, err = upgrader.Upgrade(w, r, nil); err != nil {

		return // 获取连接失败直接返回
	}

	for {

		time.Sleep(1 * time.Second)

		c := make([]byte, 200)
		b.Read(c) //把公共缓存区域的数据写到c缓存区
		wbsCon.WriteMessage(websocket.TextMessage, c)

		if err := wbsCon.WriteMessage(websocket.TextMessage, c); err != nil {

			fmt.Println("推送失败")
			wbsCon.Close()
			break
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
	buffer := make([]byte, 4096)

	for {
		time.Sleep(1 * time.Second)
		b.Reset() //清空b缓存区域
		n, _ := conn.Read(buffer)
		kk := string(buffer[:n])
		b.WriteString(kk) //向b缓存区域写入数据
		fmt.Println("接收到的数据:" + string(buffer[:n]))

	}

}
func main() {
	go geet() //开启一个goroutine

	// 当有请求访问ws时，执行此回调方法
	http.HandleFunc("/ws", wsHandler)
	// 监听127.0.0.1:7777
	err := http.ListenAndServe("127.0.0.1:7777", nil)
	if err != nil {
		log.Fatal("ListenAndServe", err.Error())
	}
}
