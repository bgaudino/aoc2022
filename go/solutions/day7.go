package solutions

import (
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type directory struct {
	size     int
	parent   *directory
	children children
}
type children map[string]*directory

func (d directory) getSizes() (int, []int) {
	sizes := []int{}
	var getSize func(directory) int
	getSize = func(d directory) int {
		size := d.size
		for _, c := range d.children {
			size += getSize(*c)
		}
		sizes = append(sizes, size)
		return size
	}
	return getSize(d), sizes
}

func Day7() (string, string) {
	file, scanner := helpers.GetFile(7)
	defer file.Close()

	root := directory{children: make(children)}
	cursor := &root
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, " ")

		// directory
		if parts[0] == "dir" {
			dir := directory{parent: cursor, children: make(children)}
			cursor.children[parts[1]] = &dir
			continue
		}

		// file
		if parts[0] != "$" {
			size, _ := strconv.Atoi(parts[0])
			cursor.size += size
			continue
		}

		// ls
		if parts[1] == "ls" {
			continue
		}

		// cd
		pwd := parts[2]
		if pwd == "/" {
			cursor = &root
			continue
		}
		if pwd == ".." {
			cursor = cursor.parent
			continue
		}
		cursor = cursor.children[pwd]
	}
	totalSize, sizes := root.getSizes()
	availableSpace := 70000000 - totalSize
	spaceToFree := 30000000 - availableSpace

	p1 := 0
	p2 := -1
	for _, n := range sizes {
		if n <= 100000 {
			p1 += n
		}
		if n >= spaceToFree && (p2 == -1 || p2 > n) {
			p2 = n
		}
	}

	return strconv.Itoa(p1), strconv.Itoa(p2)
}
