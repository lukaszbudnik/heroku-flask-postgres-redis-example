package main

import (
	"github.com/lukaszbudnik/migrator/xcli"
	"github.com/lukaszbudnik/migrator/db"
	"github.com/lukaszbudnik/migrator/loader"
)

func main() {
	configFile := "migrator.yaml"
	config := xcli.ReadConfig(&configFile)
	xcli.ApplyMigrations(config, db.CreateConnector, loader.CreateLoader)
}
