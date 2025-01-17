#!/bin/bash


# get all java files
FILES_TO_CHECK=$(find . -type f -name "*.java" | grep "./*/src/.*java")

HAS_CHANGES=false

for FILE in $FILES_TO_CHECK; do
    echo "Checking file: $FILE"
    java -jar .dev_tools/google-java-format-1.7-all-deps.jar $FILE | diff $FILE -
    if [ $? -ne 0 ]; then
        echo "File $FILE has changes after formatting."
        HAS_CHANGES=true
    else
        echo "File $FILE has no changes after formatting."
    fi
done

if [ "$HAS_CHANGES" = true ]; then
    echo "Run formatting failed, please try to run `sh lint.sh` and re-commit your java files!"
    exit 1
fi

mvn package

if [ $? -ne 0 ]; then
  echo "mvn package failed, please check if any unittest is failed!"
  exit -1
fi

echo "CI passed."