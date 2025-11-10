# mining.py
import time
import threading
from typing import List, Optional
from crypto import CryptoUtils, MerkleTree
from util import ByteUtils, Config, TimeUtils
from block import Block, BlockHeader
from transaction import Transaction, TransactionBuilder
from database import get_data_manager

class Miner:
    """Bitpy Miner (mengikuti algoritma PoW persis)"""
    
    def __init__(self, miner_address: str):
        self.miner_address = miner_address
        self.is_mining = False
        self.current_block: Optional[Block] = None
        self.hash_rate = 0
        self.thread: Optional[threading.Thread] = None
        self.found_blocks = 0
        
    def start_mining(self):
        """Mulai mining"""
        if self.is_mining:
            print("Mining sudah berjalan")
            return
            
        self.is_mining = True
        self.thread = threading.Thread(target=self._mining_loop, daemon=True)
        self.thread.start()
        print(f"Mining started for address: {self.miner_address}")
        
    def stop_mining(self):
        """Stop mining"""
        self.is_mining = False
        if self.thread:
            self.thread.join()
        print("Mining stopped")
        
    def _mining_loop(self):
        """Main mining loop"""
        while self.is_mining:
            try:
                if not self.current_block:
                    self._create_new_block()
                    
                if self.current_block:
                    found = self._mine_block()
                    if found:
                        self._submit_block()
            except Exception as e:
                print(f"Mining error: {e}")
                time.sleep(1)
                
    def _create_new_block(self):
        """Buat block baru untuk mining"""
        data_manager = get_data_manager()
        blockchain = data_manager.db
        
        # Dapatkan block terakhir
        prev_block = blockchain.get_best_block()
        if not prev_block:
            print("Tidak ada previous block, pastikan genesis block diinisialisasi")
            return
            
        # Dapatkan transactions dari mempool
        transactions = self._get_transactions_from_mempool()
        
        # Buat coinbase transaction (mining reward)
        coinbase_tx = self._create_coinbase_transaction()
        all_transactions = [coinbase_tx] + transactions
        
        # Hitung merkle root
        tx_hashes = [tx.get_txid() for tx in all_transactions]
        merkle_root = MerkleTree.compute_merkle_root(tx_hashes)
        
        # Dapatkan current difficulty
        difficulty = blockchain.get_difficulty()
        
        # Buat block header
        header = BlockHeader(
            version=1,
            prev_block_hash=prev_block.header.get_hash(),
            merkle_root=merkle_root,
            timestamp=TimeUtils.get_current_timestamp(),
            bits=difficulty,
            nonce=0
        )
        
        self.current_block = Block(header, all_transactions)
        print(f"New block created, mining... Difficulty: {difficulty:08x}")
        
    def _create_coinbase_transaction(self) -> Transaction:
        """Buat coinbase transaction (mining reward)"""
        data_manager = get_data_manager()
        block_height = data_manager.db.get_block_height() + 1
        
        # Hitung block reward (mengikuti Bitpy halving schedule)
        reward = self._calculate_block_reward(block_height)
        
        # Extra data (bisa berisi apa saja)
        extra_data = f"Python Bitpy Miner - Block {block_height}".encode()
        
        return TransactionBuilder.create_coinbase_transaction(
            block_height=block_height,
            miner_address=self.miner_address,
            reward=reward,
            extra_data=extra_data
        )
        
    def _calculate_block_reward(self, block_height: int) -> int:
        """Hitung block reward berdasarkan height (mengikuti Bitpy)"""
        # Initial reward: 50 BITPY
        reward = 50 * Config.COIN
        
        # Apply halving setiap 210,000 blocks
        halving_interval = Config.SUBSIDY_HALVING_INTERVAL
        halvings = block_height // halving_interval
        
        # Setelah setiap halving, reward dibagi 2
        for _ in range(halvings):
            reward //= 2
            
        return reward
        
    def _get_transactions_from_mempool(self) -> List[Transaction]:
        """Dapatkan transactions dari mempool"""
        # Dalam implementasi sederhana, ambil beberapa transactions
        # Di real implementation, pilih berdasarkan fee rate
        data_manager = get_data_manager()
        if hasattr(data_manager.db, 'mempool'):
            return data_manager.db.mempool.get_transactions()[:10]
        return []
        
    def _mine_block(self) -> bool:
        """Lakukan Proof-of-Work mining pada block"""
        if not self.current_block:
            return False
            
        start_time = time.time()
        hashes_calculated = 0
        max_nonce = 0xFFFFFFFF  # 4-byte nonce
        
        print(f"Mining block with target: {self.current_block.header.get_target():064x}")
        
        for nonce in range(self.current_block.header.nonce, max_nonce):
            if not self.is_mining:
                return False
                
            # Update nonce
            self.current_block.header.nonce = nonce
            
            # Calculate block hash
            block_hash = self.current_block.header.get_hash()
            hash_int = int.from_bytes(block_hash, 'big')
            
            hashes_calculated += 1
            
            # Update hash rate setiap 1000 hashes
            if hashes_calculated % 1000 == 0:
                elapsed = time.time() - start_time
                if elapsed > 0:
                    self.hash_rate = hashes_calculated / elapsed
                    
            # Check jika hash memenuhi target difficulty
            if hash_int <= self.current_block.header.get_target():
                elapsed = time.time() - start_time
                print(f"🎉 BLOCK MINED! Nonce: {nonce}")
                print(f"Block Hash: {block_hash.hex()}")
                print(f"Time: {elapsed:.2f}s, Hash Rate: {self.hash_rate:.2f} H/s")
                print(f"Transactions: {len(self.current_block.transactions)}")
                return True
                
        return False
        
    def _submit_block(self):
        """Submit mined block ke blockchain"""
        if not self.current_block:
            return
            
        data_manager = get_data_manager()
        success = data_manager.db.save_block(self.current_block)
        
        if success:
            print(f"✅ Block successfully added to blockchain!")
            print(f"Block Height: {data_manager.db.get_block_height()}")
            print(f"Block Hash: {self.current_block.header.get_hash_hex()}")
            
            # Broadcast block ke network
            self._broadcast_block()
            
            # Update stats
            self.found_blocks += 1
            
        else:
            print("❌ Failed to add block to blockchain")
            
        # Reset untuk block berikutnya
        self.current_block = None
        
    def _broadcast_block(self):
        """Broadcast block ke network P2P"""
        # Ini akan diintegrasikan dengan network layer
        global network_server
        if network_server and self.current_block:
            asyncio.create_task(network_server.broadcast_block(self.current_block))
            
    def get_mining_info(self) -> dict:
        """Dapatkan informasi mining saat ini"""
        return {
            'mining': self.is_mining,
            'miner_address': self.miner_address,
            'hash_rate': self.hash_rate,
            'found_blocks': self.found_blocks,
            'current_block': self.current_block.header.get_hash_hex() if self.current_block else None,
            'difficulty': self.current_block.header.get_target() if self.current_block else 0
        }

