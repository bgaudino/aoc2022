package main

import (
	"strconv"
	"strings"

	"main.go/go/helpers"
)

var rock, paper, scissors = 1, 2, 3
var loss, draw, win = 0, 3, 6

var elfCodes = map[string]int{"A": rock, "B": paper, "C": scissors}
var myCodes = map[string]int{"X": rock, "Y": paper, "Z": scissors}
var outcomeCodes = map[string]int{"X": loss, "Y": draw, "Z": win}

func day2() (string, string) {
	file, scanner := helpers.GetFile(2)
	defer file.Close()

	p1, p2 := 0, 0
	for scanner.Scan() {
		codes := strings.Split(scanner.Text(), " ")

		elf, me := elfCodes[codes[0]], myCodes[codes[1]]
		p1 += me + getOutcomePoints(elf, me)

		outcome := outcomeCodes[codes[1]]
		p2 += outcome + getShapePointsByOutcome(elf, outcome)
	}

	return strconv.Itoa(p1), strconv.Itoa(p2)
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
