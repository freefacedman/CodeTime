import java.util.ArrayList;
import java.util.HashMap;

public class BlockChain {
    public static final int CUT_OFF_AGE = 10;
    private TransactionPool transactionPool;
    private HashMap<ByteArrayWrapper, BlockNode> blockchain;
    private BlockNode maxHeightBlockNode;

    private class BlockNode {
        public Block block;
        public BlockNode parent;
        public ArrayList<BlockNode> children;
        public UTXOPool utxoPool;
        public int height;

        public BlockNode(Block block, BlockNode parent, UTXOPool utxoPool, int height) {
            this.block = block;
            this.parent = parent;
            this.children = new ArrayList<>();
            this.utxoPool = utxoPool;
            this.height = height;
            if (parent != null) {
                parent.children.add(this);
            }
        }
    }

    public BlockChain(Block genesisBlock) {
        UTXOPool utxoPool = new UTXOPool();
        // Assume the genesis block includes a coinbase tx. Process it to update the UTXOPool.
        addCoinbaseToUTXOPool(genesisBlock, utxoPool);
        
        this.transactionPool = new TransactionPool();
        this.blockchain = new HashMap<>();
        BlockNode genesisNode = new BlockNode(genesisBlock, null, utxoPool, 1);
        this.maxHeightBlockNode = genesisNode;
        blockchain.put(new ByteArrayWrapper(genesisBlock.getHash()), genesisNode);
    }

    public Block getMaxHeightBlock() {
        return maxHeightBlockNode.block;
    }

    public UTXOPool getMaxHeightUTXOPool() {
        return new UTXOPool(maxHeightBlockNode.utxoPool); // Return a defensive copy
    }

    public TransactionPool getTransactionPool() {
        return transactionPool;
    }

    public boolean addBlock(Block block) {
        if (block.getPrevBlockHash() == null) {
            return false; // Reject the genesis block or blocks without a parent.
        }

        ByteArrayWrapper prevBlockHash = new ByteArrayWrapper(block.getPrevBlockHash());
        BlockNode parentBlockNode = blockchain.get(prevBlockHash);
        if (parentBlockNode == null) {
            return false; // Parent block not found.
        }

        UTXOPool newUTXOPool = new UTXOPool(parentBlockNode.utxoPool);
        ArrayList<Transaction> transactions = block.getTransactions();
        
        // Create a temporary TxHandler to validate transactions
        TxHandler validator = new TxHandler(newUTXOPool);
        for (Transaction tx : transactions) {
            if (!validator.isValidTx(tx)) {
                return false; // Transaction is invalid
            }

            // Update the UTXOPool for each valid transaction
            updateUTXOPoolWithTransaction(tx, newUTXOPool);
        }

        int newHeight = parentBlockNode.height + 1;
        if (newHeight <= maxHeightBlockNode.height - CUT_OFF_AGE) {
            return false; // Block is too old.
        }

        // If transactions are valid, add the block
        BlockNode newNode = new BlockNode(block, parentBlockNode, newUTXOPool, newHeight);
        blockchain.put(new ByteArrayWrapper(block.getHash()), newNode);

        if (newHeight > maxHeightBlockNode.height) {
            maxHeightBlockNode = newNode; // Update if new block extends the blockchain to a greater height.
        }

        // Update the transaction pool by removing transactions included in the new block
        transactions.forEach(tx -> transactionPool.removeTransaction(tx.getHash()));

        return true;
    }

    private void updateUTXOPoolWithTransaction(Transaction tx, UTXOPool utxoPool) {
        // Remove consumed UTXOs
        for (Transaction.Input in : tx.getInputs()) {
            UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
            utxoPool.removeUTXO(utxo);
        }
        // Add new UTXOs
        for (int i = 0; i < tx.numOutputs(); i++) {
            Transaction.Output out = tx.getOutput(i);
            UTXO utxo = new UTXO(tx.getHash(), i);
            utxoPool.addUTXO(utxo, out);
        }
    }

    private void addCoinbaseToUTXOPool(Block genesisBlock, UTXOPool utxoPool) {
        // Assuming the coinbase transaction is the first transaction in the block
        Transaction coinbaseTx = genesisBlock.getCoinbase();
        for (int i = 0; i < coinbaseTx.numOutputs(); i++) {
            UTXO utxo = new UTXO(coinbaseTx.getHash(), i);
            utxoPool.addUTXO(utxo, coinbaseTx.getOutput(i));
        }
    }

    public void addTransaction(Transaction tx) {
        transactionPool.addTransaction(tx);
    }
}
