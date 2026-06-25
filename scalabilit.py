```python id="q4nv71"
from web3 import Web3
from datetime import datetime
import json
import uuid


class ProjectConfig:

    def __init__(self):
        self.rpc_url = "https://mainnet.base.org"
        self.chain_id = 8453

        self.labels = {
            "network": "worldchain",
            "action": "connect",
            "domain": "galaxy",
            "resource": "supply"
        }


class TransactionSession:

    def __init__(
        self,
        private_key,
        contract_address
    ):
        self.config = ProjectConfig()

        self.web3 = Web3(
            Web3.HTTPProvider(
                self.config.rpc_url
            )
        )

        self.private_key = private_key

        self.account = (
            self.web3.eth.account.from_key(
                private_key
            )
        )

        self.contract_address = (
            Web3.to_checksum_address(
                contract_address
            )
        )

    def is_ready(self):

        return self.web3.is_connected()

    def wallet(self):

        return self.account.address

    def nonce(self):

        return (
            self.web3.eth.get_transaction_count(
                self.account.address
            )
        )

    def gas_price(self):

        return self.web3.eth.gas_price

    def build_metadata(self):

        return {
            "id": str(uuid.uuid4()),
            "created": (
                datetime.utcnow().isoformat()
            ),
            "connect": (
                self.config.labels["action"]
            ),
            "worldchain": (
                self.config.labels["network"]
            ),
            "galaxy": (
                self.config.labels["domain"]
            ),
            "supply": (
                self.config.labels["resource"]
            )
        }

    def encode_metadata(self):

        payload = json.dumps(
            self.build_metadata()
        ).encode()

        return "0x" + payload.hex()

    def create_transaction(self):

        return {
            "to": self.contract_address,
            "value": 0,
            "gas": 170000,
            "gasPrice": self.gas_price(),
            "nonce": self.nonce(),
            "chainId": self.config.chain_id,
            "data": self.encode_metadata()
        }

    def sign(self, transaction):

        return (
            self.web3.eth.account.sign_transaction(
                transaction,
                self.private_key
            )
        )

    def report(self, signed_tx):

        return {
            "wallet": self.wallet(),
            "network": (
                self.config.labels["network"]
            ),
            "operation": (
                self.config.labels["action"]
            ),
            "environment": (
                self.config.labels["domain"]
            ),
            "resource": (
                self.config.labels["resource"]
            ),
            "hash": (
                signed_tx.hash.hex()
            )
        }


def print_header():

    print("=" * 50)
    print("Blockchain Interaction Signer")
    print("=" * 50)


def create_session():

    private_key = (
        "YOUR_PRIVATE_KEY"
    )

    contract_address = (
        "0x1234567890123456789012345678901234567890"
    )

    return TransactionSession(
        private_key,
        contract_address
    )


def display_report(data):

    print(
        json.dumps(
            data,
            indent=2
        )
    )


def main():

    print_header()

    session = create_session()

    if not session.is_ready():
        raise RuntimeError(
            "Unable to connect to RPC endpoint"
        )

    transaction = (
        session.create_transaction()
    )

    signed_tx = (
        session.sign(
            transaction
        )
    )

    report = (
        session.report(
            signed_tx
        )
    )

    display_report(
        report
    )

    print()
    print(
        "connect process completed"
    )

    print(
        "worldchain environment active"
    )
