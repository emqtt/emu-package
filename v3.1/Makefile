export

OS = $(shell uname -s)
REL_PROFILE ?= pkg
# The version-release used for package
PKG_VSN ?= 3.0
# Tag or branch to clone emqx-rel project
REL_TAG ?= emqx30
# Default tag for all emqx-rel dependencies
EMQX_DEPS_DEFAULT_VSN ?= emqx30
# Default name
EMQX_NAME ?= emqx
# Override the default
# emqx_vsn = v3.0.0
#
##
## Support RPM and Debian based linux systems
##
ifeq ($(OS),Linux)
	ISRPM  := $(shell cat /etc/redhat-release 2> /dev/null)
	ISDEB  := $(shell cat /etc/debian_version 2> /dev/null)
	ISSLES := $(shell cat /etc/SuSE-release 2> /dev/null)
	ifneq ($(ISRPM),)
		PKGERDIR := rpm
	else
		ifneq ($(ISDEB),)
			PKGERDIR := deb
		else
			ifneq ($(ISSLES),)
				PKGERDIR := rpm
			endif  # SLES
		endif  # deb
	endif  # rpm
endif  # linux

.PHONY: all
all: clean
	$(if $(PKGERDIR),,$(error "Operating system '$(OS)' not supported"))
	cd $(PKGERDIR) && $(MAKE)

clean:
	rm -rf package
	make -C rpm clean
	make -C deb clean

.PHONY: deb
deb:
	make -C deb

.PHONY: rpm
rpm:
	make -C rpm

