import requests

class BelibAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, limit=20):
        try:
            response = requests.get(self.api_url, params={'limit': limit})
            if response.status_code == 200:
                json_data = response.json()
                total_records = json_data.get('total', None)
                return json_data, total_records
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None

def main():
    api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/belib-points-de-recharge-pour-vehicules-electriques-disponibilite-temps-reel/records"
    client = BelibAPIClient(api_url)
    data, total_records = client.fetch_data()
    if data:
        print("Data fetched successfully:")
        print(data)
        if total_records is not None:
            print(f"Total records: {total_records}")
        else:
            print("Total records count not available.")
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()
