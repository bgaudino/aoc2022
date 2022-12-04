package main

import (
	"strconv"
	"strings"

	"main.go/go/helpers"
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

func day4() (p1, p2 int) {
	file, scanner := helpers.GetFile(4)
	defer file.Close()
	for scanner.Scan() {
		pair := getElfPair(strings.Split(scanner.Text(), ","))
		if pair.fullyOverlaps() {
			p1++
			p2++
		} else if pair.partiallyOverlaps() {
			p2++
		}
	}

	return p1, p2
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
