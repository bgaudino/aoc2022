package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

func main() {
	file, _ := os.Open("../data/day1.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)

	calorieTotals := []int{}
	elfItemCalories := []int{}
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			calorieTotals = append(calorieTotals, sum(elfItemCalories))
			elfItemCalories = []int{}
			continue
		}
		itemCalories, _ := strconv.Atoi(line)
		elfItemCalories = append(elfItemCalories, itemCalories)
	}

	sort.Slice(calorieTotals, func(i, j int) bool {
		return calorieTotals[i] > calorieTotals[j]
	})

	// Part one
	fmt.Println(calorieTotals[0])

	// Part two
	fmt.Println(sum(calorieTotals[:3]))
}

func sum(nums []int) int {
	s := 0
	for _, n := range nums {
		s += n
	}
	return s
}
