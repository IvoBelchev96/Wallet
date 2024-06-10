from data.connection import query as supabase

def create_card(card_data: dict):
    print("Creating card with data:", card_data)
    response = supabase.table('cards').insert(card_data).execute()
    print("Supabase response:", response)
    if not response.data:
        print("Error creating card:", response)
        raise Exception(response.json())
    return response.data[0]

def get_all_cards():
    response = supabase.table('cards').select('*').execute()
    if not response.data:
        print("Error fetching cards:", response)
        raise Exception(response.json())
    return response.data

def get_card_by_id(card_id: int):
    response = supabase.table('cards').select('*').eq('id', card_id).execute()
    if not response.data:
        print("Error fetching card by id:", response)
        raise Exception(response.json())
    data = response.data
    return data[0] if data else None

def update_card(card_id: int, card_data: dict):
    print("Updating card with id:", card_id, "with data:", card_data)
    response = supabase.table('cards').update(card_data).eq('id', card_id).execute()
    print("Supabase response:", response)
    if not response.data:
        print("Error updating card:", response)
        raise Exception(response.json())
    return response.data[0]

def delete_card(card_id: int):
    print("Deleting card with id:", card_id)
    response = supabase.table('cards').delete().eq('id', card_id).execute()
    print("Supabase response:", response)
    if not response.data:
        print("Error deleting card:", response)
        raise Exception(response.json())
    return response.data[0] if response.data else None
