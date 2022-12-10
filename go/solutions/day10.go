package solutions

import (
	"fmt"
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type crt struct {
	cycle                int
	register             int
	image                [][]string
	sumOfSignalStrengths int
}

func (c *crt) performCycle() {
	if c.cycle%40 == 20 {
		c.sumOfSignalStrengths += c.signalStrength()
	}
	c.cycle++
	c.draw()
}

func (c *crt) draw() {
	pixel := "."
	if c.spriteVisible() {
		pixel = "#"
	}
	if len(c.image) == 0 || len(*c.lastRow()) == 40 {
		c.image = append(c.image, []string{pixel})
	} else {
		*c.lastRow() = append(*c.lastRow(), pixel)
	}
}

func (c crt) lastRow() *[]string {
	return &c.image[len(c.image)-1]
}

func (c crt) spritePosition() map[int]bool {
	middle := c.register % 40
	return map[int]bool{
		middle - 1: true, middle: true, middle + 1: true,
	}
}

func (c crt) spriteVisible() bool {
	sp := c.spritePosition()
	if len(c.image) == 0 {
		return sp[0]
	}
	lr := len(*c.lastRow())
	return sp[lr] || (sp[0] && lr == 40)
}

func (c crt) signalStrength() int {
	return c.cycle * c.register
}

func (c crt) print() {
	for _, row := range c.image {
		fmt.Println(strings.Join(row, ""))
	}
}

func (c crt) toString() string {
	rows := []string{}
	for _, row := range c.image {
		rows = append(rows, strings.Join(row, ""))
	}
	return strings.Join(rows, "\n")
}

func parseInstruction(i string) (string, int) {
	parts := strings.Split(i, " ")
	operation := parts[0]
	if operation == "noop" {
		return operation, 0
	}
	value, _ := strconv.Atoi(parts[1])
	return operation, value
}

func Day10() (string, string) {
	file, scanner := helpers.GetFile(10)
	defer file.Close()

	c := crt{cycle: 1, register: 1}
	for scanner.Scan() {
		c.performCycle()

		operation, value := parseInstruction(scanner.Text())
		if operation == "addx" {
			c.performCycle()
			c.register += value
		}
	}
	return strconv.Itoa(c.sumOfSignalStrengths), c.toString()
}

var Day10part2Answer = `####.#..#.###..###..####.####..##..#....
...#.#..#.#..#.#..#.#....#....#..#.#....
..#..#..#.#..#.#..#.###..###..#....#....
.#...#..#.###..###..#....#....#....#....
#....#..#.#....#.#..#....#....#..#.#....
####..##..#....#..#.#....####..##..####.`
