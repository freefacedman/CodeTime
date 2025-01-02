# deploy.ps1

# Define variables
 = """"
 = "".zip""

# Remove existing ZIP if it exists
if (Test-Path ) {
    Remove-Item  -Force
    Write-Host "Removed existing ZIP file: "
}

# Create ZIP archive
Compress-Archive -Path "\*" -DestinationPath 
Write-Host "Created ZIP archive: "

# Optionally, you can add commands to upload the ZIP to a server or cloud storage
# Example: Upload to Azure Blob Storage (requires Azure PowerShell module and credentials)
# Import-Module Az
#  = "yourstorageaccount"
#  = "deployments"
#  = "UltimateInteractiveWebShowcase.zip"
# Set-AzStorageBlobContent -File  -Container  -Blob  -Context (Get-AzStorageAccount -Name ).Context
# Write-Host "Uploaded ZIP to Azure Blob Storage."
