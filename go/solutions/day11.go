package solutions

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"

	"main.go/go/helpers"
)

type monkey struct {
	items           []int
	operation       func(int) int
	test            func(int) bool
	ifTrue          int
	ifFalse         int
	inspectionCount int
}

func (m *monkey) inspect() {
	m.items[0] = m.operation(m.items[0])
	m.inspectionCount++
}

func (m *monkey) getBored() {
	m.items[0] /= 3
}

func (m monkey) toMonkeyIndex() int {
	if m.test(m.items[0]) {
		return m.ifTrue
	}
	return m.ifFalse
}

func (m *monkey) throw() int {
	item := m.items[0]
	if len(m.items) < 2 {
		m.items = []int{}
	} else {
		m.items = m.items[1:]
	}
	return item
}

func (m *monkey) catch(item int) {
	m.items = append(m.items, item)
}

func Day11() {
	troop := getMonkeys()

	for i := 0; i < 20; i++ {
		completeRound(troop)
	}
	mostActive := mostActiveMonkeys(troop)
	fmt.Println(mostActive[0].inspectionCount * mostActive[1].inspectionCount)
}

func completeRound(troop []monkey) {
	for i := 0; i < len(troop); i++ {
		fromMonkey := &troop[i]
		for len(fromMonkey.items) > 0 {
			fromMonkey.inspect()
			fromMonkey.getBored()
			j := fromMonkey.toMonkeyIndex()
			toMonkey := &troop[j]
			item := fromMonkey.throw()
			toMonkey.catch(item)
		}
	}
}

func mostActiveMonkeys(troop []monkey) []monkey {
	sort.Slice(troop, func(i, j int) bool {
		return troop[i].inspectionCount > troop[j].inspectionCount
	})
	return troop[:2]
}

func getMonkeys() []monkey {
	file, scanner := helpers.GetFile(11)
	defer file.Close()

	troop := []monkey{}
	m := monkey{}
	for scanner.Scan() {
		line := strings.Trim(scanner.Text(), " ")
		parts := strings.Split(line, ":")
		switch parts[0] {
		case "Starting items":
			m.items = parseItems(parts[1])
		case "Operation":
			m.operation = parseOperation(parts[1])
		case "Test":
			m.test = parseTest(parts[1])
		case "If true":
			m.ifTrue = parseCondition(parts[1])
		case "If false":
			m.ifFalse = parseCondition(parts[1])
			troop = append(troop, m)
			m = monkey{}
		default:
			continue
		}
	}
	return troop
}

func parseItems(itemStr string) []int {
	itemSlice := strings.Split(strings.Trim(itemStr, ""), ",")
	items := []int{}
	for _, is := range itemSlice {
		item, err := strconv.Atoi(strings.Trim(is, " "))
		if err != nil {
			fmt.Printf("Could not parse items")
			os.Exit(1)
		}
		items = append(items, item)
	}
	return items
}

func parseOperation(operStr string) (o func(int) int) {
	parts := strings.Split(operStr, " ")
	value := parts[len(parts)-1]
	var intVal int
	if value != "old" {
		converted, err := strconv.Atoi(parts[len(parts)-1])
		if err != nil {
			fmt.Println("Could not convert value to int:", value)
			os.Exit(1)
		}
		intVal = converted
	}
	operator := parts[len(parts)-2]

	switch operator {
	case "+":
		return func(old int) int {
			if value == "old" {
				return old + old
			}
			return old + intVal
		}
	case "*":
		return func(old int) int {
			if value == "old" {
				return old * old
			}
			return old * intVal
		}
	default:
		fmt.Println("Unexpected operator:", operator)
		os.Exit(1)
	}
	return
}

func parseTest(testString string) func(int) bool {
	parts := strings.Split(testString, " ")
	value, err := strconv.Atoi(parts[len(parts)-1])
	if err != nil {
		fmt.Println("Could not convert test value to int:", value)
		os.Exit(1)
	}
	return func(old int) bool { return old%value == 0 }
}

func parseCondition(conditionString string) int {
	parts := strings.Split(conditionString, " ")
	value, err := strconv.Atoi(parts[len(parts)-1])
	if err != nil {
		fmt.Println("Could not convert monkey value to int:", value)
		os.Exit(1)
	}
	return value
}
