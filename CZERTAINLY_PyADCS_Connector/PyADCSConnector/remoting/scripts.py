from PyADCSConnector.utils.dump_parser import AuthorityData, TemplateData
from PyADCSConnector.utils.revocation_reason import CertificateRevocationReason

IMPORTS = """
# ---- Encoding for native processes ----
# PS 6+ honors $OutputEncoding for native exe I/O; set to UTF-8 (no BOM).
if ($PSVersionTable.PSVersion.Major -ge 6) {
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
}

# ---- Encoding for file cmdlets (works in 5.1 and 7+) ----
# Make common cmdlets default to UTF-8, so you don't have to remember -Encoding everywhere.
$PSDefaultParameterValues['Out-File:Encoding']    = 'utf8'
$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'
$PSDefaultParameterValues['Add-Content:Encoding'] = 'utf8'
$PSDefaultParameterValues['Export-Csv:Encoding']  = 'utf8'

$ProgressPreference='SilentlyContinue'
Import-Module Microsoft.PowerShell.Utility -ErrorAction SilentlyContinue
$PSModuleAutoLoadingPreference='None'
"""

IMPORTS_COM_OBJECTS = """
# Helper: release COM objects to avoid leaks
$script:__ComObjects = @()
function __Track-Com($obj) {
  if ($null -ne $obj -and $obj -is [__ComObject]) { $script:__ComObjects += $obj }
  return $obj
}
function __Release-AllCom() {
  foreach ($o in $script:__ComObjects) {
    try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($o) } catch {}
  }
  $script:__ComObjects = @()
}
"""

IMPORT_FUNCTION_ADD_RESTRICTION = """
function Add-Restriction {
  param(
    [__ComObject]$View, [int]$Col, [string]$Op, $Value,
    [int]$CVR_SEEK_EQ = 0x1, [int]$CVR_SEEK_LT = 0x2, [int]$CVR_SEEK_LE = 0x4,
    [int]$CVR_SEEK_GE = 0x8, [int]$CVR_SEEK_GT = 0x10
  )
  $seek = switch ($Op) {
    'eq' { $CVR_SEEK_EQ }
    'lt' { $CVR_SEEK_LT }
    'le' { $CVR_SEEK_LE }
    'ge' { $CVR_SEEK_GE }
    'gt' { $CVR_SEEK_GT }
    default { throw "Unsupported operator '$Op'." }
  }
  $CVR_SORT_NONE = 0
  $View.SetRestriction($Col, $seek, $CVR_SORT_NONE, $Value) | Out-Null
}
"""

IMPORT_FUNCTION_APPLY_FILTERS = """
# Accepts simple filters like: "Request.Disposition ge 12", "CertificateTemplate eq WebServer"
function Apply-Filters {
  param([__ComObject]$View, [hashtable]$ColIndex, [string[]]$Filters)
  foreach ($f in $Filters) {
    if (-not $f) { continue }
    if ($f -notmatch '^\\s*(?<col>[^ ]+)\\s+(?<op>eq|lt|le|ge|gt)\\s+(?<val>.+?)\\s*$') {
      throw "Bad filter syntax: '$f'"
    }
    $colName = $matches.col
    $op      = $matches.op
    $valRaw  = $matches.val.Trim()

    if (-not $ColIndex.ContainsKey($colName)) { throw "Unknown column '$colName'." }

    # try to coerce types: int, datetime, else string
    $val = if ($valRaw -match '^\\d+$') {
      [int]$valRaw
    } elseif ($valRaw -match '^\\d{4}-\\d{2}-\\d{2}') {
      [datetime]::Parse($valRaw)
    } else {
      # strip quotes if present
      $valRaw.Trim("'`"")
    }
    Add-Restriction -View $View -Col $ColIndex[$colName] -Op $op -Value $val
  }
}
"""

IMPORT_FUNCTION_CONVERT_RAWCERTTOBYTES = """
function Convert-RawCertToBytes {
  param([Parameter(Mandatory)]$Val)
  if ($Val -is [byte[]]) { return $Val }
  $s = [string]$Val
  if ([string]::IsNullOrWhiteSpace($s)) { return $null }
  if ($s -match '-----BEGIN [^-]+-----') {
    $s = $s -replace '-----BEGIN [^-]+-----',''
    $s = $s -replace '-----END [^-]+-----',''
  }
  $s = $s -replace '\\s',''
  [Convert]::FromBase64String($s)
}
"""

