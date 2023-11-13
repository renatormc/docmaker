package main

import (
	"os"
	"os/exec"
	"path/filepath"
)

func main() {

	DOCTPL_HOME := os.Getenv("DOCTPL_HOME")
	args := []string{filepath.Join(DOCTPL_HOME, "main.py")}
	args = append(args, os.Args[1:]...)
	cmd := exec.Command(filepath.Join(DOCTPL_HOME, ".venv", "Scripts", "python.exe"), args...)
	err := cmd.Run()

	if err != nil {
		println(err.Error())
		return
	}

}
