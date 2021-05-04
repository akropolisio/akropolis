

for i in `find ./contracts/ -name "*.sol"`; do sh ./security/scribble/scribble.sh $i $1; done