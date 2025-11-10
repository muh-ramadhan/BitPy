# Bitpy Technical Specification

## Detailed Technical Specifications

### 1. Network Parameters

**Supply & Unit:**
- Total Supply: 1,000,000,000,000,000,000 (1 quintillion)
- Smallest Unit: 0.0001 coin (4 decimal places)
- Base Unit: 1 Satoshi = 0.0001 coin

**Block Parameters:**
- Target Block Time: 2.5 minutes
- Difficulty Adjustment: Every 2016 blocks
- Maximum Block Size: 4 MB

### 2. Cryptography Specifications

**Hashing Algorithms:**
- Block Hashing: SHA-256
- Address Generation: SHA-256 + RIPEMD-160
- Digital Signature: ECDSA with SECP256K1 curve

**Address Format:**
- Base58Check encoding
- Version byte: 0x1C (mainnet)
- 4-byte checksum

### 3. Data Structures

**Block Header:**
- Version: 4 bytes
- Previous Block Hash: 32 bytes
- Merkle Root: 32 bytes
- Timestamp: 4 bytes
- Difficulty Target: 4 bytes
- Nonce: 4 bytes

**Transaction:**
- Version: 4 bytes
- Input Count: Variable
- Inputs: List of transaction inputs
- Output Count: Variable
- Outputs: List of transaction outputs
- Lock Time: 4 bytes

### 4. Network Protocol

**Message Types:**
- VERSION: Initial handshake
- VERACK: Handshake confirmation
- ADDR: Node address list
- INV: Inventory (blocks/transactions)
- GETDATA: Specific data request
- TX: Transaction
- BLOCK: Block

**Peer Discovery:**
- DNS seeds for bootstrap
- Manual peer entry
- Exchange peer lists

### 5. Consensus Mechanisms

**Proof-of-Work:**
- Target difficulty adjustment
- Valid nonce discovery
- Block validation rules

**Transaction Validation:**
- Signature verification
- Double spend check
- Format validation
- Fee calculation verification

### 6. Economic Parameters

**Fee Structure:**
- Free Quota: 9,999,999 coins per 30 days
- Tier 1: 0.01% (10-50 million)
- Tier 2: 0.05% (50-500 million)
- Tier 3: 0.1% (500 million-5 billion)
- Tier 4: 0.2% (>5 billion)

**Reward Distribution:**
- Miners: 70% of total fees
- Staking: 20% of total fees
- Pending Supply: 10% of total fees

### 7. Security & Privacy

**Privacy Model:**
- Balances: Private
- Total Sent: Private
- Sender-Receiver: Public
- Transaction Amounts: Public

**Anti-Abuse Measures:**
- 30-day cumulative tracking
- Transaction rate limiting
- Tiered fee discouragement
