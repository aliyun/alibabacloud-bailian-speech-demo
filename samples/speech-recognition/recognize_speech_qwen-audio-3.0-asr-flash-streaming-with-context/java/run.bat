@echo off

call mvn clean
call mvn package
java -jar target/alibabacloud-bailian-speech-demo-java-1.0-SNAPSHOT.jar
