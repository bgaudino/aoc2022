package solutions

import (
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type position struct {
	x int
	y int
}

type knot struct {
	position
	next    *knot
	visited map[position]bool
}

func (k knot) isTouching(h knot) bool {
	return !(k.x > h.x+1 || k.x < h.x-1 || k.y > h.y+1 || k.y < h.y-1)
}

func (k *knot) follow(h knot) {
	if k.isTouching(h) {
		return
	}
	if k.x != h.x {
		if k.x > h.x {
			k.x--
		} else {
			k.x++
		}
	}
	if k.y != h.y {
		if k.y > h.y {
			k.y--
		} else {
			k.y++
		}
	}
}

func Day9() (string, string) {
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
	head := knot{visited: make(map[position]bool)}
	tail := &head
	for i := 1; i < ropeLength; i++ {
		tail.next = &knot{visited: make(map[position]bool)}
		tail = tail.next
	}

	for _, instruction := range instructions {
		parts := strings.Split(instruction, " ")
		movement := parts[0]
		distance, _ := strconv.Atoi(string(parts[1]))

		for i := 0; i < distance; i++ {
			switch movement {
			case "U":
				head.y++
			case "D":
				head.y--
			case "L":
				head.x--
			case "R":
				head.x++
			}
			k := &head
			for k.next != nil {
				k.next.follow(*k)
				k = k.next
				tail.visited[tail.position] = true
			}
		}
	}
	return len(tail.visited)
}
