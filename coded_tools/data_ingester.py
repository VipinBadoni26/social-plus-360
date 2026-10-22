import pandas as pd
from neuro_san.interfaces.coded_tool import CodedTool

class DataIngesterTool(CodedTool):
    def invoke(self, args: dict, sly_data: dict) -> dict:
        file_path = args.get("file_path", "data/social_posts.csv")
        df = pd.read_csv(file_path)
        
        # Filter spam
        clean_df = df[~df['text'].str.contains('BUY CHEAP|crypto', case=False, na=False)]
        
        formatted_posts = []
        secure_pii_store = {}
        
        for _, row in clean_df.iterrows():
            post_id = str(row['id'])
            
            # Secure handle metadata in sly_data
            secure_pii_store[post_id] = {
                "handle": row['handle'],
                "name": row['@user']
            }
            
            # Pass only clean text downstream
            formatted_posts.append({
                "post_id": post_id,
                "text": row['text']
            })
            
        sly_data["secure_user_mapping"] = secure_pii_store
        sly_data["active_posts"] = formatted_posts
        
        return {
            "status": "success", 
            "ingested_count": len(formatted_posts),
            "summary": f"Ingested {len(formatted_posts)} posts cleanly into sly_data channel."
        }