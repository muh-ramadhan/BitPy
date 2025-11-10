# script.py
"""
Bitpy Script Interpreter
"""

from typing import List, Optional, Any
from crypto import CryptoUtils
from util import ByteUtils

class ScriptError(Exception):
    """Error dalam eksekusi script"""
    pass

class Script:
    """
    Bitpy Script Interpreter
    """
    
    def __init__(self):
        self.stack: List[bytes] = []
        self.altstack: List[bytes] = []
        self.pc = 0  # Program counter
        self.last_code_separator = 0
        self.execution_success = True
        
    def evaluate(self, script_sig: bytes, script_pubkey: bytes) -> bool:
        """
        Evaluate script combination (scriptSig + scriptPubKey)
        """
        # Combine scripts (scriptSig dijalankan pertama, lalu scriptPubKey)
        combined_script = script_sig + script_pubkey
        return self.execute(combined_script)
        
    def execute(self, script: bytes) -> bool:
        """
        Execute Bitpy script opcode
        """
        self.stack = []
        self.altstack = []
        self.pc = 0
        self.execution_success = True
        
        try:
            while self.pc < len(script) and self.execution_success:
                opcode = script[self.pc]
                self.pc += 1
                
                # Data pushing opcodes (0x01 - 0x4b)
                if 1 <= opcode <= 75:
                    # Push opcode bytes ke stack
                    data_length = opcode
                    if self.pc + data_length > len(script):
                        raise ScriptError("PUSHDATA melebihi batas script")
                    
                    data = script[self.pc:self.pc + data_length]
                    self.pc += data_length
                    self.stack.append(data)
                    continue
                    
                # OP_PUSHDATA1
                elif opcode == 76:
                    if self.pc >= len(script):
                        raise ScriptError("OP_PUSHDATA1 tanpa data")
                    
                    data_length = script[self.pc]
                    self.pc += 1
                    
                    if self.pc + data_length > len(script):
                        raise ScriptError("OP_PUSHDATA1 melebihi batas")
                    
                    data = script[self.pc:self.pc + data_length]
                    self.pc += data_length
                    self.stack.append(data)
                    continue
                    
                # OP_PUSHDATA2
                elif opcode == 77:
                    if self.pc + 1 >= len(script):
                        raise ScriptError("OP_PUSHDATA2 tanpa data")
                    
                    data_length = int.from_bytes(script[self.pc:self.pc+2], 'little')
                    self.pc += 2
                    
                    if self.pc + data_length > len(script):
                        raise ScriptError("OP_PUSHDATA2 melebihi batas")
                    
                    data = script[self.pc:self.pc + data_length]
                    self.pc += data_length
                    self.stack.append(data)
                    continue
                    
                # OP_PUSHDATA4
                elif opcode == 78:
                    if self.pc + 3 >= len(script):
                        raise ScriptError("OP_PUSHDATA4 tanpa data")
                    
                    data_length = int.from_bytes(script[self.pc:self.pc+4], 'little')
                    self.pc += 4
                    
                    if self.pc + data_length > len(script):
                        raise ScriptError("OP_PUSHDATA4 melebihi batas")
                    
                    data = script[self.pc:self.pc + data_length]
                    self.pc += data_length
                    self.stack.append(data)
                    continue
                
                # Handle other opcodes
                else:
                    self._execute_opcode(opcode)
            
            # Script berhasil jika stack tidak kosong dan top element true
            return (self.execution_success and 
                   len(self.stack) > 0 and 
                   self._cast_to_bool(self.stack[-1]))
                   
        except Exception as e:
            print(f"Script execution error: {e}")
            return False
    
    def _execute_opcode(self, opcode: int):
        """Execute single opcode"""
        try:
            # Constants
            if opcode == 0:  # OP_0, OP_FALSE
                self.stack.append(b'')
                
            elif 81 <= opcode <= 96:  # OP_1 - OP_16
                self.stack.append(bytes([opcode - 80]))
            
            # Stack operations
            elif opcode == 107:  # OP_TOALTSTACK
                if not self.stack:
                    raise ScriptError("OP_TOALTSTACK dengan stack kosong")
                self.altstack.append(self.stack.pop())
                
            elif opcode == 108:  # OP_FROMALTSTACK
                if not self.altstack:
                    raise ScriptError("OP_FROMALTSTACK dengan altstack kosong")
                self.stack.append(self.altstack.pop())
                
            elif opcode == 117:  # OP_DROP
                if not self.stack:
                    raise ScriptError("OP_DROP dengan stack kosong")
                self.stack.pop()
                
            elif opcode == 118:  # OP_DUP
                if not self.stack:
                    raise ScriptError("OP_DUP dengan stack kosong")
                self.stack.append(self.stack[-1])
                
            elif opcode == 169:  # OP_HASH160
                if not self.stack:
                    raise ScriptError("OP_HASH160 dengan stack kosong")
                data = self.stack.pop()
                self.stack.append(CryptoUtils.hash160(data))
                
            elif opcode == 170:  # OP_HASH256
                if not self.stack:
                    raise ScriptError("OP_HASH256 dengan stack kosong")
                data = self.stack.pop()
                self.stack.append(CryptoUtils.double_sha256(data))
            
            # Crypto operations
            elif opcode == 172:  # OP_CHECKSIG (sederhana)
                if len(self.stack) < 2:
                    raise ScriptError("OP_CHECKSIG butuh 2 element di stack")
                
                pubkey = self.stack.pop()
                signature = self.stack.pop()
                
                # Dalam implementasi real, butuh transaction data untuk verifikasi
                # Di sini kita sederhanakan untuk testing
                self.stack.append(b'\x01')  # Always return true untuk testing
                
            elif opcode == 174:  # OP_CHECKMULTISIG (sederhana)
                # Implementasi sederhana untuk testing
                self.stack.append(b'\x01')  # Always return true
                
            # Bitwise logic
            elif opcode == 135:  # OP_EQUAL
                if len(self.stack) < 2:
                    raise ScriptError("OP_EQUAL butuh 2 element di stack")
                
                a = self.stack.pop()
                b = self.stack.pop()
                
                if a == b:
                    self.stack.append(b'\x01')
                else:
                    self.stack.append(b'')
                    
            elif opcode == 136:  # OP_EQUALVERIFY
                if len(self.stack) < 2:
                    raise ScriptError("OP_EQUALVERIFY butuh 2 element di stack")
                
                a = self.stack.pop()
                b = self.stack.pop()
                
                if a != b:
                    raise ScriptError("OP_EQUALVERIFY failed")
            
            # Control operations
            elif opcode == 106:  # OP_RETURN
                self.execution_success = False
                
            else:
                # Opcode tidak dikenali
                raise ScriptError(f"Opcode tidak didukung: {opcode:02x}")
                
        except ScriptError as e:
            self.execution_success = False
            raise e
    
    def _cast_to_bool(self, data: bytes) -> bool:
        """Convert bytes ke boolean (mengikuti aturan Bitpy)"""
        # Bitpy: empty array = false, lainnya true
        # Kecuali: negative zero = false
        if len(data) == 0:
            return False
            
        # Check untuk negative zero
        for i, byte in enumerate(data):
            if byte != 0:
                # Bukan nol - return true
                return True
            if i == len(data) - 1 and byte == 0x80:
                # Negative zero - return false
                return False
                
        return True
    
    # Standard script templates (mengikuti Bitpy standar)

