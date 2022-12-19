package day09

import (
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type coordinates helpers.Coordinates

type knot struct {
	coordinates
	next    *knot
	visited map[coordinates]bool
}

func (k knot) isTouching(h knot) bool {
	return !(k.X > h.X+1 || k.X < h.X-1 || k.Y > h.Y+1 || k.Y < h.Y-1)
}

func (k *knot) follow(h knot) {
	if k.isTouching(h) {
		return
	}
	if k.X != h.X {
		if k.X > h.X {
			k.X--
		} else {
			k.X++
		}
	}
	if k.Y != h.Y {
		if k.Y > h.Y {
			k.Y--
		} else {
			k.Y++
		}
	}
}

func Solution() (string, string) {
	file, scanner := helpers.GetFile(9)
	defer file.Close()

	instructions := []string{}
	for scanner.Scan() {
		instructions = append(instructions, scanner.Text())
	}
	part1 := move(instructions, 2)
	part2 := move(instructions, 10)
	return strconv.Itoa(part1), strconv.Itoa(part2)
}

func move(instructions []string, ropeLength int) int {
	head := knot{visited: make(map[coordinates]bool)}
	tail := &head
	for i := 1; i < ropeLength; i++ {
		tail.next = &knot{visited: make(map[coordinates]bool)}
		tail = tail.next
	}

	for _, instruction := range instructions {
		parts := strings.Split(instruction, " ")
		movement := parts[0]
		distance, _ := strconv.Atoi(string(parts[1]))

		for i := 0; i < distance; i++ {
			switch movement {
			case "U":
				head.Y++
			case "D":
				head.Y--
			case "L":
				head.X--
			case "R":
				head.X++
			}
			k := &head
			for k.next != nil {
				k.next.follow(*k)
				k = k.next
				tail.visited[tail.coordinates] = true
			}
		}
	}
	return len(tail.visited)
}

var Day = helpers.Day{Solution: Solution, Answer: helpers.Answer{Part1: "6081", Part2: "2487"}}
