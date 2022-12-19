package main

import (
	"fmt"
	"testing"

	"main.go/go/helpers"
)

func test(n int, d helpers.Day, t *testing.T) {
	part1, part2 := d.Solution()
	if part1 != d.Answer.Part1 {
		t.Error("Day", n+1, "(part 1): Expected", d.Answer.Part1, "got", part1)
	}
	if part2 != d.Answer.Part2 {
		t.Error("Day", n+1, "(part 2): Expected", d.Answer.Part2, "got", part2)
	}
	fmt.Println("Day", n+1, ": OK")
}

func Test(t *testing.T) {
	for i, d := range Days {
		test(i, d, t)
	}
}