class MiningManager:
    """Manager untuk multiple miners"""
    
    def __init__(self):
        self.miners: List[Miner] = []
        self.active_miner: Optional[Miner] = None
        
    def create_miner(self, address: str) -> Miner:
        """Buat miner baru"""
        miner = Miner(address)
        self.miners.append(miner)
        return miner
        
    def start_mining(self, address: str):
        """Start mining dengan address tertentu"""
        # Stop miner aktif jika ada
        if self.active_miner:
            self.active_miner.stop_mining()
            
        # Cari atau buat miner untuk address ini
        miner = next((m for m in self.miners if m.miner_address == address), None)
        if not miner:
            miner = self.create_miner(address)
            
        self.active_miner = miner
        miner.start_mining()
        
    def stop_mining(self):
        """Stop semua mining"""
        if self.active_miner:
            self.active_miner.stop_mining()
        self.active_miner = None
        
    def get_mining_info(self) -> dict:
        """Dapatkan info mining"""
        if self.active_miner:
            return self.active_miner.get_mining_info()
        return {'mining': False, 'miners': len(self.miners)}

# Global mining manager
mining_manager = MiningManager()

def start_mining(address: str):
    """Start mining (untuk CLI)"""
    mining_manager.start_mining(address)
    
def stop_mining():
    """Stop mining (untuk CLI)"""
    mining_manager.stop_mining()
    
def get_mining_info() -> dict:
    """Dapatkan mining info (untuk CLI)"""
    return mining_manager.get_mining_info()

# Test function
def test_mining():
    """Test mining functionality"""
    print("Testing Bitpy Mining...")
    
    # Buat test address
    from crypto import CryptoUtils
    private_key = CryptoUtils.generate_private_key()
    public_key = CryptoUtils.private_to_public_key(private_key)
    address = CryptoUtils.create_bitpy_address(public_key)
    
    print(f"Mining to address: {address}")
    
    # Start mining
    miner = Miner(address)
    miner.start_mining()
    
    # Mining untuk 10 detik
    time.sleep(10)
    miner.stop_mining()
    
    print("Mining test completed")

if __name__ == "__main__":
    test_mining()
