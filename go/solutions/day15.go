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

func isEmpty(sensor coordinates, position coordinates, sensors coordinatesSet, beacons coordinatesSet, sensorBeaconPairs coordinatePairs) bool {
	if beacons[position] || sensors[position] {
		return false
	}
	for s := range sensors {
		sensorRange := manhattanDistance(s, sensorBeaconPairs[s])
		distanceToSensor := manhattanDistance(s, position)
		if sensorRange >= distanceToSensor {
			return false
		}
	}
	return true
}

func Day15() (string, string) {
	sensors, beacons, sensorBeaconPairs := parse()
	targetRow := 2000000
	columnRanges := make(map[yRange]bool)

	// Part 1
	currentRange := yRange{0, 0}
	for sensor, beacon := range sensorBeaconPairs {
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
			if !beacons[c] && !sensors[c] {
				eliminated[c] = true
			}
		}
	}
	numSquaresWithNoBeacon := len(eliminated)

	// Part 2
	signal := findSignal(sensors, beacons, sensorBeaconPairs)
	if signal == nil {
		fmt.Println("Oops")
		os.Exit(1)
	}
	frequency := tuningFrequency(*signal)

	return strconv.Itoa(numSquaresWithNoBeacon), strconv.Itoa(frequency)
}

func findSignal(sensors coordinatesSet, beacons coordinatesSet, sensorBeaconPairs coordinatePairs) *coordinates {
	for sensor := range sensors {
		distance := manhattanDistance(sensor, sensorBeaconPairs[sensor]) + 1
		start := sensor.x + 1
		if start < 0 {
			start = 0
		}
		end := sensor.x + distance
		if end > SEARCH_AREA_SIZE {
			end = SEARCH_AREA_SIZE
		}
		for x := sensor.x + 1; x <= sensor.x+distance; x++ {
			offset := int(math.Abs(float64(x) - float64(sensor.x)))
			top := coordinates{x, sensor.y - distance + offset}
			bottom := coordinates{x, sensor.y + distance - offset}
			if !isOutOfBounds(top) && isEmpty(sensor, top, sensors, beacons, sensorBeaconPairs) {
				return &top
			}
			if !isOutOfBounds(bottom) && isEmpty(sensor, bottom, sensors, beacons, sensorBeaconPairs) {
				return &bottom
			}

		}
		for x := sensor.x - 1; x >= sensor.x-distance; x-- {
			offset := int(math.Abs(float64(x) - float64(sensor.x)))
			top := coordinates{x, sensor.y - distance + offset}
			bottom := coordinates{x, sensor.y + distance - offset}
			if !isOutOfBounds(top) && isEmpty(sensor, top, sensors, beacons, sensorBeaconPairs) {
				return &top
			}
			if !isOutOfBounds(bottom) && isEmpty(sensor, bottom, sensors, beacons, sensorBeaconPairs) {
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
