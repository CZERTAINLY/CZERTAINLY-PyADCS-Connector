from PyADCSConnector.remoting.scripts import IMPORTS, IMPORT_FUNCTION_ADD_RESTRICTION, \
    IMPORT_FUNCTION_APPLY_FILTERS, IMPORT_FUNCTION_CONVERT_RAWCERTTOBYTES


def dump_certificates_script_static():
    script = f"""
{IMPORTS}
{IMPORT_FUNCTION_ADD_RESTRICTION}
{IMPORT_FUNCTION_APPLY_FILTERS}
{IMPORT_FUNCTION_CONVERT_RAWCERTTOBYTES}
# --- params / inputs ---------------------------------------------------------
$caName        = "vmi307469.3key.local\\Demo MS Sub CA"
$Page          = 1
$PageSize      = 10
$TemplateName  = "User"
$TemplateOID   = ""
$IssuedAfter   = ""

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
$view = New-Object -ComObject CertificateAuthority.View
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
$rows = $view.OpenView()
$results = New-Object 'System.Collections.Generic.List[object]'
$i = 0

for ($row = $rows.Next(); $row -ne -1; $row = $rows.Next()) {{
  if ($i -lt $skip) {{ $i++; continue }}
  if ($results.Count -ge $take) {{ break }}

  $cols = $rows.EnumCertViewColumn()
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

$results | ConvertTo-Json -Compress -Depth 4
"""
    return script