def create_p2pkh_script(pubkey_hash: bytes) -> bytes:
    """
    Create P2PKH (Pay to Public Key Hash) script
    Format: OP_DUP OP_HASH160 <pubkey_hash> OP_EQUALVERIFY OP_CHECKSIG
    """
    script = bytes([0x76, 0xa9])  # OP_DUP, OP_HASH160
    script += ByteUtils.var_int_encode(len(pubkey_hash))
    script += pubkey_hash
    script += bytes([0x88, 0xac])  # OP_EQUALVERIFY, OP_CHECKSIG
    return script

def create_p2sh_script(script_hash: bytes) -> bytes:
    """
    Create P2SH (Pay to Script Hash) script
    Format: OP_HASH160 <script_hash> OP_EQUAL
    """
    script = bytes([0xa9])  # OP_HASH160
    script += ByteUtils.var_int_encode(len(script_hash))
    script += script_hash
    script += bytes([0x87])  # OP_EQUAL
    return script

def create_multisig_script(m: int, pubkeys: List[bytes]) -> bytes:
    """
    Create multisig script
    Format: <m> <pubkeys> <n> OP_CHECKMULTISIG
    """
    if m < 1 or m > 16:
        raise ScriptError("m harus antara 1 dan 16")
    if len(pubkeys) < m or len(pubkeys) > 16:
        raise ScriptError("Jumlah pubkey tidak valid")
        
    script = bytes([80 + m])  # OP_1 hingga OP_16
    
    for pubkey in pubkeys:
        script += ByteUtils.var_int_encode(len(pubkey))
        script += pubkey
        
    script += bytes([80 + len(pubkeys)])  # OP_1 hingga OP_16
    script += bytes([0xae])  # OP_CHECKMULTISIG
    
    return script

def extract_p2pkh_address(script_pubkey: bytes) -> Optional[str]:
    """Extract address dari P2PKH script"""
    # Pattern: OP_DUP OP_HASH160 <20 bytes> OP_EQUALVERIFY OP_CHECKSIG
    if (len(script_pubkey) == 25 and
        script_pubkey[0] == 0x76 and script_pubkey[1] == 0xa9 and
        script_pubkey[2] == 0x14 and script_pubkey[23] == 0x88 and 
        script_pubkey[24] == 0xac):
        
        pubkey_hash = script_pubkey[3:23]
        return CryptoUtils.create_bitpy_address(pubkey_hash)
    
    return None

def extract_p2sh_address(script_pubkey: bytes) -> Optional[str]:
    """Extract address dari P2SH script"""
    # Pattern: OP_HASH160 <20 bytes> OP_EQUAL
    if (len(script_pubkey) == 23 and
        script_pubkey[0] == 0xa9 and script_pubkey[1] == 0x14 and
        script_pubkey[22] == 0x87):
        
        script_hash = script_pubkey[2:22]
        return CryptoUtils.create_bitpy_address(script_hash)
    
    return None

# Test functions
def test_script():
    """Test script functionality"""
    print("Testing Bitpy Script...")
    
    # Test P2PKH script
    pubkey_hash = CryptoUtils.hash160(b'test_public_key')
    script_pubkey = create_p2pkh_script(pubkey_hash)
    
    # Test script execution
    script_engine = Script()
    result = script_engine.execute(script_pubkey)
    
    print(f"P2PKH script test: {result}")
    print(f"P2PKH address: {extract_p2pkh_address(script_pubkey)}")

if __name__ == "__main__":
    test_script()
