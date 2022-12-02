package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

var rock = 1
var paper = 2
var scissors = 3

var loss = 0
var draw = 3
var win = 6

var elfCodes = map[string]int{"A": rock, "B": paper, "C": scissors}
var myCodes = map[string]int{"X": rock, "Y": paper, "Z": scissors}
var outcomeCodes = map[string]int{"X": loss, "Y": draw, "Z": win}

var shapes = []int{1, 2, 3}

func main() {
	file, _ := os.Open("../data/day2.txt")
	scanner := bufio.NewScanner(file)

	partOnePoints := 0
	partTwoPoints := 0
	for scanner.Scan() {
		codes := strings.Split(scanner.Text(), " ")

		elf, me := elfCodes[codes[0]], myCodes[codes[1]]
		partOnePoints += me + getOutcomePoints(elf, me)

		outcome := outcomeCodes[codes[1]]
		partTwoPoints += outcome + getShapePointsByOutcome(elf, outcome)
	}

	fmt.Println(partOnePoints)
	fmt.Println(partTwoPoints)
}

func getOutcomePoints(s1 int, s2 int) int {
	if s1 == s2 {
		return draw
	}
	if s1%3+1 == s2 {
		return win
	}
	return loss
}

func getShapePointsByOutcome(s int, o int) int {
	if o == draw {
		return s
	}
	if o == win {
		return s%3 + 1
	}
	if s-1 == 0 {
		return 3
	}
	return s - 1
}
