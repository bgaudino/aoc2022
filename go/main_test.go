package main

import (
	"testing"
)

func test(n int, d day, t *testing.T) {
	part1, part2 := d.solution()
	if part1 != d.answers[0] {
		t.Error("Day", n, "(part 1): Expected", d.answers[0], "got", part1)
	}
	if part2 != d.answers[1] {
		t.Error("Day", n, "(part 2): Expected", d.answers[1], "got", part2)
	}
}

func Test(t *testing.T) {
	for i, d := range days {
		test(i, d, t)
	}
}
