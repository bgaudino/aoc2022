package solutions

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type coordinatesSet map[coordinates]bool
type coordinatePairs map[coordinates]coordinates
type yRange struct {
	start int
	stop  int
}

const SEARCH_AREA_SIZE = 4000000

func manhattanDistance(c1 coordinates, c2 coordinates) int {
	x := math.Abs(float64(c1.x) - float64(c2.x))
	y := math.Abs(float64(c1.y) - float64(c2.y))
	return int(x + y)
}

func tuningFrequency(c coordinates) int {
	return (c.x * SEARCH_AREA_SIZE) + c.y
}

func isOutOfBounds(c coordinates) bool {
	return c.x < 0 || c.y < 0 || c.x > SEARCH_AREA_SIZE || c.y > SEARCH_AREA_SIZE
}

func isEmpty(position coordinates, beacons coordinatesSet, sensorBeaconPairs coordinatePairs) bool {
	_, ok := sensorBeaconPairs[position]
	if beacons[position] || ok {
		return false
	}
	for sensor, beacon := range sensorBeaconPairs {
		sensorRange := manhattanDistance(sensor, beacon)
		distanceToSensor := manhattanDistance(sensor, position)
		if sensorRange >= distanceToSensor {
			return false
		}
	}
	return true
}

func Day15() (string, string) {
	sensors, beacons := parse()
	targetRow := 2000000
	columnRanges := make(map[yRange]bool)

	// Part 1
	currentRange := yRange{0, 0}
	for sensor, beacon := range sensors {
		distanceToBeacon := manhattanDistance(sensor, beacon)
		distanceToRow := manhattanDistance(sensor, coordinates{sensor.x, targetRow})
		if distanceToRow > distanceToBeacon {
			continue
		}
		offset := int(math.Abs(float64(sensor.y) - float64(targetRow)))
		columnRange := yRange{sensor.x - distanceToBeacon + offset, sensor.x + distanceToBeacon - offset}

		// Don't overlap
		if columnRange.start > currentRange.stop || columnRange.stop < currentRange.start {
			columnRanges[currentRange] = true
			currentRange = columnRange
			continue
		}

		// Extends right
		if columnRange.stop > currentRange.stop {
			currentRange.stop = columnRange.stop
		}

		// Extends left
		if columnRange.start < currentRange.start {
			currentRange.start = columnRange.start
		}
	}
	columnRanges[currentRange] = true

	eliminated := make(coordinatesSet)
	for cr := range columnRanges {
		for i := cr.start; i <= cr.stop; i++ {
			c := coordinates{i, targetRow}
			_, ok := sensors[c]
			if !beacons[c] && !ok {
				eliminated[c] = true
			}
		}
	}
	numSquaresWithNoBeacon := len(eliminated)

	// Part 2
	signal := findSignal(sensors, beacons)
	if signal == nil {
		fmt.Println("Oops")
		os.Exit(1)
	}
	frequency := tuningFrequency(*signal)

	return strconv.Itoa(numSquaresWithNoBeacon), strconv.Itoa(frequency)
}

func findSignal(sensors coordinatePairs, beacons coordinatesSet) *coordinates {
	for sensor, beacon := range sensors {
		distance := manhattanDistance(sensor, beacon) + 1
		for x := sensor.x - 1; x <= sensor.x+distance; x++ {
			offset := int(math.Abs(float64(x) - float64(sensor.x)))
			top := coordinates{x, sensor.y - distance + offset}
			bottom := coordinates{x, sensor.y + distance - offset}
			if !isOutOfBounds(top) && isEmpty(top, beacons, sensors) {
				return &top
			}
			if !isOutOfBounds(bottom) && isEmpty(bottom, beacons, sensors) {
				return &bottom
			}

		}
	}
	return nil
}

func parse() (coordinatePairs, coordinatesSet) {
	file, scanner := helpers.GetFile(15)
	defer file.Close()

	beacons := make(coordinatesSet)
	sensors := make(coordinatePairs)
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), " ")
		sensor := coordinates{
			x: parseCoordinate(parts[2]),
			y: parseCoordinate(parts[3]),
		}

		beacon := coordinates{
			x: parseCoordinate(parts[8]),
			y: parseCoordinate(parts[9]),
		}
		beacons[beacon] = true
		sensors[sensor] = beacon
	}
	return sensors, beacons
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
