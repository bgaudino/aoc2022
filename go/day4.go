package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type elfPair struct {
	a campSectionRange
	b campSectionRange
}

type campSectionRange struct {
	start int
	stop  int
}

func (e elfPair) fullyOverlaps() bool {
	for _, p := range []elfPair{e, e.opposite()} {
		if p.a.start <= p.b.start && p.a.stop >= p.b.stop {
			return true
		}
	}
	return false
}

func (e elfPair) partiallyOverlaps() bool {
	for _, p := range []elfPair{e, e.opposite()} {
		if (p.a.start <= p.b.start && p.a.stop >= p.b.start) || p.a.start <= p.b.stop && p.a.stop >= p.b.stop {
			return true
		}
	}
	return false
}

func (e elfPair) opposite() elfPair {
	return elfPair{e.b, e.a}
}

func main() {
	file, _ := os.Open("../data/day4.txt")
	scanner := bufio.NewScanner(file)

	fullOverlapCount := 0
	paritalOverlapCount := 0
	for scanner.Scan() {
		pair := getElfPair(strings.Split(scanner.Text(), ","))
		if pair.fullyOverlaps() {
			fullOverlapCount++
			paritalOverlapCount++
		} else if pair.partiallyOverlaps() {
			paritalOverlapCount++
		}
	}

	fmt.Println(fullOverlapCount)
	fmt.Println(paritalOverlapCount)
}

func getElfPair(s []string) elfPair {
	return elfPair{getCampSectionRange(s[0]), getCampSectionRange(s[1])}
}

func getCampSectionRange(s string) campSectionRange {
	strSlice := strings.Split(s, "-")
	r := []int{}
	for _, c := range strSlice {
		i, _ := strconv.Atoi(string(c))
		r = append(r, i)
	}
	return campSectionRange{r[0], r[1]}
}
