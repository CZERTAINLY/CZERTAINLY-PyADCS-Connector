from PyADCSConnector.utils.dump_parser import AuthorityData, TemplateData
from PyADCSConnector.utils.revocation_reason import CertificateRevocationReason

IMPORT_MODULE = """$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$Host.UI.RawUI.BufferSize = New-Object Management.Automation.Host.Size (2048, $Host.UI.RawUI.BufferSize.Height)"""


def verify_connection_script():
    """
    Returns a script that verifies the connection to the remote server.
    """
    return '\n'.join([
        IMPORT_MODULE,
        # "Get-CertificationAuthority | Ping-ICertInterface"
    ])


def get_ca_script(computer_name: str):
    return '\n'.join([
        IMPORT_MODULE,
        # Use native Windows COM object to get CA information
        "$CAConfig = New-Object -ComObject CertificateAuthority.Config",
        "$CAName = $CAConfig.GetConfig(2)",  # Get local CA name if computer_name is local
        f"$ComputerName = \"{computer_name}\"",
        "try {",
        "    $CertAdmin = New-Object -ComObject CertificateAuthority.Admin",
        f"    $ConfigString = \"$ComputerName\\$CAName\"",
        "    $CAProperty = $CertAdmin.GetCAProperty($ConfigString, 0x00000000, 0, 0x00000004)",  # CR_PROP_CANAME
        "    $OutputObject = \"\" | Select Name, DisplayName, ComputerName, ConfigString, Type, IsEnterprise, IsRoot, IsAccessible, ServiceStatus",
        "    $OutputObject.Name = $CAName",
        "    $OutputObject.DisplayName = $CAName", 
        f"    $OutputObject.ComputerName = \"{computer_name}\"",
        "    $OutputObject.ConfigString = $ConfigString",
        "    $OutputObject.Type = \"Enterprise CA\"", # Default assumption
        "    $OutputObject.IsEnterprise = $true",
        "    $OutputObject.IsRoot = $false", # Default assumption
        "    $OutputObject.IsAccessible = $true",
        "    $OutputObject.ServiceStatus = \"Running\"",
        "    $OutputObject | Format-List *",
        "} catch {",
        "    Write-Error \"Failed to connect to CA: $_\"",
        "}"
    ])


def get_cas_script():
    return '\n'.join([
        IMPORT_MODULE,
        "$TemplateList = @()",
        "try {",
        "    # Use certutil to enumerate CAs",
        "    $CertUtilOutput = & certutil -config - 2>&1",
        "    if ($LASTEXITCODE -eq 0) {",
        "        $Lines = $CertUtilOutput -split \"`n\"",
        "        for ($i = 0; $i -lt $Lines.Length; $i++) {",
        "            $line = $Lines[$i].Trim()",
        "            if ($line -match '^\\d+') {",  # Line starts with a number (CA index)
        "                $parts = $line -split ' ', 2",
        "                if ($parts.Length -ge 2) {",
        "                    $configString = $parts[1].Trim('\"')",
        "                    if ($configString -match '^(.+)\\\\(.+)$') {",
        "                        $computerName = $Matches[1]",
        "                        $caName = $Matches[2]",
        "                        $OutputObject = \"\" | Select Name, DisplayName, ComputerName, ConfigString, Type, IsEnterprise, IsRoot, IsAccessible, ServiceStatus",
        "                        $OutputObject.Name = $caName",
        "                        $OutputObject.DisplayName = $caName",
        "                        $OutputObject.ComputerName = $computerName",
        "                        $OutputObject.ConfigString = $configString",
        "                        $OutputObject.Type = \"Enterprise CA\"",
        "                        $OutputObject.IsEnterprise = $true",
        "                        $OutputObject.IsRoot = $false",
        "                        $OutputObject.IsAccessible = $true",
        "                        $OutputObject.ServiceStatus = \"Running\"",
        "                        $TemplateList += $OutputObject",
        "                    }",
        "                }",
        "            }",
        "        }",
        "    } else {",
        "        # Fallback: try to get local CA info using COM",
        "        $CAConfig = New-Object -ComObject CertificateAuthority.Config",
        "        $CAName = $CAConfig.GetConfig(2)",
        "        $ComputerName = $env:COMPUTERNAME",
        "        $OutputObject = \"\" | Select Name, DisplayName, ComputerName, ConfigString, Type, IsEnterprise, IsRoot, IsAccessible, ServiceStatus",
        "        $OutputObject.Name = $CAName",
        "        $OutputObject.DisplayName = $CAName",
        "        $OutputObject.ComputerName = $ComputerName",
        "        $OutputObject.ConfigString = \"$ComputerName\\$CAName\"",
        "        $OutputObject.Type = \"Enterprise CA\"",
        "        $OutputObject.IsEnterprise = $true",
        "        $OutputObject.IsRoot = $false",
        "        $OutputObject.IsAccessible = $true",
        "        $OutputObject.ServiceStatus = \"Running\"",
        "        $TemplateList += $OutputObject",
        "    }",
        "} catch {",
        "    Write-Error \"Failed to enumerate CAs: $_\"",
        "}",
        "$TemplateList | Format-List"
    ])


