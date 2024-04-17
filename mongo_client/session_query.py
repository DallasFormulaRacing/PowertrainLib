from pymongo import MongoClient
import pprint
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client['cluster0']
collection = db['realtime_metrics']

def get_session_time_range(session_id):
    session_documents = collection.find({'metadata.session_id': session_id}).sort('timestamp', 1)
    session_documents_list = list(session_documents)

    if len(session_documents_list) == 0:
        return None, None
    elif len(session_documents_list) == 1:
        doc = session_documents_list[0]
        return doc['timestamp'], doc['timestamp']
    else:
        first_doc = session_documents_list[0]
        last_doc = session_documents_list[-1]
        start_time = first_doc['timestamp']
        end_time = last_doc['timestamp']
        return start_time, end_time

def get_session_documents(session_id, start_time, end_time):
    session_documents = collection.find({
        'metadata.session_id': session_id,
        'timestamp': {'$gte': start_time, '$lte': end_time}
    })
    return list(session_documents)

# Test the query
def main():
    printer = pprint.PrettyPrinter()
    session_id = "102"
    start_time, end_time = get_session_time_range(session_id)

    if start_time is not None and end_time is not None:
        session_documents = get_session_documents(session_id, start_time, end_time)
        for doc in session_documents:
            printer.pprint(doc)
    else:
        print("No documents found for the provided session ID.")


if __name__ == '__main__':
    main()