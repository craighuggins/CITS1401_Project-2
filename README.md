# CITS1401_Project-2
Using Stylometry to Verify Authorship

This program is intended to check for plagiarism between two texts by looking for stylistic similarities. These similarities lie in the way an author uses language, rather than similarities in the actual words themselves.

The program reads in two text files containing the works to be analysed, and builds a profile for each. The two profiles are compared and returned besides a score which reflects the distance between the two works in terms of their style. Low scores imply that the same author is likely responsible for both works, while large scores imply different authors. For example, a score of 0 means that the two works are identical.

Running the program:
- Call the main function and provide the three required arguments, as follows...
- main(textfile1, textfile2, feature)
  - 'textfile1' and 'textfile2' are the names of the text files to be analysed (input as strings in quotations)
  - 'feature' is the type of feature that will be used to compare the document profiles.
      - The allowed features are: "punctuation", "unigrams", "conjunctions" and "composite"
