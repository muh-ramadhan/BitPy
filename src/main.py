# main.py
#!/usr/bin/env python3
"""
Bitpy Python - CLI Interface
Implementasi Bitpy lengkap dalam Python dengan interface command line
"""

import argparse
import asyncio
import sys
import os
from typing import Optional

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_data_manager, DataManager
from wallet import Wallet, WalletManager, format_bitpys, parse_bitpy_amount
from mining import start_mining, stop_mining, get_mining_info
from network import start_network_server, TransactionMempool
from util import ByteUtils, Config

class BitpyCLI:
    """Bitpy Command Line Interface"""
    
    def __init__(self):
        self.data_manager = get_data_manager()
        self.wallet_manager = WalletManager()
        self.running = True
        
    def print_banner(self):
        """Print welcome banner"""
        print("=" * 60)
        print("           BIT PYTHON - CLI INTERFACE")
        print("            help to show all main menu")
        print("=" * 60)
        print()
        
    def run(self):
        """Main CLI loop"""
        self.print_banner()
        
        # Initialize genesis block jika pertama kali
        if self.data_manager.db.get_block_count() == 0:
            print("Initializing genesis block...")
            self.data_manager.initialize_genesis_block()
        
        while self.running:
            try:
                command = input("\nbitpy> ").strip()
                
                if not command:
                    continue
                    
                if command in ['quit', 'exit', 'q']:
                    self.running = False
                    print("Goodbye! 👋")
                    
                elif command == 'help':
                    self.show_help()
                    
                elif command == 'status':
                    self.show_status()
                    
                elif command.startswith('createwallet'):
                    self.handle_createwallet(command)
                    
                elif command.startswith('getbalance'):
                    self.handle_getbalance(command)
                    
                elif command.startswith('send'):
                    self.handle_send(command)
                    
                elif command.startswith('mine'):
                    self.handle_mine(command)
                    
                elif command == 'stopmining':
                    self.handle_stopmining()
                    
                elif command == 'mininginfo':
                    self.handle_mininginfo()
                    
                elif command == 'getblockcount':
                    self.handle_getblockcount()
                    
                elif command.startswith('getblock'):
                    self.handle_getblock(command)
                    
                elif command == 'getbestblockhash':
                    self.handle_getbestblockhash()
                    
                elif command.startswith('listaddresses'):
                    self.handle_listaddresses(command)
                    
                elif command == 'startnode':
                    self.handle_startnode()
                    
                elif command == 'getpeerinfo':
                    self.handle_getpeerinfo()
                    
                elif command == 'dumpblockchain':
                    self.handle_dumpblockchain()
                    
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Show help message"""
        print("\nAvailable Commands:")
        print("  help                      - Show this help")
        print("  status                    - Show node status")
        print("  createwallet [name]       - Create new wallet")
        print("  getbalance [addr]         - Get balance for address")
        print("  listaddresses [wallet]    - List addresses in wallet")
        print("  send <from> <to> <amount> - Send Bitpy")
        print("  mine <address>            - Start mining to address")
        print("  stopmining                - Stop mining")
        print("  mininginfo                - Show mining information")
        print("  getblockcount             - Get current block height")
        print("  getblock <hash>           - Get block information")
        print("  getbestblockhash          - Get best block hash")
        print("  startnode                 - Start P2P network node")
        print("  getpeerinfo               - Get peer information")
        print("  dumpblockchain            - Dump blockchain info")
        print("  quit                      - Exit Bitpy CLI")
    
    def show_status(self):
        """Show node status"""
        blockchain = self.data_manager.db
        wallet = self.wallet_manager.current_wallet
        
        print("\n=== BITPY NODE STATUS ===")
        print(f"Block Height: {blockchain.get_block_height()}")
        print(f"Block Count:  {blockchain.get_block_count()}")
        print(f"Difficulty:   {blockchain.difficulty:08x}")
        
        if wallet:
            print(f"Wallet:       {wallet.name}")
            print(f"Addresses:    {len(wallet.get_addresses())}")
            
            # Calculate total balance
            total_balance = 0
            for addr in wallet.get_addresses():
                balance = blockchain.get_balance(addr)
                total_balance += balance
                if balance > 0:
                    print(f"  {addr}: {format_bitpys(balance)}")
            
            print(f"Total Balance: {format_bitpys(total_balance)}")
        else:
            print("Wallet:       No wallet loaded")
        
        mining_info = get_mining_info()
        print(f"Mining:       {'Yes' if mining_info['mining'] else 'No'}")
        if mining_info['mining']:
            print(f"Hash Rate:    {mining_info['hash_rate']:.2f} H/s")
    
    def handle_createwallet(self, command: str):
        """Handle createwallet command"""
        parts = command.split()
        wallet_name = parts[1] if len(parts) > 1 else "default"
        
        wallet = self.wallet_manager.create_wallet(wallet_name)
        print(f"✅ Wallet '{wallet_name}' created!")
        print(f"First address: {wallet.default_address}")
    
    def handle_getbalance(self, command: str):
        """Handle getbalance command"""
        parts = command.split()
        
        if len(parts) > 1:
            # Get balance for specific address
            address = parts[1]
            balance = self.data_manager.db.get_balance(address)
            print(f"Balance for {address}: {format_bitpys(balance)}")
        else:
            # Get balance for current wallet
            wallet = self.wallet_manager.current_wallet
            if not wallet:
                print("No wallet loaded. Use 'createwallet' first.")
                return
            
            total_balance = 0
            print(f"Balances for wallet '{wallet.name}':")
            for addr in wallet.get_addresses():
                balance = self.data_manager.db.get_balance(addr)
                total_balance += balance
                print(f"  {addr}: {format_bitpys(balance)}")
            
            print(f"Total: {format_bitpys(total_balance)}")
    
    def handle_send(self, command: str):
        """Handle send command"""
        parts = command.split()
        if len(parts) != 4:
            print("Usage: send <from_address> <to_address> <amount>")
            return
        
        from_addr = parts[1]
        to_addr = parts[2]
        amount_str = parts[3]
        
        try:
            amount = parse_bitpy_amount(amount_str)
            
            # Get wallet
            wallet = self.wallet_manager.current_wallet
            if not wallet:
                print("No wallet loaded. Use 'createwallet' first.")
                return
            
            # Get UTXOs for from_address
            utxos = self.data_manager.db.get_utxos_for_address(from_addr)
            if not utxos:
                print(f"No UTXOs found for address: {from_addr}")
                return
            
            # Create transaction
            transaction = wallet.create_transaction(from_addr, to_addr, amount, utxos)
            if transaction:
                print(f"✅ Transaction created successfully!")
                print(f"TXID: {transaction.get_txid_hex()}")
                print(f"Amount: {format_bitpys(amount)}")
                print(f"From: {from_addr}")
                print(f"To: {to_addr}")
                
                # Add to mempool (simulated)
                self.data_manager.db.mempool.add_transaction(transaction)
                print("Transaction added to mempool")
            else:
                print("❌ Failed to create transaction")
                
        except Exception as e:
            print(f"Error: {e}")
    
    def handle_mine(self, command: str):
        """Handle mine command"""
        parts = command.split()
        if len(parts) != 2:
            print("Usage: mine <address>")
            return
        
        address = parts[1]
        print(f"🚀 Starting mining to address: {address}")
        print("Press Ctrl+C to stop mining")
        
        # Start mining in background
        start_mining(address)
    
    def handle_stopmining(self):
        """Handle stopmining command"""
        stop_mining()
        print("⛔ Mining stopped")
    
    def handle_mininginfo(self):
        """Handle mininginfo command"""
        info = get_mining_info()
        print("\n=== MINING INFORMATION ===")
        print(f"Mining:      {'Yes' if info['mining'] else 'No'}")
        if info['mining']:
            print(f"Address:     {info['miner_address']}")
            print(f"Hash Rate:   {info['hash_rate']:.2f} H/s")
            print(f"Found Blocks: {info['found_blocks']}")
            print(f"Current Block: {info['current_block']}")
            print(f"Difficulty:  {info['difficulty']:08x}")
    
    def handle_getblockcount(self):
        """Handle getblockcount command"""
        count = self.data_manager.db.get_block_count()
        print(f"Block Count: {count}")
    
    def handle_getblock(self, command: str):
        """Handle getblock command"""
        parts = command.split()
        if len(parts) != 2:
            print("Usage: getblock <hash>")
            return
        
        block_hash = parts[1]
        block = self.data_manager.db.get_block(block_hash)
        
        if block:
            print(f"\n=== BLOCK {block_hash} ===")
            print(f"Height:       {self.data_manager.db.get_block_height()}")
            print(f"Version:      {block.header.version}")
            print(f"Prev Hash:    {block.header.prev_block_hash.hex()}")
            print(f"Merkle Root:  {block.header.merkle_root.hex()}")
            print(f"Timestamp:    {block.header.timestamp}")
            print(f"Bits:         {block.header.bits:08x}")
            print(f"Nonce:        {block.header.nonce}")
            print(f"Transactions: {len(block.transactions)}")
            
            # Show first few transactions
            for i, tx in enumerate(block.transactions[:3]):
                print(f"  TX {i}: {tx.get_txid_hex()}")
            
            if len(block.transactions) > 3:
                print(f"  ... and {len(block.transactions) - 3} more transactions")
        else:
            print(f"Block not found: {block_hash}")
    
    def handle_getbestblockhash(self):
        """Handle getbestblockhash command"""
        best_block = self.data_manager.db.get_best_block()
        if best_block:
            print(f"Best Block Hash: {best_block.header.get_hash_hex()}")
        else:
            print("No blocks in blockchain")
    
    def handle_listaddresses(self, command: str):
        """Handle listaddresses command"""
        parts = command.split()
        wallet_name = parts[1] if len(parts) > 1 else "default"
        
        wallet = self.wallet_manager.get_wallet(wallet_name)
        if not wallet:
            print(f"Wallet '{wallet_name}' not found")
            return
        
        print(f"Addresses in wallet '{wallet_name}':")
        for addr in wallet.get_addresses():
            balance = self.data_manager.db.get_balance(addr)
            print(f"  {addr} - {format_bitpys(balance)}")
    
    async def handle_startnode(self):
        """Handle startnode command"""
        print("Starting P2P network node...")
        
        # Initialize mempool
        mempool = TransactionMempool()
        self.data_manager.db.mempool = mempool
        
        # Start network server
        await start_network_server(
            blockchain=self.data_manager.db,
            mempool=mempool,
            host='0.0.0.0',
            port=Config.DEFAULT_PORT
        )
    
    def handle_getpeerinfo(self):
        """Handle getpeerinfo command"""
        # This would show connected peers in a real implementation
        print("Peer information not available in standalone mode")
        print("Use 'startnode' to enable P2P networking")
    
    def handle_dumpblockchain(self):
        """Handle dumpblockchain command"""
        print("\n=== BLOCKCHAIN DUMP ===")
        blockchain = self.data_manager.db
        
        for i, block_hash in enumerate(blockchain.blocks.keys()):
            block = blockchain.blocks[block_hash]
            print(f"Block {i}: {block_hash}")
            print(f"  Transactions: {len(block.transactions)}")
            print(f"  Timestamp: {block.header.timestamp}")
            
            if i >= 10:  # Show only first 10 blocks
                print(f"... and {len(blockchain.blocks) - 10} more blocks")
                break

def main():
    """Main function"""
    cli = BitpyCLI()
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        # Single command mode
        command = ' '.join(sys.argv[1:])
        if command == 'startnode':
            asyncio.run(cli.handle_startnode())
        else:
            print(f"Single command mode not implemented for: {command}")
            print("Run without arguments for interactive mode")
    else:
        # Interactive mode
        cli.run()

if __name__ == '__main__':
    main()
