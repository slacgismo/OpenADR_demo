from .create_agents import convert_csv_to_pandas, BATTERY_BRANDS, Device_Type
import pandas as pd
from .create_agents import guid
import random
import os
import json
import csv
import logging


def parse_batteries_csv_file_to_json(
    path: str,
    battery_file: str,
    num_rows: int,
    batter_brands: str
):
    """Parse the battery csv file and return a list of battery token
    "Item1": {
        "serial": {
            "S": "66354"
        },
        "token": {
            "S": "12321321qsd"
        }
    },
    """
    battery_df = convert_csv_to_pandas(file=battery_file, path=path)
    battery_token_list = battery_df["battery_token"][:num_rows].tolist()
    battery_sn_list = battery_df["battery_sn"][:num_rows].tolist()
    battery_brand_list = battery_df["device_brand"][:num_rows].tolist()
    batteries_json = {}
    if len(battery_token_list) < num_rows:
        raise Exception("battery_token_list is not enough")
    # loop through the battery token list and create a json file
    # for index, sen in battery_sn_list:
    for index, sn in enumerate(battery_sn_list):
        if sn == "null":
            raise Exception("battery_sn is null")
        batteries_json[f'Item{index}'] = {

            "token": {"S": battery_token_list[index]},
            "serial": {"S": str(battery_sn_list[index])}
        }
    # save battery to json file
    with (open(f"{path}/batteries.json", "w")) as f:
        json.dump(batteries_json, f, indent=4)
    logging.info(f"=== Create {path}/batteries.json ===")


def convert_df_to_josn_file(
    df: pd.DataFrame,
    json_file_path: str,

):
    logging.info(f"=== Create {json_file_path} ===")
    # convert df to json
    new_index = [i for i in range(len(df))]
    df.index = new_index
    json_data = df.to_json(orient='index')
    json_dict = json.loads(json_data)

#    create a new list to store the modified data
    new_dict = {}
    # iterate over the original JSON data and create a new dictionary with modified index
    for i, v in enumerate(json_dict.values()):

        new_dict[f"Item{i+1}"] = {}
        for k, val in v.items():
            if isinstance(val, (int, float)):
                new_dict[f"Item{i+1}"][k] = {"N": str(val)}
            else:
                new_dict[f"Item{i+1}"][k] = {"S": str(val)}

    # write the modified data to a JSON file
    with open(json_file_path, 'w') as f:
        json.dump(new_dict, f)


def create_batter_json(
    match_device_ids: list,
    num_rows: int = 100,
    path: str = "./simulation_data_files",
    batter_brands: str = BATTERY_BRANDS.SONNEN_BATTERY.value,
    battery_file: str = "simluated_battery.csv",
):

    header = ['device_id', 'device_name',
              'battery_token', 'battery_sn', 'device_brand']
    if len(match_device_ids) < num_rows:
        raise Exception("device_id_list is not enough")
    # Generate data for each row
    rows = []
    for i in range(num_rows):
        row = [
            match_device_ids[i],
            "battery_" + str(i),
            guid(),  # Generate random UUID v4 for battery_token
            # Generate 5-digit random number for battery_sn
            str(random.randint(10000, 99999)),
            batter_brands  # Set device_brand to "Tesla"
        ]
        rows.append(row)
    saved_battery_csv_file = os.path.join(path, battery_file)
    if not os.path.exists(path):
        os.makedirs(path)
    # Write the data to a CSV file
    with open(saved_battery_csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)
    logging.info(f"=== Create {saved_battery_csv_file} ===")


def filter_and_convert_csv_to_json(
    devices_type: list[str],
    num_rows: int = 100,
    path: str = "./simulation_data_files",
    batter_brands: str = BATTERY_BRANDS.SONNEN_BATTERY.value,
    battery_file: str = "simluated_battery.csv",
):

    # read csv file
    # meters_table_df = convert_csv_to_pandas(
    #     file="dump_meters.csv", path="./simulation_data_files")
    # select the devices that are battery
    devices_table_df = convert_csv_to_pandas(
        file="dump_devices.csv", path="./simulation_data_files")

    # filter the devices df
    filter_device_df = pd.DataFrame()
    for device_type in devices_type:
        filter_device_df = devices_table_df[devices_table_df["device_type"]
                                            == device_type]

    # create filter device table json
    convert_df_to_josn_file(
        df=filter_device_df,
        json_file_path="./simulation_data_files/dump_devices.json",
    )

    filter_ES_device_ids = filter_device_df[filter_device_df["device_type"]
                                            == Device_Type.ES.value]["device_id"][:num_rows].tolist()
    create_batter_json(
        match_device_ids=filter_ES_device_ids,
        num_rows=num_rows,
        path=path,
        batter_brands=batter_brands,
        battery_file=battery_file,
    )
    parse_batteries_csv_file_to_json(
        path=path,
        battery_file=battery_file,
        num_rows=num_rows,
        batter_brands=batter_brands,
    )
    # conver order csv to order df
    # filter_order_df = pd.DataFrame()
    orders_table_df = convert_csv_to_pandas(
        file="dump_orders.csv", path="./simulation_data_files")
    filter_orders_df = orders_table_df[orders_table_df["device_id"].isin(
        filter_ES_device_ids)]
    filter_orders_ids = filter_orders_df['order_id'].tolist()
    # create filter orders table json

    convert_df_to_josn_file(
        df=filter_orders_df,
        json_file_path="./simulation_data_files/dump_orders.json",
    )

    # create filter dispatch table json
    # get filer

    dispatches_table_df = convert_csv_to_pandas(
        file="dump_dispatches.csv", path="./simulation_data_files")
    filter_dispatches_df = dispatches_table_df[dispatches_table_df["order_id"].isin(
        filter_orders_ids)]
    # create filter orders table json

    convert_df_to_josn_file(
        df=filter_dispatches_df,
        json_file_path="./simulation_data_files/dump_dispatches.json",
    )
