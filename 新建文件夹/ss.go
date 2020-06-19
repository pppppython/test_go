package main

import (
	"bytes"
	"errors"
	"fmt"
	"net"
	"net/http"
	"runtime"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

///////////////////////////////////////////////////////
// 大家有代码和工作上的疑难问题，可以加老师的微信交流：120848369
///////////////////////////////////////////////////////

//var ch = make(chan byte)
var b bytes.Buffer //创建一个公共缓存区域

// http升级websocket协议的配置
var wsUpgrader = websocket.Upgrader{
	// 允许所有CORS跨域请求
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

// 客户端读写消息
type wsMessage struct {
	messageType int
	data        []byte
}

// 客户端连接
type wsConnection struct {
	wsSocket *websocket.Conn // 底层websocket
	inChan   chan *wsMessage // 读队列
	outChan  chan *wsMessage // 写队列

	mutex     sync.Mutex // 避免重复关闭管道
	isClosed  bool
	closeChan chan byte // 关闭通知
}

func (wsConn *wsConnection) wsReadLoop() {
	for {
		// 读一个message
		msgType, data, err := wsConn.wsSocket.ReadMessage()
		if err != nil {
			goto error
		}
		req := &wsMessage{
			msgType,
			data,
		}
		// 放入请求队列
		select {
		case wsConn.inChan <- req:
		case <-wsConn.closeChan:
			goto closed
		}
	}
error:
	wsConn.wsClose()
closed:
}

func (wsConn *wsConnection) wsWriteLoop() {
	for {
		select {
		// 取一个应答
		case msg := <-wsConn.outChan:
			// 写给websocket
			if err := wsConn.wsSocket.WriteMessage(msg.messageType, msg.data); err != nil {
				goto error
			}
		case <-wsConn.closeChan:
			goto closed
		}
	}
error:
	wsConn.wsClose()
closed:
}

func (wsConn *wsConnection) procLoop() {

	// 启动一个gouroutine发送心跳,这是一个匿名函数
	go func() {
		/*
			fmt.Println("连接tcp服务器")
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
			buffer := make([]byte, 4096)
		*/
		for {
			time.Sleep(1 * time.Second)
			//n, _ := conn.Read(buffer)
			//fmt.Println("接收到的数据:" + string(buffer[:n]))
			c := make([]byte, 200)
			b.Read(c) //把公共缓存区域的数据写到c缓存区
			wsConn.wsWrite(websocket.TextMessage, c)
			//runtime.Goexit()

			if err := wsConn.wsWrite(websocket.TextMessage, c); err != nil {
				//if err := wsConn.wsWrite(websocket.TextMessage, []byte("heartbeat from server")); err != nil {
				fmt.Println("heartbeat fail")
				wsConn.wsClose()
				fmt.Println("h fail")
				runtime.Goexit()

				break
			}

		}
	}()

	// 这是一个同步处理模型（只是一个例子），如果希望并行处理可以每个请求一个gorutine，注意控制并发goroutine的数量!!!
	/*
		for {
			msg, err := wsConn.wsRead()
			if err != nil {
				fmt.Println("read fail")
				break
			}
			fmt.Println(string(msg.data))
			err = wsConn.wsWrite(msg.messageType, msg.data)
			if err != nil {
				fmt.Println("write fail")
				break
			}
		}
	*/
}

func wsHandler(resp http.ResponseWriter, req *http.Request) {
	// 应答客户端告知升级连接为websocket
	wsSocket, err := wsUpgrader.Upgrade(resp, req, nil)
	if err != nil {
		return
	}
	wsConn := &wsConnection{
		wsSocket:  wsSocket,
		inChan:    make(chan *wsMessage, 1000),
		outChan:   make(chan *wsMessage, 1000),
		closeChan: make(chan byte),
		isClosed:  false,
	}

	// 处理器
	go wsConn.procLoop()
	// 读协程
	go wsConn.wsReadLoop()
	// 写协程
	go wsConn.wsWriteLoop()
}

func (wsConn *wsConnection) wsWrite(messageType int, data []byte) error {
	select {
	case wsConn.outChan <- &wsMessage{messageType, data}:
	case <-wsConn.closeChan:
		return errors.New("websocket closed")
	}
	return nil
}

func (wsConn *wsConnection) wsRead() (*wsMessage, error) {
	select {
	case msg := <-wsConn.inChan:
		return msg, nil
	case <-wsConn.closeChan:
	}
	return nil, errors.New("websocket closed")
}

func (wsConn *wsConnection) wsClose() {
	wsConn.wsSocket.Close()

	wsConn.mutex.Lock()
	defer wsConn.mutex.Unlock()
	if !wsConn.isClosed {
		wsConn.isClosed = true
		close(wsConn.closeChan)
	}
}

func geet() {

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

	//连接TCP服务器在一个线程里面，向b缓存区域写入接收到的TCP数据
	//向前端页面推送消息在另一个goroutine里面，从b缓存区域获取数据，再推送

	go geet() //开启一个goroutine

	http.HandleFunc("/ws", wsHandler)
	http.ListenAndServe("0.0.0.0:7777", nil)
}
