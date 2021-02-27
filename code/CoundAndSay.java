/*
Dropbox

Count And Say

This question is mainly for college interns.

This question can directly be found on LeetCode.

A follow-up question is to read from a file stream of numbers.
*/

public class CountAndSay {
    public String countAndSay(int n) {
        StringBuilder curr = new StringBuilder("1");
        StringBuilder prev;
        int count;
        char say;
        for (int i = 1; i < n; i++) {
            prev = curr;
            curr = new StringBuilder();
            count = 1;
            say = prev.charAt(0);
            int len = prev.length();
            for (int j = 1; j < len; j++) {
                if (prev.charAt(j) != say) {
                    curr.append(count);
                    curr.append(say);
                    count = 1;
                    say=prev.charAt(j);
                    } else {
                        count++;
                    }
                }
                curr.append(count);
                curr.append(say);
            }
        return curr.toString();
    }
}