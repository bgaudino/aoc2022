package day06

import (
	"strconv"

	"main.go/go/helpers"
)

type datastream struct {
	stream string
}

func (ds datastream) findMarker(n int) string {
	for i := 0; i < len(ds.stream)-n+1; i++ {
		if isUnique(ds.stream[i : i+n]) {
			return strconv.Itoa(i + n)
		}
	}
	return ""
}

func Solution() (string, string) {
	file, scanner := helpers.GetFile(6)
	defer file.Close()
	scanner.Scan()

	ds := datastream{scanner.Text()}
	return ds.findMarker(4), ds.findMarker(14)
}

func isUnique(s string) bool {
	result := make(map[rune]bool)
	for _, c := range s {
		if _, ok := result[c]; ok {
			return false
		}
		result[c] = true
	}
	return true
}

var Day = helpers.Day{Solution: Solution, Answer: helpers.Answer{Part1: "1912", Part2: "2122"}}
