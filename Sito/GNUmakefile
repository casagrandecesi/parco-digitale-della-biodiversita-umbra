.PHONY: upload server public clean check_hugo help

uname_s := $(shell uname -s)
uname_m := $(shell uname -m)
hugo_dir := tools/hugo/$(uname_s)/$(uname_m)
export PATH := $(hugo_dir):$(PATH)

help:
	@echo
	@echo 'Available targets: '
	@echo
	@echo '   help      Show this help'
	@echo '   server    Start the local development server'
	@echo '   upload    Upload the website to the FTP server'
	@echo '   public    Compile the website in the public/ directory'
	@echo '   clean     Remove hugo-generated files and directories'
	@echo

server: check_hugo
	$(hugo_dir)/hugo server

public: check_hugo
	$(hugo_dir)/hugo --minify

clean:
	rm -fr public/ resources/

check_hugo:
	@test -x "$(hugo_dir)/hugo" || { echo 'There is no hugo executable for this architecture, exiting...'; exit 1; }
