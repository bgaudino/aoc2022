package solutions

import (
	"strconv"
	"strings"

	"main.go/go/helpers"
)

func Day5() (string, string) {
	diagram, instructions := parseInput()

	// Part 1
	stacks := fillStacks(diagram)
	rearrange(stacks, instructions, false)
	part1 := topOfEachStack(stacks)

	// Part 2
	stacks = fillStacks(diagram)
	rearrange(stacks, instructions, true)
	part2 := topOfEachStack(stacks)
	return part1, part2
}

func parseInput() ([]string, []string) {
	file, scanner := helpers.GetFile(5)
	defer file.Close()

	diagram := []string{}
	instructions := []string{}
	diagramComplete := false
	for scanner.Scan() {
		line := scanner.Text()
		if diagramComplete {
			instructions = append(instructions, line)
		} else if line == "" {
			diagramComplete = true
		} else {
			diagram = append([]string{line}, diagram...)
		}
	}
	return diagram, instructions
}

func fillStacks(diagram []string) map[string][]string {
	stacks := make(map[string][]string)
	for k, line := range diagram {
		i, j := 1, 1
		for i < len(line) {
			crate := string(line[i])
			if k == 0 {
				stacks[crate] = []string{}
			} else if crate != " " {
				key := strconv.Itoa(j)
				stacks[key] = append(stacks[key], crate)
			}
			i += 4
			j++
		}
	}
	return stacks
}

func rearrange(stacks map[string][]string, instructions []string, inBulk bool) {
	for _, instruction := range instructions {
		parts := strings.Fields(instruction)
		quantity, _ := strconv.Atoi(parts[1])
		from := parts[3]
		to := parts[5]
		to_stack := stacks[to]
		from_stack := stacks[from]
		if inBulk {
			index := len(from_stack) - quantity
			to_stack = append(to_stack, from_stack[index:]...)
			from_stack = from_stack[:index]
		} else {
			for i := 0; i < quantity; i++ {
				index := len(from_stack) - 1
				to_stack = append(to_stack, from_stack[index:]...)
				if len(from_stack) > 1 {
					from_stack = from_stack[:index]
				} else {
					from_stack = []string{}
				}
			}
		}
		stacks[from], stacks[to] = from_stack, to_stack
	}
}

func topOfEachStack(stacks map[string][]string) string {
	tops := []string{}
	for i := 1; i <= len(stacks); i++ {
		stack := stacks[strconv.Itoa(i)]
		if len(stack) > 0 {
			tops = append(tops, stack[len(stack)-1])
		}
	}
	return strings.Join(tops, "")
}
