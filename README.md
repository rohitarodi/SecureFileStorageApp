$env:AZURE_CLIENT_ID="52a65d7d-1692-47f9-8db6-451a62b7cf96"
$env:AZURE_TENANT_ID="704d822c-358a-4784-9a16-49e20b75f941"
$env:AZURE_CLIENT_SECRET="VXt8Q~BevGR6Ib2PFdt-~6fIXFoWY0cTESt~Lbe1"

Create a App Registration on AAD
Get the Tenant_ID --> Directory Tenant ID

Create a Secret under App the same app
Value = VXt8Q~BevGR6Ib2PFdt-~6fIXFoWY0cTESt~Lbe1
Secret_ID = 636d7732-3617-474f-bf58-84fa74dd08f1
Expiry  3/2/2026

Using the Microsoft Storage Explorer 
Create a Shared Access Signature
Connection String = SharedAccessSignature=sv=2023-01-03&ss=btqf&srt=sco&st=2025-03-03T00%3A30%3A47Z&se=2065-10-14T23%3A30%3A00Z&sp=rwdxftlacup&sig=OsN6%2FLn9ChoS7ja5BI8JhD5CCOdp1BjZCnevNTxXfq4%3D;BlobEndpoint=https://stgsustudentdata001.blob.core.windows.net/;FileEndpoint=https://stgsustudentdata001.file.core.windows.net/;QueueEndpoint=https://stgsustudentdata001.queue.core.windows.net/;TableEndpoint=https://stgsustudentdata001.table.core.windows.net/;

SAS Token = ?sv=2023-01-03&ss=btqf&srt=sco&st=2025-03-03T00%3A30%3A47Z&se=2065-10-14T23%3A30%3A00Z&sp=rwdxftlacup&sig=OsN6%2FLn9ChoS7ja5BI8JhD5CCOdp1BjZCnevNTxXfq4%3D

Using Test.py created a base 32 Encerpytion key