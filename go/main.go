package main

import (
	"fmt"
	"os"
	"strconv"

	"main.go/go/solutions"
)

type solution func() (string, string)
type answer struct {
	part1 string
	part2 string
}
type day struct {
	solution solution
	answer   answer
}

var days = []day{
	{solutions.Day1, answer{"72070", "211805"}},
	{solutions.Day2, answer{"14297", "10498"}},
	{solutions.Day3, answer{"7826", "2577"}},
	{solutions.Day4, answer{"424", "804"}},
	{solutions.Day5, answer{"FJSRQCFTN", "CJVLJQPHS"}},
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
