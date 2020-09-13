package main

import (
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

func main() {
	http.HandleFunc("/", saye)               //设置访问的路由
	http.HandleFunc("/xx", sayhelloName)     //设置访问的路由
	err := http.ListenAndServe(":8000", nil) //设置监听的端口
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
	time.Sleep(5 * time.Second)
}

func saye(w http.ResponseWriter, r *http.Request) {
	f, err := os.Open("greet.html")
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
