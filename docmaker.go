package main

import (
	"log"
	"os"
	"os/exec"
)

func main() {
	env := os.Environ()
	for i := range env {
		if env[i][:10] == "PYTHONPATH" {
			env = append(env[:i], env[i+1:]...)
			break
		}
	}
	cmd := exec.Command("$pythonExe", "$scriptFile")
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout
	cmd.Env = env
	if err := cmd.Run(); err != nil {
		log.Fatal(err)
	}
}