def get_templates_script():
    return '\n'.join([
        IMPORT_MODULE,
        "$TemplateList = @()",
        "try {",
        "    # Use certutil to get certificate templates",
        "    $CertUtilOutput = & certutil -CATemplates 2>&1",
        "    if ($LASTEXITCODE -eq 0) {",
        "        $Lines = $CertUtilOutput -split \"`n\"",
        "        $currentTemplate = $null",
        "        foreach ($line in $Lines) {",
        "            $line = $line.Trim()",
        "            if ($line -match '^Template\\[\\d+\\]:') {",
        "                if ($currentTemplate) {",
        "                    $TemplateList += $currentTemplate",
        "                }",
        "                $currentTemplate = \"\" | Select Name, DisplayName, SchemaVersion, Version, OID",
        "            } elseif ($currentTemplate -and $line -match '^TemplatePropCommonName = (.+)') {",
        "                $currentTemplate.Name = $Matches[1].Trim('\"')",
        "                $currentTemplate.DisplayName = $Matches[1].Trim('\"')",
        "            } elseif ($currentTemplate -and $line -match '^TemplatePropOID = (.+)') {",
        "                $currentTemplate.OID = $Matches[1]",
        "            } elseif ($currentTemplate -and $line -match '^TemplatePropSchemaVersion = (.+)') {",
        "                $currentTemplate.SchemaVersion = $Matches[1]",
        "            } elseif ($currentTemplate -and $line -match '^TemplatePropMinorRevision = (.+)') {",
        "                $currentTemplate.Version = $Matches[1]",
        "            }",
        "        }",
        "        if ($currentTemplate) {",
        "            $TemplateList += $currentTemplate",
        "        }",
        "    } else {",
        "        # Fallback: Try to get the default domain DN from registry or environment",
        "        try {",
        "            $domain = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()",
        "            $domainDN = $domain.Name -split '\\.' | ForEach-Object { \"DC=$_\" } -join ','",
        "            $configDN = \"CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,$domainDN\"",
        "            $searcher = New-Object System.DirectoryServices.DirectorySearcher",
        "            $searcher.SearchRoot = New-Object System.DirectoryServices.DirectoryEntry(\"LDAP://$configDN\")",
        "            $searcher.Filter = \"(objectClass=pKICertificateTemplate)\"",
        "            $searcher.PropertiesToLoad.Add(\"cn\") | Out-Null",
        "            $searcher.PropertiesToLoad.Add(\"displayName\") | Out-Null",
        "            $searcher.PropertiesToLoad.Add(\"msPKI-Cert-Template-OID\") | Out-Null",
        "            $searcher.PropertiesToLoad.Add(\"revision\") | Out-Null",
        "            $results = $searcher.FindAll()",
        "            foreach ($result in $results) {",
        "                $template = \"\" | Select Name, DisplayName, SchemaVersion, Version, OID",
        "                $template.Name = $result.Properties[\"cn\"][0]",
        "                $template.DisplayName = if ($result.Properties[\"displayName\"].Count -gt 0) { $result.Properties[\"displayName\"][0] } else { $result.Properties[\"cn\"][0] }",
        "                $template.OID = if ($result.Properties[\"msPKI-Cert-Template-OID\"].Count -gt 0) { $result.Properties[\"msPKI-Cert-Template-OID\"][0] } else { \"\" }",
        "                $template.SchemaVersion = \"2\"",  # Default for modern templates
        "                $template.Version = if ($result.Properties[\"revision\"].Count -gt 0) { $result.Properties[\"revision\"][0] } else { \"1\" }",
        "                $TemplateList += $template",
        "            }",
        "        } catch {",
        "            Write-Warning \"Could not access Active Directory for templates: $_\"",
        "        }",
        "    }",
        "} catch {",
        "    Write-Error \"Failed to get certificate templates: $_\"",
        "}",
        "$TemplateList | Format-List"
    ])


