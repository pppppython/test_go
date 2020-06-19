package main

import (
	"fmt"
	"strconv"
)

func main() {
	/*****Format系列******/
	// bool转字符串
	fmt.Println(strconv.FormatBool(true))
	//'f'指打印格式以小数方式，3：指小数位数， 64：指float64处理
	fmt.Println(strconv.FormatFloat(2.12, 'f', 3, 64))
	//整数转字符串
	fmt.Println(strconv.Itoa(19))

	/*****Parse系列******/
	//字符串转bool
	flag, _ := strconv.ParseBool("true")
	fmt.Println(flag)
	//字符串转浮点
	float, _ := strconv.ParseFloat("3.14", 64)
	fmt.Println(float)
	//字符串转整型
	i, _ := strconv.Atoi("123")
	fmt.Println(i)

	/*****Append系列******/
	slice := make([]byte, 0, 1024)
	slice = strconv.AppendBool(slice, true)
	// 10:指十进制
	slice = strconv.AppendInt(slice, 123, 10)
	slice = strconv.AppendFloat(slice, 3.14, 'f', 2, 64)
	slice = strconv.AppendQuote(slice, "hello go")
	fmt.Println(string(slice))
}
