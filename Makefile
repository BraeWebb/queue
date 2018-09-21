.PHONY: all spec

all: spec

spec:
	mkdir -p ./build/
	weasyprint ./spec/index.html ./build/a3.pdf

clean:
	rm -r ./build/
