# Makefile for Sphinx documentation

# Variables for sphinx-build:
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Variables for sphinx-apidoc
SPHINXAPIDOC  ?= sphinx-apidoc
APIDOCDIR     = module
APIDOCMODULE  = ../switchmng

# "make" without argument is like "make help"
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

.PHONY: help Makefile

# Catch-all target: Route all targets to Sphinx
# $(O) is meant as a shortcut for $(SPHINXOPTS)
%: Makefile
	$(SPHINXAPIDOC) -o "$(APIDOCDIR)" "$(APIDOCMODULE)"
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
