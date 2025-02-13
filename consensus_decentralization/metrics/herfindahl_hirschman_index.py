def compute_hhi(blocks_per_entity):
    """
    Calculates the Herfindahl-Hirschman index of a distribution of blocks to entities
    From investopedia: The HHI is calculated by squaring the market share of each firm competing in a market and then
    summing the resulting numbers. It can range from close to 0 to 10,000, with lower values indicating a less
    concentrated market. The U.S. Department of Justice considers a market with an HHI of less than 1,500 to be a
    competitive marketplace, an HHI of 1,500 to 2,500 to be a moderately concentrated marketplace,
    and an HHI of 2,500 or greater to be a highly concentrated marketplace.
    :param blocks_per_entity: a dictionary with entities and the blocks they have produced
    :return: float between 0 and 10,000 that represents the HHI of the given distribution or None if the data is empty
    """
    total_blocks = sum(blocks_per_entity.values())
    if total_blocks == 0:
        return None
    return sum([pow(num_blocks / total_blocks * 100, 2) for num_blocks in blocks_per_entity.values()])
