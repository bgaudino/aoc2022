package main

import (
	"fmt"
	"testing"
)

func test(n int, d day, t *testing.T) {
	part1, part2 := d.solution()
	if part1 != d.answer.part1 {
		t.Error("Day", n, "(part 1): Expected", d.answer.part1, "got", part1)
	}
	if part2 != d.answer.part2 {
		t.Error("Day", n, "(part 2): Expected", d.answer.part2, "got", part2)
	}
	fmt.Println("Day", n, ": OK")
}

func Test(t *testing.T) {
	for i, d := range days {
		test(i, d, t)
	}
}
