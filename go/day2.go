package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type shape struct {
	name     string
	points   int
	beats    string
	beatenBy string
}

type outcome struct {
	name   string
	points int
}

var rock = shape{name: "rock", points: 1, beats: "scissors", beatenBy: "paper"}
var paper = shape{name: "paper", points: 2, beats: "rock", beatenBy: "scissors"}
var scissors = shape{name: "scissors", points: 3, beats: "paper", beatenBy: "rock"}

var elfShapes = map[string]shape{"A": rock, "B": paper, "C": scissors}
var myShapes = map[string]shape{"X": rock, "Y": paper, "Z": scissors}
var myOutcomes = map[string]outcome{"X": loss, "Y": draw, "Z": win}

var win = outcome{name: "win", points: 6}
var draw = outcome{name: "draw", points: 3}
var loss = outcome{name: "loss", points: 0}

func (s1 shape) getOutcomeFromOpponentShape(s2 shape) outcome {
	if s1.beats == s2.name {
		return win
	}
	if s1.name == s2.name {
		return draw
	}
	return loss
}

func (s shape) getShapeFromOpponentOutcome(o outcome) shape {
	shapes := map[string]shape{
		"rock":     rock,
		"paper":    paper,
		"scissors": scissors,
	}
	if o.name == "win" {
		return shapes[s.beatenBy]
	}
	if o.name == "loss" {
		return shapes[s.beats]
	}
	return shapes[s.name]
}

func main() {

	file, _ := os.Open("../data/day2.txt")
	scanner := bufio.NewScanner(file)

	partOnePoints := 0
	partTwoPoints := 0
	for scanner.Scan() {
		shapes := strings.Split(scanner.Text(), " ")

		// Part one
		elfShape, myShape := elfShapes[shapes[0]], myShapes[shapes[1]]
		myOutcome := myShape.getOutcomeFromOpponentShape(elfShape)
		partOnePoints += myShape.points + myOutcome.points

		// Part two
		myOutcome = myOutcomes[shapes[1]]
		myShape = elfShape.getShapeFromOpponentOutcome(myOutcome)
		partTwoPoints += myShape.points + myOutcome.points
	}

	fmt.Println(partOnePoints)
	fmt.Println(partTwoPoints)
}
