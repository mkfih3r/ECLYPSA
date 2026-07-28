package main

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

type ScanResult struct {
	Target string `json:"target"`
	Port   int    `json:"port"`
	Open   bool   `json:"open"`
}

func scanPort(target str, port int, wg *sync.WaitGroup, results chan<- ScanResult) {
	defer wg.Done()
	address := fmt.Sprintf("%s:%d", target, port)
	conn, err := net.DialTimeout("tcp", address, 1500*time.Millisecond)

	if err != nil {
		results <- ScanResult{Target: target, Port: port, Open: false}
		return
	}
	conn.Close()
	results <- ScanResult{Target: target, Port: port, Open: true}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println(`{"error": "Target host argument required"}`)
		os.Exit(1)
	}

	target := os.Args[1]
	ports := []int{21, 22, 80, 443, 8080, 8443, 3306, 5432}

	var wg sync.WaitGroup
	resultsChan := make(chan ScanResult, len(ports))

	for _, port := range ports {
		wg.Add(1)
		go scanPort(target, port, &wg, resultsChan)
	}

	wg.Wait()
	close(resultsChan)

	var openPorts []ScanResult
	for res := range resultsChan {
		if res.Open {
			openPorts = append(openPorts, res)
		}
	}

	output, _ := json.Marshal(openPorts)
	fmt.Println(string(output))
}