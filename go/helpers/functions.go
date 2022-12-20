package helpers

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func GetFile(day int) (*os.File, *bufio.Scanner) {
	dayString := strconv.Itoa(day)
	if day < 10 {
		dayString = "0" + dayString
	}
	filename := fmt.Sprint("../data/day", dayString, ".txt")
	file, _ := os.Open(filename)
	return file, bufio.NewScanner(file)
}

func Sum(nums []int) int {
	s := 0
	for _, n := range nums {
		s += n
	}
	return s
}

func Min(nums []int) int {
	m := nums[0]
	for _, n := range nums {
		if n < m {
			m = n
		}
	}
	return m
}
func Max(nums []int) int {
	m := nums[0]
	for _, n := range nums {
		if n > m {
			m = n
		}
	}
	return m
}
