.PHONY: critterpedia relink generate
all: generate relink
relink: linked/material.js linked/material.css
	cp linked/material.css unlinked/material.css
	cp linked/material.css docs/assets/material.css
	cp linked/material.js unlinked/material.js
	cp linked/material.js docs/assets/material.js
generate: critterpedia
critterpedia: web_templates/critterpedia.py
	python3 generate_page.py critterpedia

