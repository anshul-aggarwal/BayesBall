#!/bin/bash
CURRENT_TIMESTAMP=$(date +"%m%d%y_%H%M%S")
REPORT_FILE="reports/"$CURRENT_TIMESTAMP"-report.txt";
ERROR_FILE="reports/"$CURRENT_TIMESTAMP"-error.txt";

{
FILE_NAME_REGEX="(test-cases\/)(.*?)(-)(\w*)(\.txt)";
numberOfTestCases=$(ls test-cases/*-graph.txt | wc -l)
totalCorrectAnswer=0
totalWrongAnswer=0
echo "Total Test Cases Found: ${numberOfTestCases}"
for graphFile in $(ls test-cases/*-graph.txt)
do
[[ $graphFile =~ $FILE_NAME_REGEX ]]
testCaseNumber=${BASH_REMATCH[2]};
echo "----------------------------------"
echo "Running Test Case: $testCaseNumber"
cp "test-cases/$testCaseNumber-graph.txt" "graph.txt"
cp "test-cases/$testCaseNumber-queries.txt" "queries.txt"
cp "test-cases/$testCaseNumber-ans.txt" "ans.txt"
python3 A0191501R_A0191496R.py > generatedAns.txt
diff -q generatedAns.txt ans.txt 1>/dev/null
if [[ $? == "0" ]]
then
  echo "Correct Answer"
  totalCorrectAnswer=$((totalCorrectAnswer+1))
else
  echo "Wrong Answer"
  totalWrongAnswer=$((totalWrongAnswer+1))
  echo "Generated Answer:"
  cat generatedAns.txt
fi
rm graph.txt queries.txt ans.txt generatedAns.txt
echo "----------------------------------"
done
echo "Total Correct Answers: $totalCorrectAnswer"
echo "Total Wrong Asnwers: $totalWrongAnswer"
} > "$REPORT_FILE" 2> "$ERROR_FILE";

echo "Generated Report File: $REPORT_FILE"
echo "Generate Error File: $ERROR_FILE"