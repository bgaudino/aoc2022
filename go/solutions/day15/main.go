package day15

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type coordinates helpers.Coordinates
type coordinatesSet map[coordinates]bool
type coordinatePairs map[coordinates]coordinates

const SEARCH_AREA_SIZE = 4000000

func manhattanDistance(c1 coordinates, c2 coordinates) int {
	x := math.Abs(float64(c1.X) - float64(c2.X))
	y := math.Abs(float64(c1.Y) - float64(c2.Y))
	return int(x + y)
}

func tuningFrequency(c coordinates) int {
	return (c.X * SEARCH_AREA_SIZE) + c.Y
}

func isOutOfBounds(c coordinates) bool {
	return c.X < 0 || c.Y < 0 || c.X > SEARCH_AREA_SIZE || c.Y > SEARCH_AREA_SIZE
}

func isEmpty(position coordinates, beacons coordinatesSet, sensors coordinatePairs) bool {
	_, ok := sensors[position]
	if beacons[position] || ok {
		return false
	}
	for sensor, beacon := range sensors {
		sensorRange := manhattanDistance(sensor, beacon)
		distanceToSensor := manhattanDistance(sensor, position)
		if sensorRange >= distanceToSensor {
			return false
		}
	}
	return true
}

func Solution() (string, string) {
	sensors, beacons := parse()
	targetRow := 2000000

	// Part 1
	sensorRange := make(map[int]bool)
	for sensor, beacon := range sensors {
		distanceToBeacon := manhattanDistance(sensor, beacon)
		distanceToRow := manhattanDistance(sensor, coordinates{sensor.X, targetRow})
		if distanceToRow > distanceToBeacon {
			continue
		}
		offset := int(math.Abs(float64(sensor.Y) - float64(targetRow)))
		for x := sensor.X - distanceToBeacon + offset; x < sensor.X+distanceToBeacon-offset; x++ {
			sensorRange[x] = true
		}
	}

	// Part 2
	signal := findSignal(sensors, beacons)
	if signal == nil {
		fmt.Println("Oops")
		os.Exit(1)
	}
	frequency := tuningFrequency(*signal)

	return strconv.Itoa(len(sensorRange)), strconv.Itoa(frequency)
}

func findSignal(sensors coordinatePairs, beacons coordinatesSet) *coordinates {
	for sensor, beacon := range sensors {
		distance := manhattanDistance(sensor, beacon) + 1
		for x := sensor.X - 1; x <= sensor.X+distance; x++ {
			offset := int(math.Abs(float64(x) - float64(sensor.X)))
			top := coordinates{x, sensor.Y - distance + offset}
			bottom := coordinates{x, sensor.Y + distance - offset}
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
			X: parseCoordinate(parts[2]),
			Y: parseCoordinate(parts[3]),
		}

		beacon := coordinates{
			X: parseCoordinate(parts[8]),
			Y: parseCoordinate(parts[9]),
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

var Day = helpers.Day{Solution: Solution, Answer: helpers.Answer{Part1: "4582667", Part2: "10961118625406"}}
