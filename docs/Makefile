# Makefile for Sphinx documentation

# Variables for sphinx-build:
#   You can set these variables from the command line
#   and the first two also from the environment.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Variables for sphinx-apidoc
SPHINXAPIDOC  ?= sphinx-apidoc
APIDOCDIR     = module
APIDOCMODULE  = ../src/switchmng

# "make" without argument is like "make help"
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: Route all targets to Sphinx
# $(O) is meant as a shortcut for $(SPHINXOPTS)
%: Makefile
	$(SPHINXAPIDOC) -o "$(APIDOCDIR)" --separate "$(APIDOCMODULE)"
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
