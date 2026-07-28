package main

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

// ScanResult holds the outcome of a port scan for JSON output
type ScanResult struct {
	Target string `json:"target"`
	Port   int    `json:"port"`
	Open   bool   `json:"open"`
	Banner string `json:"banner,omitempty"`
}

// scanPort attempts a TCP connection to the target host and port
func scanPort(host string, port int, timeout time.Duration, wg *sync.WaitGroup, results chan<- ScanResult) {
	defer wg.Done()

	address := fmt.Sprintf("%s:%d", host, port)
	conn, err := net.DialTimeout("tcp", address, timeout)
	if err != nil {
		results <- ScanResult{
			Target: host,
			Port:   port,
			Open:   false,
		}
		return
	}
	defer conn.Close()

	// Read banner if available
	conn.SetReadDeadline(time.Now().Add(1 * time.Second))
	buffer := make([]byte, 256)
	n, _ := conn.Read(buffer)
	banner := string(buffer[:n])

	results <- ScanResult{
		Target: host,
		Port:   port,
		Open:   true,
		Banner: banner,
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: recon <target_host>")
		os.Exit(1)
	}

	targetHost := os.Args[1]
	timeout := 1500 * time.Millisecond
	commonPorts := []int{21, 22, 25, 53, 80, 110, 143, 443, 445, 8080, 8443}

	var wg sync.WaitGroup
	results := make(chan ScanResult, len(commonPorts))

	for _, port := range commonPorts {
		wg.Add(1)
		go scanPort(targetHost, port, timeout, &wg, results)
	}

	// Wait for scans in background and close channel
	go func() {
		wg.Wait()
		close(results)
	}()

	openPorts := []ScanResult{}
	for res := range results {
		if res.Open {
			openPorts = append(openPorts, res)
		}
	}

	// Output clean JSON format expected by Python tests and plugins
	outputJSON, err := json.MarshalIndent(openPorts, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error marshaling JSON: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(string(outputJSON))
}