def verify_connection_script():
    """
    Returns a script that verifies the connection to the remote server.
    """
    script = f"""{IMPORTS}"""
    return script


def get_cas_script():
    script = f"""
{IMPORTS}
{IMPORTS_COM_OBJECTS}
try {{
  $cas = @()

  # ICertConfig to enumerate CAs visible to the client
  $cfg = __Track-Com (New-Object -ComObject CertificateAuthority.Config)
  [void]$cfg.Reset(0)

  # Constants for ICertAdmin::GetCAProperty
  $PROPTYPE_LONG  = 1
  $CR_PROP_CATYPE = 0x0000000A

  function Map-CaTypeText($n) {{
      switch ($n) {{
          0 {{ "Enterprise Root CA" }}
          1 {{ "Enterprise Subordinate CA" }}
          3 {{ "Standalone Root CA" }}
          4 {{ "Standalone Subordinate CA" }}
          default {{ "" }}
      }}
  }}

  do {{
      $obj = [pscustomobject]@{{
          Name         = $cfg.GetField("CommonName")
          DisplayName  = $cfg.GetField("CommonName")
          ComputerName = $cfg.GetField("Server")
          ConfigString = $cfg.GetField("Config")
          Type         = ""       # blank unless reachable
          IsEnterprise = $false   # default False unless we confirm
          IsRoot       = $false
          IsAccessible = $false
          ServiceStatus= ""       # blank unless reachable
      }}

      try {{
          $adm = __Track-Com (New-Object -ComObject CertificateAuthority.Admin)
          $catype = $adm.GetCAProperty($obj.ConfigString, $CR_PROP_CATYPE, 0, $PROPTYPE_LONG, 0)

          # If we got here, the CA responded
          $obj.Type         = Map-CaTypeText $catype
          switch ($catype) {{
              0 {{ $obj.IsEnterprise = $true; $obj.IsRoot = $true  }}
              1 {{ $obj.IsEnterprise = $true; $obj.IsRoot = $false }}
              3 {{ $obj.IsEnterprise = $false; $obj.IsRoot = $true }}
              4 {{ $obj.IsEnterprise = $false; $obj.IsRoot = $false}}
              default {{ }}
          }}
          $obj.IsAccessible = $true
          $obj.ServiceStatus = "Running"
      }} catch {{
          # Leave defaults: blank Type/ServiceStatus, booleans False, IsAccessible False
      }}

      $cas += $obj
  }} while ($cfg.Next() -ne -1)

  $__out = $cas | Select Name,DisplayName,ComputerName,ConfigString,Type,IsEnterprise,IsRoot,IsAccessible,ServiceStatus | ConvertTo-Json -Compress -Depth 4
}} finally {{
  __Release-AllCom
}}
$__out
"""
    return script


