from collections import defaultdict
from src.helpers.helper import get_pool_data, write_blocks_per_entity_to_file, get_pool_addresses
from src.mappings.mapping import Mapping


class CardanoMapping(Mapping):

    def __init__(self, project_name, dataset):
        super().__init__(project_name, dataset)

    def process(self, timeframe):
        pool_data, pool_links = get_pool_data(self.project_name, timeframe)

        data = [tx for tx in self.dataset if tx['timestamp'][:len(timeframe)] == timeframe]

        daily_helper_data = {}
        blocks_per_entity = defaultdict(int)
        for tx in data:
            day = tx['timestamp'][:10]
            try:
                pool_data = daily_helper_data[day]['pool_data']
                pool_links = daily_helper_data[day]['pool_links']
                pool_addresses = daily_helper_data[day]['pool_addresses']
            except KeyError:
                pool_data, pool_links = get_pool_data(self.project_name, day)
                pool_addresses = get_pool_addresses(self.project_name, day)
                daily_helper_data[day] = {}
                daily_helper_data[day]['pool_data'] = pool_data
                daily_helper_data[day]['pool_links'] = pool_links
                daily_helper_data[day]['pool_addresses'] = pool_addresses

            entity = tx['coinbase_param']
            if entity:
                if entity in pool_links.keys():
                    entity = pool_links[entity]
                elif entity in pool_data['coinbase_tags'].keys():
                    entity = pool_data['coinbase_tags'][entity]['name']
            else:
                pool = tx['coinbase_addresses']
                if pool:
                    entity = pool
                else:
                    entity = '[!] IOG (core nodes pre-decentralization)'

            blocks_per_entity[entity.replace(',', '')] += 1

        write_blocks_per_entity_to_file(self.io_dir, blocks_per_entity, timeframe)

        return blocks_per_entity
