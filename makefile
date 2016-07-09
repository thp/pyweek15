all:
	@echo "nothing to be done."

convert:
	python convert_sprites.py

crunch-files:
	# Make files smaller for distribution
	# (don't commit the changes, though - use "undo-crunch")
	(cd data/sprites/ && pngnq *.png)
	(cd data/sprites/ && for file in *-nq8.png; do mv $$file $$(basename $$file -nq8.png).png; done)
	(cd data/creatures/ && pngnq *.png)
	(cd data/creatures/ && for file in *-nq8.png; do mv $$file $$(basename $$file -nq8.png).png; done)
	(cd data/backgrounds/ && for file in *.jpg; do convert $$file -quality 70 $$file; done)
	(cd data/sounds/ && oggenc -q0 *.wav && rm *.wav)

clean:
	find . -name '*.pyc' -exec rm '{}' +

.PHONY: all convert crunch-files clean
.DEFAULT: all
