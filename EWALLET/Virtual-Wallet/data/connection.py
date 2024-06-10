from supabase import create_client

# Supabase URL and Key
url = 'https://lcrwokhdqhyvbcjmuedq.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxjcndva2hkcWh5dmJjam11ZWRxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNTg2OTQyMiwiZXhwIjoyMDMxNDQ1NDIyfQ.eiB4kcfN6wbGRKQWrevrpjjCzdf7p3YZrecxSJ6C59g'

# Create Supabase client
query = create_client(url, key)

