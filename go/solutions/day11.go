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
	modulus         int
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

func (m monkey) test(item int) bool {
	return item%m.modulus == 0
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

func Day11() (string, string) {
	t1 := getTroop()
	for i := 0; i < 20; i++ {
		completeRound(t1, 1)
	}

	t2 := getTroop()
	for i := 0; i < 10000; i++ {
		completeRound(t2, 2)
	}

	p1, p2 := getMonkeyBusiness(t1), getMonkeyBusiness(t2)
	return strconv.Itoa(p1), strconv.Itoa((p2))
}

func completeRound(troop []monkey, part int) {
	for i := 0; i < len(troop); i++ {
		fromMonkey := &troop[i]
		for len(fromMonkey.items) > 0 {
			fromMonkey.inspect()
			if part == 1 {
				fromMonkey.getBored()
			} else if part == 2 {
				fromMonkey.items[0] = fromMonkey.items[0] % cycleLength(troop)
			} else {
				fmt.Println("Invalid argument. Part must be 1 or 2")
				os.Exit(1)
			}
			j := fromMonkey.toMonkeyIndex()
			toMonkey := &troop[j]
			item := fromMonkey.throw()
			toMonkey.catch(item)
		}
	}
}

func getMonkeyBusiness(troop []monkey) int {
	level := 1
	mostActive := mostActiveMonkeys(troop)
	for _, m := range mostActive {
		level *= m.inspectionCount
	}
	return level
}

func mostActiveMonkeys(troop []monkey) []monkey {
	sort.Slice(troop, func(i, j int) bool {
		return troop[i].inspectionCount > troop[j].inspectionCount
	})
	return troop[:2]
}

func cycleLength(troop []monkey) int {
	product := 1
	for _, m := range troop {

		product *= m.modulus
	}
	return product
}

func getTroop() []monkey {
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
			m.modulus = parseModulus(parts[1])
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

func parseModulus(testString string) int {
	parts := strings.Split(testString, " ")
	modulus, err := strconv.Atoi(parts[len(parts)-1])
	if err != nil {
		fmt.Println("Could not convert test value to int:", modulus)
		os.Exit(1)
	}
	return modulus
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
