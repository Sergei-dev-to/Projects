param(
    [Parameter(Mandatory=$true)]
    [string]$Command,
    [string]$CsvPath = "sim\data\memory_monitor.csv",
    [int]$PollSeconds = 2
)

$ErrorActionPreference = "Stop"

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "powershell.exe"
$psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -Command $Command"
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$proc = New-Object System.Diagnostics.Process
$proc.StartInfo = $psi

$rows = New-Object System.Collections.Generic.List[object]
$start = Get-Date
$null = $proc.Start()
Write-Host "[monitor] started PID=$($proc.Id)"

function Get-DescendantPids {
    param([int]$RootPid)
    $all = Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,CommandLine
    $childrenByParent = @{}
    foreach ($item in $all) {
        $parent = [int]$item.ParentProcessId
        if (-not $childrenByParent.ContainsKey($parent)) {
            $childrenByParent[$parent] = New-Object System.Collections.Generic.List[object]
        }
        $childrenByParent[$parent].Add($item)
    }
    $result = New-Object System.Collections.Generic.List[object]
    $queue = New-Object System.Collections.Generic.Queue[int]
    $queue.Enqueue($RootPid)
    while ($queue.Count -gt 0) {
        $currentPid = $queue.Dequeue()
        if ($childrenByParent.ContainsKey($currentPid)) {
            foreach ($child in $childrenByParent[$currentPid]) {
                $result.Add($child)
                $queue.Enqueue([int]$child.ProcessId)
            }
        }
    }
    return $result
}

while (-not $proc.HasExited) {
    try {
        $desc = @(Get-DescendantPids -RootPid $proc.Id)
        $pids = @($proc.Id) + @($desc | ForEach-Object { [int]$_.ProcessId })
        $processes = @($pids | ForEach-Object { Get-Process -Id $_ -ErrorAction SilentlyContinue })
        $elapsed = ((Get-Date) - $start).TotalSeconds
        $working = ($processes | Measure-Object -Property WorkingSet64 -Sum).Sum
        $private = ($processes | Measure-Object -Property PrivateMemorySize64 -Sum).Sum
        $cpu = ($processes | Measure-Object -Property CPU -Sum).Sum
        $childSummary = ($desc | ForEach-Object { "$($_.Name):$($_.ProcessId)" }) -join ";"
        $row = [pscustomobject]@{
            elapsed_s = [math]::Round($elapsed, 3)
            pid = $proc.Id
            child_processes = $childSummary
            process_count = $processes.Count
            working_set_mb = [math]::Round($working / 1MB, 3)
            private_mb = [math]::Round($private / 1MB, 3)
            cpu_s = [math]::Round($cpu, 3)
        }
        $rows.Add($row)
        Write-Host ("[monitor] t={0}s procs={1} working={2} MB private={3} MB cpu={4}s children={5}" -f $row.elapsed_s, $row.process_count, $row.working_set_mb, $row.private_mb, $row.cpu_s, $row.child_processes)
    } catch {
    }
    Start-Sleep -Seconds $PollSeconds
}

$stdout = $proc.StandardOutput.ReadToEnd()
$stderr = $proc.StandardError.ReadToEnd()
$proc.WaitForExit()

try {
    $p = Get-Process -Id $proc.Id -ErrorAction Stop
    $elapsed = ((Get-Date) - $start).TotalSeconds
    $rows.Add([pscustomobject]@{
        elapsed_s = [math]::Round($elapsed, 3)
        pid = $proc.Id
        working_set_mb = [math]::Round($p.WorkingSet64 / 1MB, 3)
        private_mb = [math]::Round($p.PrivateMemorySize64 / 1MB, 3)
        cpu_s = [math]::Round($p.CPU, 3)
    })
} catch {
}

$csv = Resolve-Path -Path . -ErrorAction Stop
$fullCsv = Join-Path $csv $CsvPath
New-Item -ItemType Directory -Force -Path (Split-Path $fullCsv) | Out-Null
$rows | Export-Csv -Path $fullCsv -NoTypeInformation

Write-Host "[monitor] exit_code=$($proc.ExitCode)"
Write-Host "[monitor] wrote $fullCsv"
Write-Host "[monitor] stdout:"
Write-Host $stdout
if ($stderr.Trim()) {
    Write-Host "[monitor] stderr:"
    Write-Host $stderr
}
exit $proc.ExitCode
