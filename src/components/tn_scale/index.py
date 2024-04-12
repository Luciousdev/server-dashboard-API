import os
import dotenv
from aiotruenas_client import CachingMachine as TrueNASMachine


# Function to be called by the API
async def main(argument):
    try:
        machine = await TrueNASMachine.create(
            os.getenv("TN_HOSTNAME"),
            api_key=os.getenv("TN_API_KEY")
        )

        if argument == "disks":
            data = await get_disks(machine)
            return data
        if argument == "pools":
            data = await get_pools(machine)
            return data
        if argument == "datasets":
            data = await get_datasets(machine, True)
            return data
        return []

    except Exception as e:
        print(f"Error connecting to server: {str(e)}")
        return None


async def get_datasets(machine, isClean):
    try:
        datasets = await machine.get_datasets()
        dataset_info = []

        for dataset in datasets:
            if isClean:
                if dataset.pool_name == "boot-pool" or "iocage" in dataset.id:
                    continue

            dataset_info.append({
                "+ Pool Name": dataset.pool_name,
                "+ Dataset Name": dataset.id,
                "+ Total": format_bytes(dataset.total_bytes),
                "+ Used": format_bytes(dataset.used_bytes),
                "+ Available": format_bytes(dataset.available_bytes)
            })

        return dataset_info
    except Exception as e:
        print(f"Error retrieving datasets: {str(e)}")
        return []


def format_bytes(bytes_value):
    # convert bytes to human-readable format
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    index = 0
    while bytes_value >= 1024 and index < len(units) - 1:
        bytes_value /= 1024.0
        index += 1
    return f"{bytes_value:.2f} {units[index]}"


async def get_disks(machine):
    try:
        disks = await machine.get_disks()
        disk_info = []

        for disk in disks:
            disk_info.append({
                "+ Disk Name": disk.name,
                "+ Disk Size": format_bytes(disk.size),
            })

        return disk_info
    except Exception as e:
        print(f"Error retrieving disks: {str(e)}")
        return []


async def get_pools(machine):
    try:
        pools = await machine.get_pools()
        pool_info = []

        for pool in pools:
            pool_info.append({
                "+ Pool ID": pool.id,
                "+ Pool Name": pool.name,
                "+ Pool Status": str(pool.status)
            })

        return pool_info
    except Exception as e:
        print(f"Error retrieving pools: {str(e)}")
        return []