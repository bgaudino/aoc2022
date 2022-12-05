package main

import (
	"fmt"
	"os"
	"strconv"
)

type solution func() (int, int)
type answer struct {
	part1 int
	part2 int
}
type day struct {
	solution solution
	answer   answer
}

var days = []day{
	{day1, answer{72070, 211805}},
	{day2, answer{14297, 10498}},
	{day3, answer{7826, 2577}},
	{day4, answer{424, 804}},
}

func main() {
	args := os.Args
	if len(args) > 1 {
		n, _ := strconv.Atoi(args[1])
		fmt.Println(days[n-1].solution())
		return
	}
	for _, d := range days {
		fmt.Println(d.solution())
	}
}
