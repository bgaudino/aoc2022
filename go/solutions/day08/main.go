package day08

import (
	"bufio"
	"strconv"

	"main.go/go/helpers"
)

type coordinates helpers.Coordinates

var north = coordinates{X: 0, Y: -1}
var south = coordinates{X: 0, Y: 1}
var east = coordinates{X: 1, Y: 0}
var west = coordinates{X: -1, Y: 0}

type tree struct {
	height int
	coordinates
}

func (t tree) isVisible(d coordinates, g [][]tree) (bool, int) {
	isVisible := true
	scenicScore := 0
	x, y := t.X, t.Y
	x += d.X
	y += d.Y
	for x >= 0 && x < len(g[0]) && y >= 0 && y < len(g) {
		scenicScore++
		neighbor := g[y][x]
		if t.height <= neighbor.height {
			isVisible = false
			break
		}
		x += d.X
		y += d.Y
	}
	return isVisible, scenicScore
}

type forest struct {
	grid [][]tree
}

func (f forest) createGrid(s *bufio.Scanner) [][]tree {
	grid := [][]tree{}
	y := 0
	for s.Scan() {
		row := []tree{}
		for x, c := range s.Text() {
			height, _ := strconv.Atoi(string(c))
			row = append(row, tree{height, coordinates{X: x, Y: y}})
		}
		grid = append(grid, row)
		y++
	}
	return grid
}

func (f forest) searchGrid() (string, string) {
	treesVisibleFromOutside := 0
	maxScenicScore := 0
	for _, row := range f.grid {
		for _, t := range row {
			northVisible, northCount := t.isVisible(north, f.grid)
			southVisible, southCount := t.isVisible(south, f.grid)
			eastVisible, eastCount := t.isVisible(east, f.grid)
			westVisible, westCount := t.isVisible(west, f.grid)

			if northVisible || southVisible || eastVisible || westVisible {
				treesVisibleFromOutside++
			}
			scenicScore := northCount * southCount * eastCount * westCount
			if scenicScore > maxScenicScore {
				maxScenicScore = scenicScore
			}
		}
	}
	return strconv.Itoa(treesVisibleFromOutside), strconv.Itoa(maxScenicScore)
}

func Solution() (string, string) {
	file, scanner := helpers.GetFile(8)
	defer file.Close()

	f := forest{}
	f.grid = f.createGrid(scanner)
	return f.searchGrid()
}

var Day = helpers.Day{Solution: Solution, Answer: helpers.Answer{Part1: "1700", Part2: "470596"}}