def get_templates_script():
    script = f"""
{IMPORTS}
$root = [ADSI]"LDAP://RootDSE"
$base = "LDAP://$($root.configurationNamingContext)"

$ds = New-Object System.DirectoryServices.DirectorySearcher (
    (New-Object System.DirectoryServices.DirectoryEntry $base),
    "(objectClass=pKICertificateTemplate)"
)
$ds.PageSize    = 1000
$ds.SearchScope = "Subtree"

# Only what we need
@(
  "cn",
  "displayName",
  "msPKI-Template-Schema-Version",
  "revision",                              # major (preferred)
  "msPKI-Template-Major-Revision",         # major (fallback, some forests)
  "msPKI-Template-Minor-Revision",         # minor
  "msPKI-Cert-Template-OID"
) | ForEach-Object {{ [void]$ds.PropertiesToLoad.Add($_) }}

$results = $ds.FindAll()

$TemplateList = foreach ($r in $results) {{
    $p = $r.Properties

    $cn        = $p["cn"] | Select-Object -First 1
    $disp      = $p["displayname"] | Select-Object -First 1
    $schema    = $p["mspki-template-schema-version"] | Select-Object -First 1
    $maj       = ($p["revision"] | Select-Object -First 1)
    if ($null -eq $maj) {{ $maj = $p["mspki-template-major-revision"] | Select-Object -First 1 }}
    $min       = $p["mspki-template-minor-revision"] | Select-Object -First 1
    $oid       = $p["mspki-cert-template-oid"] | Select-Object -First 1

    # Fallback: if major/minor missing, rebind this object and read only those attrs
    if ($maj -eq $null -or $min -eq $null) {{
        try {{
            $e = [ADSI]$r.Path
            $e.RefreshCache(@("revision","msPKI-Template-Major-Revision","msPKI-Template-Minor-Revision"))
            if ($maj -eq $null) {{ $maj = $e.Properties["revision"].Value
                                  if ($maj -eq $null) {{ $maj = $e.Properties["msPKI-Template-Major-Revision"].Value }} }}
            if ($min -eq $null) {{ $min = $e.Properties["msPKI-Template-Minor-Revision"].Value }}
        }} catch {{}}
    }}

    # Always show major.minor; default minor to 0 when absent
    $minorVal = if ($min -ne $null -and $min -ne "") {{ [int]$min }} else {{ 0 }}
    $version  = if ($maj -ne $null -and $maj -ne "") {{ "{0}.{1}" -f ([int]$maj), $minorVal }} else {{ $null }}

    [pscustomobject]@{{
        Name          = $cn
        DisplayName   = if ($disp) {{ $disp }} else {{ $cn }}
        SchemaVersion = if ($schema -ne $null -and $schema -ne "") {{ [int]$schema }} else {{ $null }}
        Version       = $version
        OID           = $oid
    }}
}}

$TemplateList | Sort-Object Name | ConvertTo-Json -Compress -Depth 4
"""
    return script


def dump_certificates_script(ca, template, issued_after, page, page_size):
    tmpl_name = ""
    tmpl_oid = ""
    if template:
        if str(template.schema_version) == "1":
            tmpl_name = template.name or ""
        else:
            tmpl_oid = template.oid or ""

    issued_after_str = issued_after or ""

    script = f"""
{IMPORTS}
{IMPORTS_COM_OBJECTS}
{IMPORT_FUNCTION_ADD_RESTRICTION}
{IMPORT_FUNCTION_APPLY_FILTERS}
{IMPORT_FUNCTION_CONVERT_RAWCERTTOBYTES}
try {{
  # --- params / inputs ---------------------------------------------------------
  $caName        = "{ca.config_string}"
  $Page          = {int(page)}
  $PageSize      = {int(page_size)}
  $TemplateName  = "{tmpl_name}"
  $TemplateOID   = "{tmpl_oid}"
  $IssuedAfter   = "{issued_after_str}"

  $skip = [Math]::Max(0, ($Page - 1) * $PageSize)
  $take = $PageSize

  # columns in the order we want them
  $colsWanted = @(
    'RequestID',
    'Request.StatusCode',
    'Request.DispositionMessage',
    'Request.RequesterName',
    'Request.SubmittedWhen',
    'Request.CommonName',
    'CertificateTemplate',
    'RawCertificate'
  )

  # --- connect/view ------------------------------------------------------------
  $view = __Track-Com (New-Object -ComObject CertificateAuthority.View)
  $view.OpenConnection($caName)

  # resolve column indexes once (table ordinal 0 = base)
  $colIndex = @{{}}
  foreach ($n in ($colsWanted + 'Request.Disposition')) {{
    if (-not $colIndex.ContainsKey($n)) {{
      $colIndex[$n] = $view.GetColumnIndex(0, $n)
    }}
  }}

  # 'NotBefore' may not exist on some deployments — try and allow missing
  try {{ $colIndex['NotBefore'] = $view.GetColumnIndex(0, 'NotBefore') }} catch {{ $colIndex['NotBefore'] = $null }}

  # narrow by disposition range (issued-ish states)
  Add-Restriction -View $view -Col $colIndex['Request.Disposition'] -Op ge -Value 12
  Add-Restriction -View $view -Col $colIndex['Request.Disposition'] -Op le -Value 21

  if ($TemplateName) {{ Add-Restriction -View $view -Col $colIndex['CertificateTemplate'] -Op eq -Value $TemplateName }}
  if ($TemplateOID)  {{ Add-Restriction -View $view -Col $colIndex['CertificateTemplate'] -Op eq -Value $TemplateOID }}
  if ($IssuedAfter -and $colIndex['NotBefore']) {{ Add-Restriction -View $view -Col $colIndex['NotBefore'] -Op ge -Value ([datetime]::Parse($IssuedAfter)) }}

  $extra = @()
  Apply-Filters -View $view -ColIndex $colIndex -Filters $extra

  # --- projection --------------------------------------------------------------
  $view.SetResultColumnCount($colsWanted.Count) | Out-Null
  foreach ($n in $colsWanted) {{ $view.SetResultColumn($colIndex[$n]) | Out-Null }}

  # --- iterate & shape ---------------------------------------------------------
  $rows = __Track-Com ($view.OpenView())
  $results = New-Object 'System.Collections.Generic.List[object]'
  $i = 0

  for ($row = $rows.Next(); $row -ne -1; $row = $rows.Next()) {{
    if ($i -lt $skip) {{ $i++; continue }}
    if ($results.Count -ge $take) {{ break }}

    $cols = __Track-Com ($rows.EnumCertViewColumn())
    $vals = @{{}}
    foreach ($name in $colsWanted) {{
      [void]$cols.Next()
      $vals[$name] = $cols.GetValue(0)     # 0 = flags
    }}

    $raw = $vals['RawCertificate']
    $rawBytes = if ($null -ne $raw) {{ Convert-RawCertToBytes $raw }} else {{ $null }}
    $b64 = if ($rawBytes) {{ [Convert]::ToBase64String($rawBytes) }} else {{ $null }}

    $tmpl = [string]$vals['CertificateTemplate']
    $tmplPretty = if ($tmpl -match '^\\d+(\\.\\d+)+$') {{ $tmpl }} else {{ $tmpl }}

    $obj = [pscustomobject]@{{
      RequestID                    = $vals['RequestID']
      'Request.StatusCode'         = $vals['Request.StatusCode']
      'Request.DispositionMessage' = $vals['Request.DispositionMessage']
      'Request.RequesterName'      = $vals['Request.RequesterName']
      'Request.SubmittedWhen'      = $vals['Request.SubmittedWhen']
      'Request.CommonName'         = $vals['Request.CommonName']
      CertificateTemplate          = $tmpl
      RawCertificate               = $b64
      CertificateTemplateOid       = $tmplPretty
      RowId                        = $vals['RequestID']
      ConfigString                 = $caName
      Table                        = 'Request'
    }}

    $results.Add($obj) | Out-Null
    $i++
  }}

  $__out = $results | ConvertTo-Json -Compress -Depth 4
}} finally {{
  __Release-AllCom
}}
$__out
"""
    return script


