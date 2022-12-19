package main

import (
	"fmt"
	"os"
	"strconv"

	"main.go/go/helpers"
	"main.go/go/solutions/day01"
	"main.go/go/solutions/day02"
	"main.go/go/solutions/day03"
	"main.go/go/solutions/day04"
	"main.go/go/solutions/day05"
	"main.go/go/solutions/day06"
	"main.go/go/solutions/day07"
	"main.go/go/solutions/day08"
	"main.go/go/solutions/day09"
	"main.go/go/solutions/day10"
	"main.go/go/solutions/day11"
	"main.go/go/solutions/day12"
	"main.go/go/solutions/day15"
)

var Days = []helpers.Day{
	day01.Day,
	day02.Day,
	day03.Day,
	day04.Day,
	day05.Day,
	day06.Day,
	day07.Day,
	day08.Day,
	day09.Day,
	day10.Day,
	day11.Day,
	day12.Day,
	day15.Day,
}

func main() {
	args := os.Args
	if len(args) > 1 {
		n, _ := strconv.Atoi(args[1])
		run(n, Days[n-1])
		return
	}
	for i, d := range Days {
		run(i+1, d)
	}
}

func run(n int, d helpers.Day) {
	s := d.Solution
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
