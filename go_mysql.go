package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

var db0 *sql.DB

func main() {
	//parseTime:时间格式转换;
	// loc=Local解决数据库时间少8小时问题
	var err error
	//TODO 注意：一下语句不能使用：db0, err ：=  ;不然将db0当做临时变量来处理，不会对全局变量db0进行赋值。
	db0, err = sql.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/testdb?charset=utf8&parseTime=true&loc=Local")

	rows, err := db0.Query("select * from db1")

	for rows.Next() {
		var id int
		var name string
		var salary string
		err = rows.Scan(&id, &name, &salary)
		checkErr(err)

		fmt.Println(id, name, salary)
	}
	db0.Close()

	if err != nil {
		log.Fatal("数据库打开出现了问题：", err)
		return
	}
	//	defer db0.Close()
	// 尝试与数据库建立连接（校验dsn是否正确）
	err = db0.Ping()
	if err != nil {
		log.Fatal("数据库连接出现了问题：", err)
		return
	}
}

//校验函数
func checkErr(err error) {
	if err != nil {
		log.Println(err)
	}
}
