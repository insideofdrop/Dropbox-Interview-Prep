/*
Dropbox

Phone Number / Dictionary

Given a string of digits (i.e. a phone number), return the list of words in a dictionary that can be formed
from that phone number on a keypad.

Solution: Use backtracking.
Use a trie in addition to backtracking to reduce needless backtracking.

Your interviewer might not require you to code the trie. Just know how you would use it.

1. Turn the dict into a tree so that you can search the words more quickly.
2. As you proceed through the phone number, you check whether the next character is a part of the trie.
3. If the prefix you've made so far is in the tree, then keep going. 
4. If the prefix you've made so far is not in the tree, then do not proceed with that prefix.
*/


public class PhoneNumberDict {
    private final static String[] KEYS = {"","","abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    private static Set<String> dict;

    // Brute force - generate the words and then check them in the dictionary
    public List<String> letterCombinations(String digits) {
        List<String> combinations = new ArrayList<>();
        if (digits == null || digits.length() < 1) {
            return combinations;
        }
        findCombinations(combinations, new StringBuilder(), digits, 0);

        return combinations;
    }

    public void findCombinations(List<String> combinations, StringBuilder sb, String digits, int i) {
        if (i == digits.length()) {
            String comb = sb.toString();
            if (isWord(comb)) {
                combinations.add(comb);
            }
        } else {
            String keyLetters = KEYS[digits.charAt(i) - '0'];
            for (int k = 0; k < keyLetters.length(); k++) {
                sb.append(keyLetters.charAt(k));
                findCombinations(combinations, sb, digits, i + 1);
                sb.setLength(sb.length() - 1);
            }
        }
    }

    public boolean isWord(String word) {
        return dict.contains(word);
    }
}

class Node {
    Map<Character, Node> children;
    boolean isWord;

    public Node() {
        children = new HashMap<Character, Node>();
        isWord = false;
    }
}

class Trie {
    private Node root;

    // Initialize your data structure here.
    public Trie() {
        root = new Node();
    }

    // Inserts a word into the trie.
    public void insert(String word) {
        Node curr = root;
        for (int i = 0; i < word.length(); i++) {
            Node temp = curr.children.get(word.charAt(i));
            if (temp == null) {
                temp = new Node();
                curr.children.put(word.charAt(i), temp);
            }
            curr = temp;
        }
        curr.isCompleteWord = true;
    }

    /** Returns if the word is in the trie. */
    public boolean search(String word) {
        Node curr = root; 
        for (int i = 0; i < word.length(); i++) {
            curr = curr.children.get(word.charAt(i));
            if (curr == null) {
                return false;
            }
        }
        return curr.isWord;
    }
    
    public Node search(Node trieNode, char c) {
        return trieNode.children.get(c);
    }

    /** Returns if there is any word in the trie that starts w ith the given prefix. */
    public boolean startsWith(String prefix) {
        Node curr = root;
        for (int i = 0; i < prefix.length(); i++) {
            curr = curr.children.get(prefix.charAt(i));
            if (curr == null) {
                return false;
            }
        }
        return true;
    }
}