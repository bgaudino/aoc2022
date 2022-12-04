package main

import (
	"sort"
	"strconv"

	"main.go/go/helpers"
)

func day1() (int, int) {
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

	return calorieTotals[0], helpers.Sum(calorieTotals[:3])
}
