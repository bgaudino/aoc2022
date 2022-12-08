package solutions

import (
	"strconv"

	"main.go/go/helpers"
)

func Day8() (string, string) {
	file, scanner := helpers.GetFile(8)
	defer file.Close()

	rows := []string{}
	for scanner.Scan() {
		rows = append(rows, scanner.Text())
	}

	onEdge := func(x, y int) bool {
		if x == 0 || y == 0 || x == len(rows[0])-1 || y == len(rows)-1 {
			return true
		}
		return false
	}

	searchX := func(height int, row string) (bool, int) {
		isVisible, count := true, 0
		for _, char := range row {
			count++
			neighbor, _ := strconv.Atoi(string(char))
			if height <= neighbor {
				isVisible = false
				break
			}
		}
		return isVisible, count
	}

	searchY := func(height int, x int, y int, north bool) (bool, int) {
		isVisible, count, start, stop := true, 0, y, len(rows)
		if north {
			stop = -1
		}
		for (north && start > stop) || (!north && start < stop) {
			count++
			neighbor, _ := strconv.Atoi(string(rows[start][x]))
			if height <= neighbor {
				isVisible = false
				break
			}
			if north {
				start--
			} else {
				start++
			}
		}
		return isVisible, count
	}

	maxTreeCount, numVisible := 0, 0
	for y, row := range rows {
		for x, h := range row {
			height, _ := strconv.Atoi(string(h))
			northVisible, northCount := searchY(height, x, y-1, true)
			southVisible, southCount := searchY(height, x, y+1, false)
			eastVisible, eastCount := searchX(height, row[x+1:])

			bs := []byte{}
			for i := x - 1; i >= 0; i-- {
				bs = append(bs, row[i])
			}
			westVisible, westCount := searchX(height, string(bs))

			count := northCount * southCount * eastCount * westCount
			if count > maxTreeCount {
				maxTreeCount = count
			}
			if onEdge(x, y) || northVisible || southVisible || eastVisible || westVisible {
				numVisible++
			}
		}
	}
	return strconv.Itoa(numVisible), strconv.Itoa(maxTreeCount)
}