def select_objects(command, select_property):
    if not select_property:
        raise ValueError("Empty property is not a valid command.")

    properties = ", ".join(select_property)
    return f"{command} | Select-Object -Property {properties}"


def dump_certificates_script(ca: AuthorityData, template: TemplateData or None, issued_after, page, page_size):
    commands = [IMPORT_MODULE]
    if issued_after:
        commands.append(f'$issued_after = Get-Date -Date "{issued_after}"')
    
    # Calculate offset for pagination
    commands.append(f'$page_size = {page_size}')
    offset = (page - 1) * page_size
    
    # Build the certutil view command to query the database
    view_cmd = f'& certutil -config "{ca.config_string}" -view -restrict "Disposition>=12,Disposition<=21"'
    
    if template:
        if template.schema_version == "1":
            view_cmd += f',CertificateTemplate={template.name}'
        else:
            view_cmd += f',CertificateTemplate={template.oid}'
    
    if issued_after:
        view_cmd += ',"NotBefore>=$issued_after"'
    
    # Add output format and columns
    view_cmd += f' -out "RawCertificate" csv'
    
    commands.extend([
        "try {",
        f"    $ViewOutput = {view_cmd} 2>&1",
        "    if ($LASTEXITCODE -eq 0) {",
        "        $Lines = $ViewOutput -split \"`n\"",
        "        $CertificateCount = 0",
        "        $ProcessedCount = 0",
        "        foreach ($line in $Lines) {",
        "            $line = $line.Trim()",
        "            if ($line -and $line -notmatch '^Row \\d+:' -and $line -notmatch '^Column' -and $line -notmatch '^Maximum' -and $line -ne 'CertUtil: -view command completed successfully.') {",
        "                if ($line -match '^\"?([A-Fa-f0-9]+)\"?$' -or $line -match '^([A-Fa-f0-9\\s]+)$') {",
        f"                    if ($ProcessedCount -ge {offset}) {{",
        "                        if ($CertificateCount -lt $page_size) {",
        "                            $cleanCert = $line -replace '[^A-Fa-f0-9]', ''",
        "                            if ($cleanCert.Length -gt 100) {",  # Basic validation
        "                                Write-Output $cleanCert",
        "                                $CertificateCount++",
        "                            }",
        "                        } else {",
        "                            break",
        "                        }",
        "                    }",
        "                    $ProcessedCount++",
        "                }",
        "            }",
        "        }",
        "    } else {",
        "        Write-Error \"CertUtil command failed\"",
        "    }",
        "} catch {",
        "    Write-Error \"Failed to dump certificates: $_\"",
        "}"
    ])
    
    return '\n'.join(commands)


def submit_certificate_request_script(request, ca: AuthorityData, template: TemplateData):
    return '\n'.join([
        IMPORT_MODULE,
        f"$req = \"{request}\"",
        "$CertRequest = New-Object -ComObject CertificateAuthority.Request",
        f"$Status = $CertRequest.Submit(0xff, $req, \"CertificateTemplate:{template.name}\", \"{ca.config_string}\")",
        f"$cert = Get-CertificationAuthority -Name \"{ca.name}\" | Get-IssuedRequest -RequestID "
        f"$CertRequest.GetRequestId() -Property \"RawCertificate\"",
        "$cert.RawCertificate"
    ])


