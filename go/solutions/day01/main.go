package day01

import (
	"sort"
	"strconv"

	"main.go/go/helpers"
)

func Solution() (string, string) {
	calorieTotals := []int{}
	elfItemCalories := []int{}
	file, scanner := helpers.GetFile(1)
	defer file.Close()

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			calorieTotals = append(calorieTotals, helpers.Sum(elfItemCalories))
			elfItemCalories = []int{}
			continue
		}
		itemCalories, _ := strconv.Atoi(line)
		elfItemCalories = append(elfItemCalories, itemCalories)
	}

	sort.Slice(calorieTotals, func(i, j int) bool {
		return calorieTotals[i] > calorieTotals[j]
	})

	p1, p2 := strconv.Itoa(calorieTotals[0]), strconv.Itoa(helpers.Sum(calorieTotals[:3]))
	return p1, p2
}

var Day = helpers.Day{Solution: Solution, Answer: helpers.Answer{Part1: "72070", Part2: "211805"}}
