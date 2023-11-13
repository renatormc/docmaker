package main

import (
	"log"
	"os"
	"os/exec"
	"path/filepath"
)

func main() {
	doctplHome := os.Getenv("DOCTPL_HOME")
	cmd := exec.Command(filepath.Join(doctplHome, ".venv", "Scripts", "python.exe"), filepath.Join(doctplHome, "main.py"), "gui")
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout
	if err := cmd.Run(); err != nil {
		log.Fatal(err)
	}
}
