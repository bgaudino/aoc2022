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
	{solutions.Day6, answer{"1912", "2122"}},
	{solutions.Day7, answer{"1307902", "7068748"}},
	{solutions.Day8, answer{"1700", "470596"}},
	{solutions.Day9, answer{"6081", "2487"}},
	{solutions.Day10, answer{"13740", solutions.Day10part2Answer}},
}

func main() {
	args := os.Args
	if len(args) > 1 {
		n, _ := strconv.Atoi(args[1])
		run(n, days[n-1])
		return
	}
	for i, d := range days {
		run(i+1, d)
	}
	solutions.Day9()
}

func run(n int, d day) {
	s := d.solution
	p1, p2 := s()
	fmt.Println("--Day", n, "--")
	fmt.Println()
	fmt.Println("Part 1")
	fmt.Println("------")
	fmt.Println(p1)
	fmt.Println()
	fmt.Println("Part 2")
	fmt.Println("------")
	fmt.Println(p2)
	fmt.Println()
	fmt.Println()
}
