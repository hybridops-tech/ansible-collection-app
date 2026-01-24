# purpose: Test wrapper for Molecule scenarios in the hybridops.app collection.
# adr: ADR-0606-ansible-collections-release-process
# maintainer: HybridOps.Studio

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

COLLECTION_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
ROLES_DIR := $(COLLECTION_ROOT)/roles

ROLE ?=

MOLECULE_ROLES := $(shell \
  find "$(ROLES_DIR)" -mindepth 1 -maxdepth 1 -type d 2>/dev/null \
    | while read -r d; do \
        if [ -d "$$d/molecule/default" ]; then basename "$$d"; fi; \
      done \
)

ifeq ($(strip $(ROLE)),)
TEST_ROLES := $(MOLECULE_ROLES)
else
TEST_ROLES := $(ROLE)
endif

.PHONY: help test

help:
	@echo ""
	@echo "Usage:"
	@echo "  make test [ROLE=<role_name>]"
	@echo ""
	@echo "Targets:"
	@echo "  make test              Run molecule test for all roles with scenarios."
	@echo "  make test ROLE=<name>  Run molecule test for a single role."
	@echo ""
	@echo "Detected roles with Molecule scenarios:"
	@echo "  $(MOLECULE_ROLES)"
	@echo ""

test:
	@if [ -z "$(strip $(TEST_ROLES))" ]; then \
	  echo "No roles with Molecule scenarios found under $(ROLES_DIR)"; \
	  exit 1; \
	fi
	@for r in $(TEST_ROLES); do \
	  role_dir="$(ROLES_DIR)/$$r"; \
	  if [ ! -d "$$role_dir/molecule/default" ]; then \
	    echo "Skipping $$r (no molecule/default scenario)"; \
	    continue; \
	  fi; \
	  echo "==> molecule test for role: $$r"; \
	  (cd "$$role_dir" && molecule test) || exit $$?; \
	done
