package helpers

type Solution func() (string, string)

type Answer struct {
	Part1 string
	Part2 string
}

type Day struct {
	Solution
	Answer
}

type Coordinates struct {
	X int
	Y int
}
