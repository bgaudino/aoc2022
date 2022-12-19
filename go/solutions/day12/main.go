package day12

import (
	"strconv"

	"main.go/go/helpers"
)

type coordinates helpers.Coordinates

func Solution() (string, string) {
	file, scanner := helpers.GetFile(12)
	defer file.Close()

	heightMap := [][]int{}
	var start coordinates
	var end coordinates
	y := 0
	for scanner.Scan() {
		row := []int{}
		for x, char := range scanner.Text() {
			elevation := int(char)
			if char == 'S' {
				start = coordinates{x, y}
				elevation = int('a')
			}
			if char == 'E' {
				end = coordinates{x, y}
				elevation = int('z')
			}
			row = append(row, elevation)
		}
		heightMap = append(heightMap, row)
		y++
	}

	steps := bfs(heightMap, start, end)

	var shortestPath int
	for i, s := range get_starting_points(heightMap) {
		path := bfs(heightMap, s, end)
		if path != -1 && (path < shortestPath || i == 0) {
			shortestPath = path
		}
	}

	return strconv.Itoa(steps), strconv.Itoa(shortestPath)
}

type pointSteps struct {
	coordinates
	steps int
}

func get_edges(mp [][]int, from coordinates) (edges []coordinates) {
	directions := []coordinates{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
	for _, d := range directions {
		x, y := from.X+d.X, from.Y+d.Y
		if x < 0 || y < 0 || x >= len(mp[0]) || y >= len(mp) {
			continue
		}
		from_elevation, to_elevation := mp[from.Y][from.X], mp[y][x]
		if to_elevation <= from_elevation+1 {
			edges = append(edges, coordinates{x, y})
		}
	}
	return edges
}

func get_starting_points(mp [][]int) (points []coordinates) {
	for y, row := range mp {
		for x, p := range row {
			if p == int('a') {
				points = append(points, coordinates{x, y})
			}
		}
	}
	return points
}

func bfs(mp [][]int, start coordinates, end coordinates) int {
	visited := map[coordinates]bool{
		start: true,
	}
	queue := []pointSteps{{start, -1}}

	for len(queue) > 0 {
		current := queue[0]
		current.steps += 1

		if len(queue) > 1 {
			queue = queue[1:]
		} else {
			queue = []pointSteps{}
		}

		if current.coordinates == end {
			return current.steps
		}

		for _, edge := range get_edges(mp, current.coordinates) {
			if _, ok := visited[edge]; !ok {
				visited[edge] = true
				es := pointSteps{edge, current.steps}
				queue = append(queue, es)
			}
		}
	}
	return -1
}

var Day = helpers.Day{Solution: Solution, Answer: helpers.Answer{Part1: "412", Part2: "402"}}
