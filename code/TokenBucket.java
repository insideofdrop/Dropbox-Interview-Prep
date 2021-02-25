

public class TokenBucket {
    private final int MAX_CAPACITY;
    private final int FILL_RATE;

    private List<Integer> bucket;
    private long lastFillTimeStamp;

    final Lock lock = new ReentrantLock(); 
    final Condition notFull = lock.newCondition();
    final Condition notEmpty = lock.newCondition();
    
    public TokenBucket(int maxCapacity, int fillRate) {
        this.MAX_CAPACITY = maxCapacity;
        this.FILL_RATE = fillRate;
        this.lastFillTimeStamp = System.currentTimeMillis();
        this.bucket = new ArrayList<>(); 
    }
    
    public void fill() throws InterruptedException {
        lock.lock();
        while (bucket.size() == MAX_CAPACITY) {
            System.out.println("Bucket is filled now.");
            notFull.await();
        }
        long now = System.currentTimeMillis();
        long numTokensToAdd = Math.min(MAX_CAPACITY - bucket.size(), (now - lastFillTimeStamp)/1000 * FILL_RATE);
        lastFillTimeStamp = now;

        for (int i=0; i < numTokensToAdd; i++) { //add tokens
            bucket.add((int) (Math.random() * 100) + 1);  
        }
        notEmpty.signalAll();
        lock.unlock();
    }

    public List<Integer> get(int n) throws InterruptedException {
        if (n <= 0) {
            throw new IllegalArgumentException("Cannot get zero or negative number of tokens.");
        }
        if (n > MAX_CAPACITY) {
            throw new IllegalArgumentException("Cannot get more tokens than max capacity.")
        }
        List<Integer> result = new ArrayList<>();
        int tokenAcquired = 0;

        while (tokenAcquired < n) { //this can ensure fair competition
            lock.lock();
            while (bucket.size() < 1) {
                // The bucket is not big enough.
                notEmpty.await();
            }
            result.add(bucket.get(bucket.size()-1));
            bucket.remove(bucket.size()-1);
            tokenAcquired++;
            notFull.signalAll();
            lock.unlock();
        }
        return result;
    }
}