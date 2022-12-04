package main

import (
	"main.go/go/helpers"
)

type item rune

func (i item) points() int {
	code := int(i)
	// lowercase
	if code >= 97 && code <= 122 {
		return code - 96
	}
	// uppercase
	if code >= 65 && code <= 90 {
		return code - 38
	}
	return 0
}

type rucksack map[item]bool

func (r rucksack) has(i item) bool {
	_, ok := r[i]
	return ok
}

func (r rucksack) add(i item) {
	r[i] = true
}

func (r rucksack) pop() (i item) {
	for it := range r {
		return it
	}
	return
}

func (r1 rucksack) intersection(r2 rucksack) rucksack {
	r3 := make(rucksack)
	for k := range r1 {
		if r2.has(k) {
			r3.add(k)
		}
	}
	return r3
}

type group []rucksack

func (g group) badge() item {
	rucksack := g[0]
	for i := 1; i < len(g); i++ {
		rucksack = rucksack.intersection(g[i])
	}
	return rucksack.pop()
}

func day3() (p1, p2 int) {
	file, scanner := helpers.GetFile(3)
	defer file.Close()

	g := group{}
	for scanner.Scan() {
		line := scanner.Text()
		r1, r2 := make(rucksack), make(rucksack)
		found := false
		m := len(line) / 2
		for i, c := range line {
			it := item(c)
			r2.add(it)
			if i < m {
				r1.add(it)
			} else if !found && r1.has(it) {
				found = true
				p1 += it.points()
			}
		}
		g = append(g, r2)
		if len(g) == 3 {
			p2 += g.badge().points()
			g = group{}
		}
	}

	return p1, p2
}
