# Required libraries
import pandas as pd

# Load the catalog (assumes whitespace-delimited fixed-width format)
catalog_url = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/478/1520/table2.dat"

# Read the catalog with predefined columns
columns = ['Name', 'RA', 'Dec', 'Dist', 'Mass', 'MLv', 'Rc', 'Rh', 'Rlim', 'sigma0']
df = pd.read_csv(catalog_url, delim_whitespace=True, comment='#', names=columns)
# Clean up the cluster names by removing any non-alphanumeric characters (such as asterisks)
df['Name'] = df['Name'].str.replace(r'[^\w\s]', '', regex=True).str.strip().str.upper()

# Print available clusters for inspection
print("Available Clusters:")
print(df['Name'].head(20))  # Display first 20 clusters

# Estimate the number of stars in a selected cluster
def estimate_star_count(cluster_name, avg_mass=0.5):
    # Clean the input name and standardize to uppercase
    cluster_name = cluster_name.strip().upper()

    # Find cluster by name (case-insensitive search)
    cluster = df[df['Name'].str.contains(cluster_name, case=False, na=False)]

    if not cluster.empty:
        cluster = cluster.iloc[0]  # Take the first match
        total_mass = cluster['Mass']  # in solar masses
        n_stars = total_mass / avg_mass  # Estimate stars assuming avg_mass per star
        print(f"Cluster: {cluster['Name']}")
        print(f"Estimated total mass: {total_mass:.2e} M_sun")
        print(f"Assumed average stellar mass: {avg_mass} M_sun")
        print(f"Estimated number of stars: {n_stars:.2e}")
    else:
        print(f"Cluster '{cluster_name}' not found. Please check the name.")

# Try the example with NGC 104 (47 Tucanae)
estimate_star_count("NGC 104")  # 47 Tucanae
