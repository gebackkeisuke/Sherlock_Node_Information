import os, sys
import re
import pandas as pd
import subprocess

def split_nodelist(nodelist: str):
    parts = []
    buf = ""
    depth = 0

    for c in nodelist:
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1

        if c == "," and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += c

    if buf:
        parts.append(buf)

    return parts


def expand_nodelist(nodelist: str):
    result = []

    parts = split_nodelist(nodelist)

    for part in parts:
        match = re.match(r"(.+?)\[(.+)\]", part)  

        if not match:
            result.append(part)
            continue

        prefix = match.group(1)
        ranges = match.group(2)

        for r in ranges.split(","):
            if "-" in r:
                start, end = map(int, r.split("-"))
                for i in range(start, end + 1):
                    result.append(f"{prefix}{i:02d}")
            else:
                result.append(f"{prefix}{int(r):02d}")

    return result


def count_nodes(nodelist: str) -> int:
    return len(expand_nodelist(nodelist))

def analyze_sinfo(df):
    """
    inputs
        - Dataframe aqcuired by running 'sinfo -o "%100N %10c %10m %100f"'

    """
    nodelists = df['NODELIST']  
    nodes = []
    for nodelist in nodelists:
        total_nodes = count_nodes(nodelist)
        nodes.append(total_nodes)

    df['TOTAL_NODES'] = nodes  
    df['TOTAL_CPUS'] = nodes * df["CPUS"].astype(float)
    
    def convert_memory_to_gb(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df["MEMORY"] = (
            df["MEMORY"]
            .astype(str)
            .str.replace(r"[+,]", "", regex=True)
        )

        df["MEMORY"] = pd.to_numeric(df["MEMORY"], errors="coerce")
        df["MEMORY[GB/node]"] = df["MEMORY"] / 1024
        df["MEMORY[GB/cpu]"]  = df["MEMORY[GB/node]"] / df["CPUS"].astype(float)
        df["MEMORY[GB/cpu]"]  = df["MEMORY[GB/cpu]"].round(2)
        df["MEMORY[GB/node]"] = df["MEMORY[GB/node]"].round(1)

        return df

    df = convert_memory_to_gb(df)
    
    return df

def parse_scontrol_node(output: str) -> dict:
    data = {}

    for line in output.splitlines():
        if not line.strip():
            continue

        parts = line.strip().split()

        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                data[key] = value

    return data


def nodes_to_dataframe(outputs: list) -> pd.DataFrame:
    """
    複数ノード分の output を DataFrame に変換
    """
    records = [parse_scontrol_node(out) for out in outputs]
    return pd.DataFrame(records)

def run_sinfo():
    command = f'sinfo -o "%100N %10c %10m %100f %P"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    return output

def get_df_sinfo(output):
    lines = output.strip().split("\n")
    rows = [line.split(None, 4) for line in lines]
    df_sinfo = pd.DataFrame(rows[1:], columns=rows[0])
    df_sinfo = analyze_sinfo(df_sinfo)
    return df_sinfo

def run_scontrol(node):
    command = f'scontrol show node {node}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output      = result.stdout
    return output

def gat_available_features(text):
    """
    Split and get available features dictionary
    """
    features = {}

    for item in text.split(","):
        if ":" in item:
            k, v = item.split(":", 1)
            features[k] = v

    return features

def main():
    # Run sinfo to collect data
    output = run_sinfo()    
    
    # Make dataframe which summarized 'sinfo'.
    df_sinfo = get_df_sinfo(output)    
    
    # Run scontrol to get detailed information of each node.
    records = []
    for nodelist in df_sinfo['NODELIST']:
        node        = expand_nodelist(nodelist)[0]
        output      = run_scontrol(node)
        node_info   = parse_scontrol_node(output)
        features    = gat_available_features(node_info['AvailableFeatures'])
        records.append({"NODELIST": nodelist, "NODE(Example)": node, **node_info, **features})
    df_detail =   pd.DataFrame(records)  

    # Combine sinfo and scontrol
    df = df_sinfo.merge(df_detail, on=["NODELIST"], how="left")
    df.to_csv('nodes_information_all.csv')

    # Extract machine specs
    df_extracted = df[[ 'NODE(Example)', 'CLASS', 'PARTITION', 'Partitions',
                        'CPUS', 'TOTAL_NODES', 'TOTAL_CPUS', 'MEMORY[GB/node]', 'MEMORY[GB/cpu]',
                        'CPU_MNF','CPU_GEN','CPU_SKU','CPU_FRQ',
                        # 'GPU_GEN','GPU_BRD','GPU_CC',
                        'GPU_SKU','GPU_MEM',                        
                    ]]
    df_extracted.to_csv('nodes_information_machine_specs.csv')

    # If you need usage, extract some columns...
    # print(df.columns)
    # print(df.head(10))


if __name__ == "__main__":
    main()