def submit_certificate_request_script(request, ca: AuthorityData, template: TemplateData,
                                      polling_interval=100, timeout=3000):
    script = f"""
{IMPORTS}
{IMPORTS_COM_OBJECTS}
try {{
  $config = "{ca.config_string}"
  $template = "CertificateTemplate:{template.name}"
  $CR_OUT_BASE64 = 0x1
  $CR_OUT_NOCRLF = 0x40000000
  $encoding = $CR_OUT_BASE64 -bor $CR_OUT_NOCRLF
  $pollMilliseconds = {polling_interval}
  $timeoutMilliseconds = {timeout}

  $csr = "{request}"

  $req = __Track-Com (New-Object -ComObject CertificateAuthority.Request)

  $disposition = $req.Submit(0xff, $csr, $template, $config)
  $requestId   = $req.GetRequestId()

  if ($disposition -eq 0 -or $disposition -eq 3) {{
      $certB64 = $req.GetCertificate($encoding)
  }} else {{
      do {{
          Start-Sleep -Milliseconds $pollMilliseconds
          $elapsed += $pollMilliseconds
          $disposition = $req.RetrievePending($requestId, $config)
      }} until ($disposition -eq 3 -or $elapsed -ge $timeoutMilliseconds)   # 3 = issued

      if ($disposition -eq 3) {{
          $certB64 = $req.GetCertificate($encoding)
      }} else {{
          throw "Timeout waiting for certificate (request $requestId)."
      }}
  }}

  $__out = [pscustomobject]@{{
    request_id   = $requestId
    disposition  = $disposition
    certificate_b64 = $certB64
  }} | ConvertTo-Json -Compress -Depth 4
}} finally {{
  __Release-AllCom
}}
$__out
"""
    return script


