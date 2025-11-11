import pandas as pd
from pathlib import Path
import os

# path = Path("C:/Users/Desktop/Sem-5/CS301 CN/Project/Voting/database")
path = Path("database")

# Ensure database directory exists
path.mkdir(exist_ok=True)

def initialize_candidate_list():
    """Initialize candidate list with new parties if it doesn't exist"""
    cand_file = path / 'cand_list.csv'
    if not cand_file.exists():
        reset_cand_list()
        print("Candidate list initialized with new parties")

def count_reset():
    try:
        df = pd.read_csv(path/'voterList.csv')
        # Use .loc to avoid chained assignment
        df.loc[:, 'hasVoted'] = 0
        df.to_csv(path/'voterList.csv', index=False)

        df = pd.read_csv(path/'cand_list.csv')
        # Use .loc to avoid chained assignment
        df.loc[:, 'Vote Count'] = 0
        df.to_csv(path/'cand_list.csv', index=False)
        print("Vote counts reset successfully")
    except Exception as e:
        print(f"Error in count_reset: {e}")

def reset_voter_list():
    try:
        df = pd.DataFrame(columns=['voter_id','Name','Gender','Zone','City','Passw','hasVoted'])
        df = df[['voter_id','Name','Gender','Zone','City','Passw','hasVoted']]
        df.to_csv(path/'voterList.csv', index=False)
        print("Voter list reset successfully")
    except Exception as e:
        print(f"Error in reset_voter_list: {e}")

def reset_cand_list():
    try:
        # Updated with new parties: DMK, ADMK, TVK instead of AAP and Shiv Sena
        df = pd.DataFrame({
            'Sign': ['bjp', 'cong', 'dmk', 'admk', 'tvk', 'nota'],
            'Name': ['BJP', 'Congress', 'DMK', 'ADMK', 'TVK', 'NOTA'],
            'Vote Count': [0, 0, 0, 0, 0, 0]
        })
        df = df[['Sign','Name','Vote Count']]
        df.to_csv(path/'cand_list.csv', index=False)
        print("Candidate list reset with new parties")
    except Exception as e:
        print(f"Error in reset_cand_list: {e}")

def verify(vid,passw):
    # Initialize candidate list on first run
    initialize_candidate_list()
    
    try:
        df = pd.read_csv(path/'voterList.csv')
        # Use vectorized operations instead of looping
        matching_voter = df[(df['voter_id'] == vid) & (df['Passw'] == passw)]
        return len(matching_voter) > 0
    except Exception as e:
        print(f"Error in verify: {e}")
        return False

def isEligible(vid):
    try:
        df = pd.read_csv(path/'voterList.csv')
        # Use vectorized operations instead of looping
        matching_voter = df[(df['voter_id'] == vid) & (df['hasVoted'] == 0)]
        return len(matching_voter) > 0
    except Exception as e:
        print(f"Error in isEligible: {e}")
        return False

def vote_update(st, vid):
    if isEligible(vid):
        try:
            # Update candidate vote count using .loc
            df_cand = pd.read_csv(path/'cand_list.csv')
            mask_cand = df_cand['Sign'] == st
            if mask_cand.any():
                df_cand.loc[mask_cand, 'Vote Count'] += 1
                df_cand.to_csv(path/'cand_list.csv', index=False)

            # Update voter's hasVoted status using .loc
            df_voter = pd.read_csv(path/'voterList.csv')
            mask_voter = df_voter['voter_id'] == vid
            if mask_voter.any():
                df_voter.loc[mask_voter, 'hasVoted'] = 1
                df_voter.to_csv(path/'voterList.csv', index=False)
                
            return True
        except Exception as e:
            print(f"Error in vote_update: {e}")
            return False
    return False

def show_result():
    # Initialize candidate list on first run
    initialize_candidate_list()
    
    try:
        df = pd.read_csv(path/'cand_list.csv')
        v_cnt = {}
        for index, row in df.iterrows():
            v_cnt[df['Sign'].iloc[index]] = df['Vote Count'].iloc[index]
        return v_cnt
    except Exception as e:
        print(f"Error in show_result: {e}")
        return {}

def taking_data_voter(name, gender, zone, city, passw):
    print(f"DEBUG: taking_data_voter called with: {name}, {gender}, {zone}, {city}, {passw}")
    
    # Initialize candidate list on first run
    initialize_candidate_list()
    
    try:
        # Check if voterList.csv exists, if not create it
        voter_file = path / 'voterList.csv'
        
        if not voter_file.exists():
            print("DEBUG: voterList.csv does not exist, creating new file")
            # Create new DataFrame with the first voter
            vid = 10001
            df = pd.DataFrame({
                "voter_id": [vid],
                "Name": [name],
                "Gender": [gender],
                "Zone": [zone],
                "City": [city],
                "Passw": [passw],
                "hasVoted": [0]
            })
        else:
            print("DEBUG: voterList.csv exists, reading file")
            # Read existing file
            df = pd.read_csv(voter_file)
            
            # Check if dataframe is empty
            if df.empty:
                print("DEBUG: DataFrame is empty, creating first voter")
                vid = 10001
                new_voter = pd.DataFrame({
                    "voter_id": [vid],
                    "Name": [name],
                    "Gender": [gender],
                    "Zone": [zone],
                    "City": [city],
                    "Passw": [passw],
                    "hasVoted": [0]
                })
                df = new_voter
            else:
                print(f"DEBUG: DataFrame has {len(df)} rows, last voter_id: {df['voter_id'].iloc[-1] if 'voter_id' in df.columns else 'N/A'}")
                # Get the last voter ID and increment
                if 'voter_id' in df.columns and not df.empty:
                    vid = df['voter_id'].iloc[-1] + 1
                else:
                    vid = 10001
                
                # Create new voter data
                new_voter = pd.DataFrame({
                    "voter_id": [vid],
                    "Name": [name],
                    "Gender": [gender],
                    "Zone": [zone],
                    "City": [city],
                    "Passw": [passw],
                    "hasVoted": [0]
                })
                
                # Append new voter to existing dataframe
                df = pd.concat([df, new_voter], ignore_index=True)

        # Save to CSV
        df.to_csv(voter_file, index=False)
        print(f"DEBUG: Successfully saved voter with ID: {vid}")
        print(f"DEBUG: File saved at: {voter_file.absolute()}")
        
        return vid
        
    except Exception as e:
        print(f"ERROR in taking_data_voter: {e}")
        return -1

# Initialize on import
initialize_candidate_list()

# Test function to check database
def test_database():
    print("=== DATABASE TEST ===")
    print(f"Database path: {path.absolute()}")
    print(f"Voter list exists: {(path/'voterList.csv').exists()}")
    print(f"Candidate list exists: {(path/'cand_list.csv').exists()}")
    
    if (path/'voterList.csv').exists():
        try:
            df = pd.read_csv(path/'voterList.csv')
            print(f"Voter list rows: {len(df)}")
            print(f"Voter list columns: {df.columns.tolist()}")
            if not df.empty:
                print("First few rows:")
                print(df.head())
        except Exception as e:
            print(f"Error reading voter list: {e}")
    
    if (path/'cand_list.csv').exists():
        try:
            df = pd.read_csv(path/'cand_list.csv')
            print(f"Candidate list rows: {len(df)}")
            print("Candidate list:")
            print(df)
        except Exception as e:
            print(f"Error reading candidate list: {e}")

# Run test if this file is executed directly
if __name__ == "__main__":
    test_database()