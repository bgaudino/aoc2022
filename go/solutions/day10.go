package solutions

import (
	"fmt"
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type signal struct {
	cycle    int
	register int
}

func (s signal) strength() int {
	return s.cycle * s.register
}

func Day10() (string, string) {
	file, scanner := helpers.GetFile(10)
	defer file.Close()

	cycle := 1
	register := 1
	interestingSignals := []signal{}
	sumOfStrengths := 0
	checkSignal := func() {
		if cycle%40 == 20 {
			s := signal{cycle, register}
			interestingSignals = append(interestingSignals, s)
			sumOfStrengths += s.strength()
		}
	}
	for scanner.Scan() {
		checkSignal()
		parts := strings.Split(scanner.Text(), " ")
		operation := parts[0]
		cycle++
		if operation == "addx" {
			checkSignal()
			cycle++
			value, _ := strconv.Atoi(parts[1])
			register += value
		}
	}
	fmt.Println(interestingSignals)
	fmt.Println(sumOfStrengths)

	return "", ""
}
