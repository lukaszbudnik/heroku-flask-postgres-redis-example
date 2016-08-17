package loader

import (
	"github.com/lukaszbudnik/migrator/config"
	"github.com/lukaszbudnik/migrator/types"
)

// Loader interface abstracts all loading operations performed by migrator
type Loader interface {
	GetMigrations() []types.Migration
}

// CreateLoader abstracts all loading operations performed by migrator
func CreateLoader(config *config.Config) Loader {
	return &DiskLoader{config}
}
