import dframe as df

def initialize_database():
    print("Initializing database with new parties...")
    
    # Reset the candidate list with new parties
    df.reset_cand_list()
    
    print("Database initialized successfully!")
    print("New parties: BJP, Congress, DMK, ADMK, TVK, NOTA")

if __name__ == "__main__":
    initialize_database()