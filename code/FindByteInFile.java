/*
Dropbox

Find Byte in File

Given a pattern of bytes, return true if the pattern is a subarray of the file content.

The brute force solution is to try to match the pattern to a subset of the text as shown in the function
FindByteInFile.containsBytes below. (This problem is also called "Finding a Needle in a Haystack" and "StrStr")

This will lead to lots of wasted time pursuing partial matches. To reduce this, we can use a rolling hash
to find all the candidate spots in the string. 

Look up Rabin-Karp's algorithm for more background on rolling hashes.

Your interviewer might not even want you to actually write a rolling hash function. Ask if you can assume
that there's a rolling hash function that lets you get hashes of length pattern.length from the file.

Your interviewer might also want to you to mimic the process of reading and opening the file. 
*/

public class FindByteInFile {
    
    public boolean containsBytes(byte[] pattern, byte[] file) {
        if (file == null && pattern != null) {
            return false;
        }
        if (pattern == null && file == null) {
            return true;
        }
        if (pattern.length > file.length) {
            return false;
        }
        for (int start = 0; start <= file.length - pattern.length; start++) {
            int end = 0;
            while (end < pattern.length && pattern[end] == file[start + end]) {
                end++;
            }
            if (end == pattern.length) {
                return true;
            }
        }
        return false;
    }

    //-----------------------
    //-----------------------
    //ALTERNATIVE IMPLEMENTATION WITH ROLLING HASH
    //-----------------------
    //-----------------------

    public boolean containsBytesRollingHash(byte[] pattern, byte[] text) {
        if (text.length < pattern.length) {
            return false;
        }
        int m = pattern.length;
        int n = text.length; 
        byte[] initialBytes = Arrays.copyOfRange(text, 0, m);
        RollingHash hashFun = new RollingHash(31, initialBytes);
        long patternHashVal = hashFun.hash(pattern);
        for (int start = 0; i <= n - m; i++) {
            if (patternHashVal == hashFun.getCurrHashValue()) {
                //need to check byte by byte to ensure 
                int end = 0; 
                while (end < m && pattern[j] == text[start + end]) {
                    end++;
                }
                if (end == m) {
                    return true;
                }
            }
            if (i < n - m) {
                hashFun.recompute(text[start], text[start + m]);
            }
        }
        return false;
    }
}

class RollingHash {
    // Ask if you can assume that you have a rolling hash class before you start implementing
    // your own rolling hash. Most interviewers won't make you create your own.
    private final int WINDOW_LENGTH;
    private long currHashValue;

    public RollingHash(int a, byte[] initialBytes) {
        this.a = a;
        this.WINDOW_LENGTH = initialBytes.length;
        // The value of h would be "pow(a, WINDOW_LENGTH - 1) % q 
        for (int i = 0; i < WINDOW_LENGTH-1; i++) {
            //a^n % p = (a^n-1 % p * a%p)%p; 
            h = (h * a) % LARGE_PRIME;
        }
        currHashValue = hash(initialBytes);
    }

    public long hash(byte[] bytes) {
        int hashVal = 0;

        for (int i = 0; i < bytes.length; i++) {
            hashVal = (a * hashVal + bytes[i]) % LARGE_PRIME;
        }
        return hashVal;
    }

    public long update(byte removed, byte incoming) {
        // Relevant math:
        // (a + b) % p = (a % p + b % p) % p
        // (a - b) % p = (a % p - b % p) % p might give negative
        // (a * b) % p = (a %p  * b % p) % p
        currHashValue = (a * (currHashValue - removed * h) + incoming) % LARGE_PRIME;

        // We might get negative value of t, converting it to positive
        if (currHashValue < 0) {
            currHashValue += LARGE_PRIME;
        }
        return currHashValue;
    }

    public long getCurrHashValue() {
        return currHashValue;
    }
}