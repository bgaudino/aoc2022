package solutions

import (
	"strconv"

	"main.go/go/helpers"
)

type point struct {
	x int
	y int
}

func Day12() (string, string) {
	file, scanner := helpers.GetFile(12)
	defer file.Close()

	heightMap := [][]int{}
	var start point
	var end point
	y := 0
	for scanner.Scan() {
		row := []int{}
		for x, char := range scanner.Text() {
			elevation := int(char)
			if char == 'S' {
				start = point{x, y}
				elevation = int('a')
			}
			if char == 'E' {
				end = point{x, y}
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
	point
	steps int
}

func get_edges(mp [][]int, from point) (edges []point) {
	directions := []point{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
	for _, d := range directions {
		x, y := from.x+d.x, from.y+d.y
		if x < 0 || y < 0 || x >= len(mp[0]) || y >= len(mp) {
			continue
		}
		from_elevation, to_elevation := mp[from.y][from.x], mp[y][x]
		if to_elevation <= from_elevation+1 {
			edges = append(edges, point{x, y})
		}
	}
	return edges
}

func get_starting_points(mp [][]int) (points []point) {
	for y, row := range mp {
		for x, p := range row {
			if p == int('a') {
				points = append(points, point{x, y})
			}
		}
	}
	return points
}

func bfs(mp [][]int, start point, end point) int {
	visited := map[point]bool{
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

		if current.point == end {
			return current.steps
		}

		for _, edge := range get_edges(mp, current.point) {
			if _, ok := visited[edge]; !ok {
				visited[edge] = true
				es := pointSteps{edge, current.steps}
				queue = append(queue, es)
			}
		}
	}
	return -1
}
