package main

import (
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

// ScanResult holds the outcome of a port scan and banner grab
type ScanResult struct {
	Port   int
	IsOpen bool
	Banner string
}

// scanPort attempts a TCP connection to the target host and port
func scanPort(host string, port int, timeout time.Duration, wg *sync.WaitGroup, results chan<- ScanResult) {
	defer wg.Done()

	address := fmt.Sprintf("%s:%d", host, port)
	conn, err := net.DialTimeout("tcp", address, timeout)
	if err != nil {
		results <- ScanResult{Port: port, IsOpen: false}
		return
	}
	defer conn.Close()

	// Set a short read deadline for banner grabbing
	conn.SetReadDeadline(time.Now().Add(1 * time.Second))
	buffer := make([]byte, 512)
	n, _ := conn.Read(buffer)
	banner := string(buffer[:n])

	results <- ScanResult{
		Port:   port,
		IsOpen: true,
		Banner: banner,
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: recon <target_host>")
		os.Exit(1)
	}

	targetHost := os.Args[1]
	timeout := 2 * time.Second
	commonPorts := []int{21, 22, 25, 53, 80, 110, 143, 443, 445, 8080, 8443}

	fmt.Println("[+] Initializing ECLYPSA Native Recon Engine")
	fmt.Printf("[+] Target: %s\n", targetHost)
	fmt.Printf("[+] Scanning %d default ports...\n\n", len(commonPorts))

	var wg sync.WaitGroup
	results := make(chan ScanResult, len(commonPorts))

	for _, port := range commonPorts {
		wg.Add(1)
		go scanPort(targetHost, port, timeout, &wg, results)
	}

	// Close channel once all goroutines complete
	go func() {
		wg.Wait()
		close(results)
	}()

	openPorts := 0
	for res := range results {
		if res.IsOpen {
			openPorts++
			if len(res.Banner) > 0 {
				fmt.Printf("[OPEN] Port %d - Banner: %s\n", res.Port, res.Banner)
			} else {
				fmt.Printf("[OPEN] Port %d\n", res.Port)
			}
		}
	}

	fmt.Printf("\n[+] Recon scan completed. Found %d open ports.\n", openPorts)
}
