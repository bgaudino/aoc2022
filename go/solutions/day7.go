package solutions

import (
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type directory struct {
	name     string
	files    []int
	parent   *directory
	children []*directory
}

func (d directory) getSizes() (int, []int) {
	sizes := []int{}
	var getSize func(directory) int
	getSize = func(d directory) int {
		size := helpers.Sum(d.files)
		for _, c := range d.children {
			size += getSize(*c)
		}
		sizes = append(sizes, size)
		return size
	}
	size := getSize(d)
	return size, sizes
}

func Day7() (string, string) {
	file, scanner := helpers.GetFile(7)
	defer file.Close()

	root := directory{name: "/"}
	cursor := &root
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, " ")
		if parts[0] == "dir" {
			dir := directory{name: parts[1], parent: cursor}
			cursor.children = append(cursor.children, &dir)
			continue
		}
		if parts[0] != "$" {
			size, _ := strconv.Atoi(parts[0])
			cursor.files = append(cursor.files, size)
			continue
		}
		if parts[1] == "cd" {
			if parts[2] == "/" {
				cursor = &root
				continue
			}

			if parts[2] == ".." {
				cursor = cursor.parent
				continue
			}

			exists := false
			for _, dir := range cursor.children {
				if dir.name == parts[2] {
					cursor = dir
					exists = true
					break
				}
			}
			if !exists {
				dir := directory{name: parts[2], parent: cursor}
				cursor.children = append(cursor.children, &dir)
				cursor = &dir
			}
		}
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
