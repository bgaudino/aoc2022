package solutions

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type Sensor struct {
	coordinates
	sweep int
}

type coordinatesSet map[coordinates]bool
type coordinatePairs map[coordinates]coordinates

const SEARCH_AREA_SIZE = 4000000

func manhattanDistance(c1 coordinates, c2 coordinates) int {
	x := math.Abs(float64(c1.x) - float64(c2.x))
	y := math.Abs(float64(c1.y) - float64(c2.y))
	return int(x + y)
}

func tuningFrequency(c coordinates) int {
	return (c.x * SEARCH_AREA_SIZE) + c.y
}

func isEmpty(sensor coordinates, position coordinates, sensors coordinatesSet, beacons coordinatesSet, pairs coordinatePairs) bool {
	if beacons[position] || sensors[position] {
		return false
	}
	if position.x < 0 || position.y < 0 || position.x > SEARCH_AREA_SIZE || position.y > SEARCH_AREA_SIZE {
		return false
	}
	for s := range sensors {
		sensorRange := manhattanDistance(s, pairs[s])
		distanceToSensor := manhattanDistance(s, position)
		if sensorRange >= distanceToSensor {
			return false
		}
	}
	return true
}

func Day15() {
	sensors, beacons, pairs := parse()
	targetRow := 2000000
	columnRanges := [][]int{}

	// Part 1
	for s, b := range pairs {
		distanceToBeacon := manhattanDistance(s, b)
		distanceToRow := manhattanDistance(s, coordinates{s.x, targetRow})
		if distanceToRow > distanceToBeacon {
			continue
		}
		offset := int(math.Abs(float64(s.y) - float64(targetRow)))
		columnRange := []int{s.x - distanceToBeacon + offset, s.x + distanceToBeacon - offset}
		columnRanges = append(columnRanges, columnRange)
	}

	eliminated := make(coordinatesSet)
	for _, cr := range columnRanges {
		for i := cr[0]; i <= cr[1]; i++ {
			c := coordinates{i, targetRow}
			if !beacons[c] && !sensors[c] {
				eliminated[c] = true
			}
		}
	}
	fmt.Println(len(eliminated))

	// Part 2
	signal := findSignal(sensors, beacons, pairs)
	if signal != nil {
		fmt.Println(tuningFrequency(*signal))
	}
}

func findSignal(sensors coordinatesSet, beacons coordinatesSet, pairs coordinatePairs) *coordinates {
	for sensor := range sensors {
		distance := manhattanDistance(sensor, pairs[sensor]) + 1
		for x := sensor.x + 1; x <= sensor.x+distance; x++ {
			offset := int(math.Abs(float64(x) - float64(sensor.x)))
			top := coordinates{x, sensor.y - distance + offset}
			bottom := coordinates{x, sensor.y + distance - offset}
			if isEmpty(sensor, top, sensors, beacons, pairs) {
				return &top
			}
			if isEmpty(sensor, bottom, sensors, beacons, pairs) {
				return &bottom
			}
		}
		for x := sensor.x - 1; x >= sensor.x-distance; x-- {
			offset := int(math.Abs(float64(x) - float64(sensor.x)))
			top := coordinates{x, sensor.y - distance + offset}
			bottom := coordinates{x, sensor.y + distance - offset}
			if isEmpty(sensor, top, sensors, beacons, pairs) {
				return &top
			}
			if isEmpty(sensor, bottom, sensors, beacons, pairs) {
				return &bottom
			}
		}
	}
	return nil
}

func parse() (coordinatesSet, coordinatesSet, coordinatePairs) {
	file, scanner := helpers.GetFile(15)
	defer file.Close()

	sensors := make(coordinatesSet)
	beacons := make(coordinatesSet)
	pairs := make(coordinatePairs)
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), " ")
		sensor := coordinates{
			x: parseCoordinate(parts[2]),
			y: parseCoordinate(parts[3]),
		}
		sensors[sensor] = true

		beacon := coordinates{
			x: parseCoordinate(parts[8]),
			y: parseCoordinate(parts[9]),
		}
		beacons[beacon] = true
		pairs[sensor] = beacon
	}
	return sensors, beacons, pairs
}

func parseCoordinate(s string) int {
	s = strings.Split(s, "=")[1]
	s = strings.Trim(s, ",: ")
	i, err := strconv.Atoi(s)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	return i
}
