async def m001_initial(db):
    """
    Initial tposs table.
    """
    await db.execute(
        """
        CREATE TABLE tpos.tposs (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            currency TEXT NOT NULL
        );
    """
    )
async def m002_on_chain_support(db):
    """
    Add onchainwallet field.
    """
    await db.execute("ALTER TABLE tpos.tposs ADD COLUMN onchainwallet TEXT;")
    