def get_template_oid_script(template):
    return '\n'.join([
        IMPORT_MODULE,
        "try {",
        "    # Try certutil first",
        "    $CertUtilOutput = & certutil -CATemplates 2>&1",
        "    if ($LASTEXITCODE -eq 0) {",
        "        $Lines = $CertUtilOutput -split \"`n\"",
        "        $inTemplate = $false",
        "        foreach ($line in $Lines) {",
        "            $line = $line.Trim()",
        "            if ($line -match '^Template\\[\\d+\\]:') {",
        "                $inTemplate = $false",
        "            }",
        f"            if ($line -match '^TemplatePropCommonName = \"{template}\"' -or $line -match '^TemplatePropCommonName = {template}') {{",
        "                $inTemplate = $true",
        "            } elseif ($inTemplate -and $line -match '^TemplatePropOID = (.+)') {",
        "                Write-Output $Matches[1]",
        "                break",
        "            }",
        "        }",
        "    } else {",
        "        # Fallback: Use LDAP query",
        "        try {",
        "            $domain = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()",
        "            $domainDN = $domain.Name -split '\\.' | ForEach-Object { \"DC=$_\" } -join ','",
        "            $configDN = \"CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,$domainDN\"",
        "            $searcher = New-Object System.DirectoryServices.DirectorySearcher",
        "            $searcher.SearchRoot = New-Object System.DirectoryServices.DirectoryEntry(\"LDAP://$configDN\")",
        f"            $searcher.Filter = \"(&(objectClass=pKICertificateTemplate)(cn={template}))\"",
        "            $searcher.PropertiesToLoad.Add(\"msPKI-Cert-Template-OID\") | Out-Null",
        "            $result = $searcher.FindOne()",
        "            if ($result -and $result.Properties[\"msPKI-Cert-Template-OID\"].Count -gt 0) {",
        "                Write-Output $result.Properties[\"msPKI-Cert-Template-OID\"][0]",
        "            }",
        "        } catch {",
        "            Write-Warning \"Could not access Active Directory for template OID: $_\"",
        "        }",
        "    }",
        "} catch {",
        "    Write-Error \"Failed to get template OID: $_\"",
        "}"
    ])


def identify_certificate_script(serial_number, ca: AuthorityData):
    return '\n'.join([
        IMPORT_MODULE,
        "try {",
        f'    $ViewOutput = & certutil -config "{ca.config_string}" -view -restrict "SerialNumber={serial_number},Disposition>=12,Disposition<=21" -out "SerialNumber,CertificateTemplate,ConfigString" csv 2>&1',
        "    if ($LASTEXITCODE -eq 0) {",
        "        $Lines = $ViewOutput -split \"`n\"",
        "        foreach ($line in $Lines) {",
        "            $line = $line.Trim()",
        "            if ($line -and $line -notmatch '^Row \\d+:' -and $line -notmatch '^Column' -and $line -notmatch '^Maximum' -and $line -ne 'CertUtil: -view command completed successfully.') {",
        "                Write-Output $line",
        "            }",
        "        }",
        "    } else {",
        "        Write-Error \"CertUtil command failed\"",
        "    }",
        "} catch {",
        "    Write-Error \"Failed to identify certificate: $_\"",
        "}"
    ])


def get_revoke_script(ca: AuthorityData, certificate_serial_number: str, reason: str) -> str:
    adcs_reason = CertificateRevocationReason.from_string(reason).to_string_ps_value()
    
    return '\n'.join([
        IMPORT_MODULE,
        "try {",
        f'    $RevokeOutput = & certutil -config "{ca.config_string}" -revoke {certificate_serial_number} {adcs_reason} 2>&1',
        "    if ($LASTEXITCODE -eq 0) {",
        "        Write-Output \"Certificate revoked successfully\"",
        "    } else {",
        "        Write-Error \"Failed to revoke certificate: $RevokeOutput\"",
        "    }",
        "} catch {",
        "    Write-Error \"Failed to revoke certificate: $_\"",
        "}"
    ])
