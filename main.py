import requests
import json
import time
import random
from web3 import Web3
from eth_account import Account
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OKXTradingArenaBot:
    def __init__(self):
        self.session = requests.Session()
        self.ref_code = "KVOLFF"
        self.base_url = "https://web3.okx.com"
        self.event_url = "/id/trading-arena/aspecta"
        
        # Headers untuk request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://web3.okx.com',
            'Referer': f'https://web3.okx.com{self.event_url}?source=cryptoverse_tradingarena'
        }
    
    def load_accounts(self, filename='account.txt'):
        """Load private keys from file"""
        try:
            with open(filename, 'r') as f:
                private_keys = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(private_keys)} accounts from {filename}")
            return private_keys
        except FileNotFoundError:
            logger.error(f"File {filename} not found!")
            return []
    
    def get_wallet_address(self, private_key):
        """Get wallet address from private key"""
        try:
            account = Account.from_key(private_key)
            return account.address
        except Exception as e:
            logger.error(f"Error getting address from private key: {e}")
            return None
    
    def register_for_event(self, private_key):
        """Register wallet for Trading Arena event"""
        try:
            wallet_address = self.get_wallet_address(private_key)
            if not wallet_address:
                return False
            
            logger.info(f"Registering wallet: {wallet_address}")
            
            # Payload untuk registrasi
            payload = {
                "walletAddress": wallet_address,
                "referralCode": self.ref_code,
                "eventType": "aspecta",
                "source": "cryptoverse_tradingarena"
            }
            
            # Request registrasi
            response = self.session.post(
                f"{self.base_url}/api/v1/trading-arena/register",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    logger.info(f"✅ Successfully registered: {wallet_address}")
                    return True
                else:
                    logger.warning(f"❌ Registration failed for {wallet_address}: {result.get('message', 'Unknown error')}")
            else:
                logger.error(f"❌ HTTP Error {response.status_code} for {wallet_address}")
            
            return False
            
        except Exception as e:
            logger.error(f"Error registering wallet: {e}")
            return False
    
    def run_registration(self):
        """Main function to run registration for all accounts"""
        private_keys = self.load_accounts()
        
        if not private_keys:
            logger.error("No private keys found!")
            return
        
        successful_registrations = 0
        failed_registrations = 0
        
        for i, private_key in enumerate(private_keys, 1):
            logger.info(f"Processing account {i}/{len(private_keys)}")
            
            if self.register_for_event(private_key):
                successful_registrations += 1
            else:
                failed_registrations += 1
            
            # Random delay between requests
            if i < len(private_keys):
                delay = random.uniform(2, 5)
                logger.info(f"Waiting {delay:.1f} seconds before next registration...")
                time.sleep(delay)
        
        # Summary
        logger.info("="*50)
        logger.info("REGISTRATION SUMMARY")
        logger.info(f"Total accounts processed: {len(private_keys)}")
        logger.info(f"Successful registrations: {successful_registrations}")
        logger.info(f"Failed registrations: {failed_registrations}")
        logger.info("="*50)

def main():
    bot = OKXTradingArenaBot()
    bot.run_registration()

if __name__ == "__main__":
    main()
