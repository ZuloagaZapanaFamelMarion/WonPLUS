#!/bin/zsh
set -e
cd "$(dirname "$0")"
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
export PATH="$JAVA_HOME/bin:/opt/homebrew/opt/postgresql@16/bin:/opt/homebrew/bin:$PATH"
mkdir -p logs
mvn -q package
java -jar target/wonplus-1.0.0.jar
