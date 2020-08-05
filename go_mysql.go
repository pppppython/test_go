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

	//连接mysql数据库，使用testdb数据库
	db0, err = sql.Open("mysql", "root:123456@tcp(127.0.0.1:3306)/testdb?charset=utf8&parseTime=true&loc=Local")

	if err != nil {
		log.Fatal("数据库打开出现了问题：", err)
		return
	}

	//选择读取  db1  这个表
	rows, err := db0.Query("select * from db1")

	//获取 db1表  中的所有数据
	for rows.Next() {
		var id int
		var name string
		var salary string
		err = rows.Scan(&id, &name, &salary)
		checkErr(err)

		fmt.Println(id, name, salary)
	}
	//db0.Close()

	//	defer db0.Close()
	// 尝试与数据库建立连接（校验dsn是否正确）
	err = db0.Ping()
	if err != nil {
		log.Fatal("数据库连接出现了问题，llll：", err)
		return
	}
	/*
		//准备插入数据
		//使用DB结构体实例方法Prepare预处理插入,Prepare会返回一个stmt对象
		stmt, err := db0.Prepare("insert into `db1`(id,name,salary)values(?,?,?)")
		if err != nil {
			fmt.Println("预处理失败:", err)
			return
		}
		//使用Stmt对象执行预处理参数
		result, err := stmt.Exec(33, "pengjin", 12580) //这3个参数是即将插入表中的数据
		if err != nil {
			fmt.Println("执行预处理失败:", err)
			return
		} else {
			rows, _ := result.RowsAffected() //执行插入数据
			fmt.Println("执行成功,影响行数", rows, "行")
		}

	*/

	/*
		//准备删除数据
		//直接调用db实例中的Exec方法实现预处理
		result, err := db0.Exec("delete from `db1` where id=?", 90)
		if err != nil {
			fmt.Println("预处理失败:", err)
			return
		}

		if err != nil {
			fmt.Println("执行预处理失败:", err)
			return
		} else {
			rows, _ := result.RowsAffected()
			fmt.Println("执行成功,影响行数", rows, "行")
		}
	*/

	//准备更新数据
	//直接调用db实例中的Exec方法实现预处理
	result, err := db0.Exec("update `db1` set id=?,name=? where id=?", 34, "zhangsan", 90800)
	if err != nil {
		fmt.Println("预处理失败:", err)
		return
	}

	if err != nil {
		fmt.Println("执行预处理失败:", err)
		return
	} else {
		rows, _ := result.RowsAffected()
		fmt.Println("执行成功,影响行数", rows, "行")
	}

	//关闭数据库连接
	db0.Close()

}

//校验函数
func checkErr(err error) {
	if err != nil {
		log.Println(err)
	}
}
