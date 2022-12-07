package helpers

import (
	"bufio"
	"fmt"
	"os"
)

func GetFile(day int) (*os.File, *bufio.Scanner) {
	filename := fmt.Sprint("../data/day", day, ".txt")
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
