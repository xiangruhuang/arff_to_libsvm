
Dirs=Eur-Lex delicious bibtex

all: 
	for i in $(Dirs); do \
		make $$i.svm; \
	done

enum=0
numeric=0
num_labels=0

target_file="temp"
source_dir="."
arff=

convert:
	@echo converting $(source_dir)
	for i in $(wildcard $(source_dir)/*.arff); do \
		python arff2libsvm.py $$i $(target_file).tmp $(enum) $(numeric) $(num_labels); \
	done
	python hash.py $(target_file).tmp $(target_file)
	rm $(target_file).tmp

Eur-Lex.svm:
	$(eval enum := 0)
	$(eval numeric := 5000)
	$(eval num_labels := 3993)
	$(eval source_dir := Eur-Lex)
	$(eval target_file := Eur-Lex.svm)
	make convert enum=$(enum) numeric=$(numeric) num_labels=$(num_labels) source_dir=$(source_dir) target_file=$(target_file)

delicious.svm:
	$(eval enum := 500)
	$(eval numeric := 0)
	$(eval num_labels := 983)
	$(eval source_dir := delicious)
	$(eval target_file := delicious.svm)
	make convert enum=$(enum) numeric=$(numeric) num_labels=$(num_labels) source_dir=$(source_dir) target_file=$(target_file)

bibtex.svm:
	$(eval enum := 1836)
	$(eval numeric := 0)
	$(eval num_labels := 159)
	$(eval source_dir := bibtex)
	$(eval target_file := bibtex.svm)
	make convert enum=$(enum) numeric=$(numeric) num_labels=$(num_labels) source_dir=$(source_dir) target_file=$(target_file)
