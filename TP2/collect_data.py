#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import time
from tqdm import tqdm

class RepositoriumCollector:
    def __init__(self):
        self.base_url = "https://repositorium.sdum.uminho.pt/oai/oai"
        self.output_dir = Path("data")
        self.output_dir.mkdir(exist_ok=True)
        
    def collect_data(self, collection="col_1822_21316", batch_size=100, max_records=1000):
        """
        Collect data from RepositoriUM using OAI-PMH protocol
        
        Args:
            collection (str): Collection identifier
            batch_size (int): Number of records per request
            max_records (int): Maximum number of records to collect
        """
        xml_file = self.output_dir / f"{collection}_data.xml"
        
        # Initialize XML structure
        root = ET.Element("repository")
        tree = ET.ElementTree(root)
        
        offset = 0
        total_records = 0
        pbar = tqdm(total=max_records, desc="Collecting records")
        
        while total_records < max_records:
            params = {
                "verb": "ListRecords",
                "resumptionToken": f"dim///{collection}/{offset}"
            }
            
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                
                if "noRecordsMatch" in response.text:
                    print(f"\nNo more records found after {total_records} records.")
                    break
                
                # Parsing response XML
                response_root = ET.fromstring(response.text)
                records = response_root.findall(".//{http://www.openarchives.org/OAI/2.0/}record")
                
                if not records:
                    break
                
                # Adding records to XML
                for record in records:
                    root.append(record)
                    total_records += 1
                    pbar.update(1)
                    
                    if total_records >= max_records:
                        break
                
                offset += batch_size
                time.sleep(1)  # I'm being nice to the server :3
                
            except requests.exceptions.RequestException as e:
                print(f"\nError during collection: {e}")
                break
                
        pbar.close()
        
        # Saving the collected data
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)
        print(f"\nData collection completed. Saved {total_records} records to {xml_file}")

if __name__ == "__main__":
    collector = RepositoriumCollector()
    collector.collect_data()