def identify_certificate_script(serial_number, ca: AuthorityData):
    script = f"""
{IMPORTS}
{IMPORTS_COM_OBJECTS}
{IMPORT_FUNCTION_ADD_RESTRICTION}
{IMPORT_FUNCTION_APPLY_FILTERS}
try {{
  # --- params / inputs ---------------------------------------------------------
  $caName       = "{ca.config_string}"
  $serialNumber = "{serial_number}"

  # columns in the order we want them
  $colsWanted = @(
    'SerialNumber',
    'CertificateTemplate',
    'Request.Disposition',
    'RequestID'
  )

  # --- connect/view ------------------------------------------------------------
  $view = __Track-Com (New-Object -ComObject CertificateAuthority.View)
  $view.OpenConnection($caName)

  # resolve column indexes once (table ordinal 0 = base)
  $colIndex = @{{}}
  foreach ($n in ($colsWanted + 'Request.Disposition')) {{
    if (-not $colIndex.ContainsKey($n)) {{
      $colIndex[$n] = $view.GetColumnIndex(0, $n)
    }}
  }}

  # Serial exact match
  Add-Restriction -View $view -Col $colIndex['SerialNumber'] -Op eq -Value $serialNumber
  # Limit to issued-ish states: 12..21
  Add-Restriction -View $view -Col $colIndex['Request.Disposition'] -Op ge -Value 12
  Add-Restriction -View $view -Col $colIndex['Request.Disposition'] -Op le -Value 21

  $extra = @()
  Apply-Filters -View $view -ColIndex $colIndex -Filters $extra

  # --- projection --------------------------------------------------------------
  $view.SetResultColumnCount($colsWanted.Count) | Out-Null
  foreach ($n in $colsWanted) {{ $view.SetResultColumn($colIndex[$n]) | Out-Null }}

  # --- iterate & shape ---------------------------------------------------------
  $rows = __Track-Com ($view.OpenView())
  $results = New-Object 'System.Collections.Generic.List[object]'

  for ($row = $rows.Next(); $row -ne -1; $row = $rows.Next()) {{
    $cols = __Track-Com ($rows.EnumCertViewColumn())
    $vals = @{{}}
    foreach ($name in $colsWanted) {{
      [void]$cols.Next()
      $vals[$name] = $cols.GetValue(0)     # 0 = flags
    }}

    $tmpl = [string]$vals['CertificateTemplate']
    $tmplPretty = if ($tmpl -match '^\\d+(\\.\\d+)+$') {{ $tmpl }} else {{ $tmpl }}

    $results.Add([pscustomobject]@{{
      SerialNumber               = $vals['SerialNumber']
      CertificateTemplate        = $tmpl
      CertificateTemplateOid     = $tmplPretty
      'Request.Disposition'      = $vals['Request.Disposition']
      RequestID                  = $vals['RequestID']
      ConfigString               = $caName
      Table                      = 'Certificate'
    }}) | Out-Null
  }}

  $__out = $results | ConvertTo-Json -Compress -Depth 4
}} finally {{
  __Release-AllCom
}}
$__out
"""
    return script


def get_revoke_script(ca: AuthorityData, certificate_serial_number: str, reason: str) -> str:
    adcs_reason = CertificateRevocationReason.from_string(reason).to_code()

    script = f"""
{IMPORTS}
{IMPORTS_COM_OBJECTS}
try {{
  $caConfig = "{ca.config_string}"
  $serialIn = "{certificate_serial_number}"
  $reasonCode = {adcs_reason}

  # Use native COM API: ICertAdmin.RevokeCertificate
  $admin = __Track-Com (New-Object -ComObject CertificateAuthority.Admin)

  # For RemoveFromCRL (8) the date is ignored; otherwise pass current datetime
  $when = if ($reasonCode -eq 8) {{ 0 }} else {{ (Get-Date) }}

  try {{
      $admin.RevokeCertificate($caConfig, $serialIn, $reasonCode, $when)
      Write-Host "Revocation command sent successfully."
  }}
  catch {{
      Write-Error "Revocation failed: $($_.Exception.Message)"
      return
  }}
}} finally {{
  __Release-AllCom
}}
"""
    return script
