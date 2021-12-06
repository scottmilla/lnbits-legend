from typing import List, Optional, Union
from quart import jsonify
from lnbits.helpers import urlsafe_short_hash
import httpx
from . import db
from .models import TPoS
from http import HTTPStatus


async def create_tpos(*, wallet_id: str, name: str, currency: str, onchainwallet: str) -> TPoS:
    tpos_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO tpos.tposs (id, wallet, name, currency, onchainwallet)
        VALUES (?, ?, ?, ?, ?)
        """,
        (tpos_id, wallet_id, name, currency, onchainwallet),
    )

    tpos = await get_tpos(tpos_id)
    assert tpos, "Newly created tpos couldn't be retrieved"
    return tpos


async def get_tpos(tpos_id: str) -> Optional[TPoS]:
    row = await db.fetchone("SELECT * FROM tpos.tposs WHERE id = ?", (tpos_id,))
    return TPoS.from_row(row) if row else None


async def get_tposs(wallet_ids: Union[str, List[str]]) -> List[TPoS]:
    if isinstance(wallet_ids, str):
        wallet_ids = [wallet_ids]

    q = ",".join(["?"] * len(wallet_ids))
    rows = await db.fetchall(
        f"SELECT * FROM tpos.tposs WHERE wallet IN ({q})", (*wallet_ids,)
    )

    return [TPoS.from_row(row) for row in rows]


async def delete_tpos(tpos_id: str) -> None:
    await db.execute("DELETE FROM tpos.tposs WHERE id = ?", (tpos_id,))

# async def check_address_txs(onchainaddress: str, amount: int):

#     async with httpx.AsyncClient() as client:
#         r = await client.get(
#             "https://mempool.space/api/address/" + onchainaddress 
#         )
#         if r.json()['mempool_stats']['funded_txo_count'] > 1:
#             respAmount = r.json()['mempool_stats']['funded_txo_sum']
#             if respAmount >= amount:
#                 return jsonify({"paid": True}), HTTPStatus.OK
#             else:
#                 return jsonify({"paid": False}), HTTPStatus.OK
#         else:
#             return jsonify(r), HTTPStatus.OK

