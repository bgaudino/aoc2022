package main

import (
	"fmt"
	"os"
	"strconv"
)

type solution func() (int, int)
type day struct {
	solution solution
	answers  []int
}

var days = []day{
	{day1, []int{72070, 211805}},
	{day2, []int{14297, 10498}},
	{day3, []int{7826, 2577}},
	{day4, []int{424, 804}},
}

func main() {
	args := os.Args
	n, _ := strconv.Atoi(args[1])
	fmt.Println(days[n-1].solution())
}
